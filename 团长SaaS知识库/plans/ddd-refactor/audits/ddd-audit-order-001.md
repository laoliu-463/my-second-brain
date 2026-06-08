---
kb_id: "KB-PLAN-DDD-AUDIT-ORDER-001"
title: "订单域 DDD 只读审查"
domain: "order"
category: "ddd_audit"
source_type: "code_audit"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 14:50:00"
related_files:
  - "D:\\Projects\\SAAS\\backend\\src\\main\\java"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-audit-order-001-20260608-145000.md"
forbidden_misread:
  - "本审查不代表已经完成订单域 DDD 重构"
  - "本审查不允许直接改订单同步代码"
  - "订单到业绩 anti-join=0 不代表结算轨已验证完成"
  - "无真实 pick_source 样本时不能宣称渠道归因闭环"
---

# 订单域 DDD 只读审查报告 (DDD-AUDIT-ORDER-001)

## 1. 最终审查结论
订单域（Order）承担着外部订单源拉取、数据一致性校验与持久化、转链归因映射的核心闭环职能。目前代码结构仍呈现强耦合的多对多注入，特别在金额双轨处理和网关适配上，尚无清晰防腐隔离。我们必须按步骤执行 Facade/Policy 拆分，且需持续补充单测保护，在此之前绝对禁止修改同步核心和物理迁移包。

## 2. 订单域当前代码结构
- **Controller**:
  - `OrderController`: 包含手动触发同步、获取订单明细和列表的编排逻辑，代码庞大（75KB，~1400行）。
  - `OrderAttributionController`: 未归因订单查询、归因摘要编排。
- **Service**:
  - `OrderSyncService`: 同步控制器，控制 10 分钟增量、6 小时补拉、6468 热同步等多个定时模式，并集成熔断器，类极其庞大（1147行，52KB）。
  - `OrderSyncPersistenceService`: 处理claim去重、乐观锁更新、落库以及后置归因副作用（补齐映射、沉淀商家、交寄样作业）。在事务提交后发布 `OrderSyncedEvent`。
  - `OrderService`: 基础增删改。
  - `OrderQueryService`: 提供支持数据权限的多维查询。
  - `OrderDualTrackAmountResolver`: 核心双轨金额映射与合并。
  - `OrderCommissionPolicy`: 提成计算相关辅助（部分逻辑存在越界计算倾向）。
  - `OrderAttributionService`: 查询未归因、做看板汇总业绩。
  - `AttributionService`: 订单归因核心逻辑类（独家商家 -> 独家达人 -> 原生团长 -> pick_source 映射，并有达人认领防冲突保护）。
- **Mapper/Entity**:
  - `ColonelsettlementOrderMapper`: 订单表 Mapper。
  - `ColonelsettlementOrder`: 订单核心事实表实体。
  - `OrderSyncDedupClaimMapper`: 并发去重主键占位 Claim 表 Mapper。
  - `ColonelOrderSettlement`: 结算表映射。
- **Gateway/SDK**:
  - `DouyinOrderGateway` (Port 接口) / `RealDouyinOrderGateway` / `TestDouyinOrderGateway`: 抖音接口调用层。
  - `OrderApi`: 对抖音开放接口的 SDK 请求和响应签名封装。
- **Event/Listener**:
  - `OrderSyncedEvent`: 订单已同步事件。
  - `OrderSyncedEventListener`: 监听事件以触发下游业绩、寄样响应。

## 3. 订单同步入口清单
1. **定时增量同步 (OrderSyncJob)**:
   - 触发方式: 定时任务。触发 `OrderSyncService.syncLatestWindow`。
   - 是否写库: 是。是否更新 checkpoint: 是 (`order:sync:last_time`)。
   - 是否发事件: 是 (`OrderSyncedEvent`)。
2. **定时补拉回扫 (PAY_RECENT)**:
   - 触发方式: 定时任务。触发 `OrderSyncService.syncPayRecentWindow`。回扫过去 6 小时已付款订单。
   - 是否更新 checkpoint: 是 (`order:sync:pay_recent_last_time`)。独占锁防止与普通增量并发。
3. **6468 事实源定时增量 (INSTITUTE_RECENT)**:
   - 触发方式: 定时任务。触发 `OrderSyncService.syncInstituteOrdersRecentWindow`。
   - 是否写库: 写预估轨。更新 checkpoint: 是 (`order:sync:institute_recent_last_time`)。
4. **6468 实时热同步 (INSTITUTE_HOT_RECENT)**:
   - 触发方式: 每分钟小窗口。触发 `OrderSyncService.syncInstituteOrdersHotRecent`。
   - 更新 checkpoint: 是 (`order:sync:institute_hot_last_time`)。
5. **手动精确同步**:
   - 触发方式: `OrderController.syncByOrderIds`。触发 `OrderSyncService.syncByOrderIds`。
   - 不影响任何 checkpoint 水位。

## 4. 6468 查询团长订单链路
- **API位置**: `buyin.instituteOrderColonel`。
- **参数与分页**: 以 `startTime`、`endTime`、`count` (100) 和 `cursor` 请求，解析 `has_more` 翻页。
- **落库机制**: 调用 `OrderDualTrackAmountResolver.applyInstituteFactToOrder` 写入预估轨，将 `syncSource` 记为 `INSTITUTE`。仅对预估金额、预估服务费等进行保存，绝不覆盖结算轨 `settle_amount` 字段。
- **上游风险**: 熔断器监视 consecutive 失败，达到 3 次会熔断 5 分钟。

## 5. 2704 团长结算订单链路
- **API位置**: `buyin.colonelMultiSettlementOrders`。
- **与6468关系**: 2704 负责更新结算轨字段（如 `settle_amount`、`effective_service_fee` 等）。在再次同步已存在订单时，调用 `mergeEstimateSnapshot` 保护已有的预估轨不被覆盖，达成双轨金额存储。
- **结算样本**: 依赖真实的结算订单数据（`time_type=update`，其在付款及结算后均有 update 时间）。如果缺乏非零结算样本，结算轨在 real-pre 无法闭环验证。

## 6. hot recent 热同步链路
- **Cron**: 每分钟执行。
- **独立锁与 checkpoint**: 分布式锁 `JobLockKeys.ORDER_SYNC_INSTITUTE_HOT`，独立水位 `order:sync:institute_hot_last_time`。
- **Freshness 日志**: 打印 `freshnessLagSeconds` 指标以监控延迟情况。
- **失败处理**: 失败时不推进 checkpoint，交由 `INSTITUTE_RECENT` 增量补偿机制进行兜底。

## 7. cursor 分页实现
- 调用 `resolveNextCursor` 方法自动寻找响应载荷中嵌套多层的分页标记（支持 `data.cursor`、`data.data.next_cursor` 等多种版本结构）。
- 退出条件包括空页、无 `next_cursor`、以及防止死循环的 `seenCursors.contains(nextCursor)` 重复校验和 `maxPages` (10/200) 阈值门禁。

## 8. Redis checkpoint / lock 审查
- **Checkpoint Keys**: `order:sync:last_time`, `order:sync:pay_recent_last_time`, `order:sync:institute_recent_last_time`, `order:sync:institute_hot_last_time`。
- **Locks**: `JobLockKeys.ORDER_SYNC`, `JobLockKeys.ORDER_SYNC_PAY_RECENT`, `JobLockKeys.ORDER_SYNC_INSTITUTE_HOT`, `JobLockKeys.ORDER_SYNC_INSTITUTE`。
- 采用 Spring `RedisTemplate` 控制，在测试模式（`testEnabled()`）下 Redis 连不上时会降级，不致阻塞测试。

## 9. Gateway / SDK 适配审查
- `RealDouyinOrderGateway` 在 contract 模式（契约测试）下直接反射返回硬编码夹具数据。
- 业务服务 `OrderSyncService` 依然持有 `DouyinOrderGateway` 接口，但网关中返回的 `OrderListResult` 与 `DouyinOrderItem` 会把 raw payload (JSON Map) 直接抛给 Service 解析，造成上游数据模型（如 `colonel_order_info` 嵌套）在服务层泄漏，未真正实现防腐（ACL）。

## 10. 落库与幂等审查
- 通过 `order_sync_dedup_claim` 去重表执行主键 `claim` 预锁定，防并发重复插入。
- 库里已有记录时使用 MyBatis-Plus 乐观锁 `updateSyncedById` 更新（防止覆盖更新已落库订单），失败则通过 OptimisticLockSupport 报错。

## 11. 默认归因审查
- **渠道归属优先级**: 独家商家 -> 独家达人 -> 原生双团长 buyin_id (`resolveNativeColonelAttribution`) -> pick_source 映射 (`findPickSourceMapping`)。
- 归属完成后，通过 `AttributionService.hasTalentClaimOwnerConflict` 进行认领冲突校验，若达人有其他人的 active 认领，则状态强置为 `UNATTRIBUTED` 并记录 Remark 为 `TALENT_CLAIM_OWNER_CONFLICT`。

## 12. 双轨金额字段审查
- 预估服务费/结算服务费均由 `OrderDualTrackAmountResolver.resolve` 从 Map 解析。
- 支持在金额缺失时由 `service_fee_rate`（服务费率）补算，并安全自动扣减 `effective_tech_service_fee`（技术服务费）。
- 金额字段存在 `settle_amount` 未回填时直接取 `pay_goods_amount` 覆盖的情况，这也是 DASH-MONEY-P0-001 计算污染的风险源头，已由 known issues 登记。

## 13. 订单状态映射审查
- 抖音 API 的 `flow_point` / `order_status` 字符串映射为本地 Integer 枚举（`PAY_SUCC` -> 1，`REFUND` / `CLOSED` -> 4）。

## 14. OrderSyncedEvent 事件链路审查
- 持久化方法 `persistOrder` 执行完毕后，调用 `publishAfterCommit`。
- 如果检测到当前在 Spring 声明式事务上下文中，通过 `TransactionSynchronizationManager.registerSynchronization` 注册同步器，在 `afterCommit()` 阶段异步发布，防止监听器中处理业绩或寄样导致原订单事务失败或死锁。

## 15. 订单域跨域依赖
- **依赖 SysUserMapper (用户域)**: 强注入，在装配渠道/招募人名称时绕过 Facade 直接查询。
- **依赖 PickSourceMappingMapper / Service (商品/渠道域)**: 持久化后通过 `pickSourceMappingService.ensureFromOrder` 动态修补转链。
- **依赖 MerchantService (商品/招商域)**: 落库时调用 `ensureMerchantFromOrder` 沉淀商家。
- **依赖 SampleLifecycleService (寄样域)**: 落库后调用 `completePendingHomeworkByOrder` 完成对应达人的待提交作业。
- **依赖 TalentClaimMapper (达人域)**: 归因时通过 `hasTalentClaimOwnerConflict` 检测。

## 16. 分层问题
- `OrderSyncService` 承载了过多的职责：时间窗滚动、熔断、原始 Json 解析、上游数据打交道，同时还作为编排层，是典型的上帝服务。
- `DataApplicationService` 标为 Service 却继承 `BaseController` 提供 API，分层极度混乱。

## 17. 订单域后续 DDD 拆分建议
1. **[第一步]** `DDD-TEST-ORDER-SYNC-001` (订单同步回归测试) 及 `DDD-TEST-ORDER-ATTRIBUTION-001` (归因规则测试)，建立测试防护红线。
2. **[第二步]** `DDD-FACADE-ORDER-001`: 创建 `OrderDomainFacade`，隔离其他领域对订单 Mappers 的越界查询。
3. **[第三步]** `DDD-INFRA-REDIS-CHECKPOINT-001`: 封装 `CheckpointStore` 端口，隔离 Redis Checkpoint/Lock 基础设施细节。
4. **[第四步]** `DDD-POLICY-ORDER-ATTRIBUTION-001`: 将 `resolveAttribution` 提炼为独立的 `OrderAttributionPolicy` 领域规则。
5. **[第五步]** `DDD-INFRA-ORDER-GATEWAY-001`: 重构 `DouyinOrderGateway` 适配器，将 raw payload 实体提取在 Gateway 内部映射为 Domain 实体，切断 SDK 数据模型向 Service 的渗透。
6. **[第六步]** `DDD-APP-ORDER-SYNC-001`: 拆分 `OrderSyncService` 为 `OrderSyncApplicationService`（负责流程编排）与 `OrderSyncScheduler`（定时驱动）。

## 18. 当前绝对禁止做的事
- 禁止直接重写订单同步。
- 禁止全局包迁移。
- 禁止修改现有金额换算和归因判定公式。
- 未建立单测保护前，禁止做任何代码拆分。

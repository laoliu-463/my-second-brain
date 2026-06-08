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
last_verified_at: "2026-06-08 14:57:33"
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

# 订单域 DDD 只读审查（DDD-AUDIT-ORDER-001）

## 1. 本次审查结论

订单域当前已经具备 2704 结算订单、6468 团长订单、hot recent、cursor 分页、Redis 水位/锁、幂等落库、afterCommit 事件等核心能力。但 DDD 结构仍处于扁平包 + 大 Service 状态，最大风险是 `OrderSyncService` 和 `OrderSyncPersistenceService` 混合了上游适配、窗口/水位、raw payload 解析、归因、持久化和跨域副作用。

本次审查不代表订单域 DDD 重构完成，不允许直接改订单同步代码。后续必须先补订单同步、归因和金额映射防护测试，再做 Facade / Policy / Gateway / Checkpoint Port 拆分。

## 2. 订单域当前代码结构

```text
Controller:
  OrderController.java                         1356 行 / 73.7 KB
  OrderAttributionController.java              256 行 / 13.1 KB

Service:
  OrderSyncService.java                       1058 行 / 50.8 KB
  OrderService.java                           1009 行 / 43.1 KB
  OrderQueryService.java                       514 行 / 23.1 KB
  Order6468PaginationDryRunService.java        497 行 / 20.6 KB
  OrderDualTrackAmountResolver.java            461 行 / 21.3 KB
  OrderAttributionService.java                 330 行 / 14.0 KB
  OrderAttributionReplayService.java           268 行 / 12.3 KB
  OrderSyncPersistenceService.java             239 行 / 12.0 KB
  OrderCommissionPolicy.java                    56 行 / 2.4 KB

Mapper / Entity:
  ColonelsettlementOrderMapper.java
  OrderSyncDedupClaimMapper.java
  ColonelOrderSettlementMapper.java
  ColonelsettlementOrder.java
  ColonelOrderSettlement.java

Gateway / Client:
  DouyinOrderGateway.java
  RealDouyinOrderGateway.java
  TestDouyinOrderGateway.java
  OrderApi.java

Job / Scheduler:
  OrderSyncJob.java
  WebhookReplayJob.java

Event / Listener:
  OrderSyncedEvent.java
  PerformanceRecordSyncListener.java
  OrderSyncedEventListener.java
```

订单域核心：`OrderSyncService`、`OrderSyncPersistenceService`、`OrderDualTrackAmountResolver`、`AttributionService`、`ColonelsettlementOrderMapper`、`RealDouyinOrderGateway`。

订单相关但跨域：`PerformanceRecordSyncListener` 属业绩域事件消费；`OrderSyncedEventListener` 处理看板缓存和达人保护期；`SampleLifecycleService.completePendingHomeworkByOrder()` 是寄样域能力但当前被订单持久化服务直接调用。

## 3. 订单同步入口清单

| 入口 | 触发 | 方法 | 上游 | 写库 | checkpoint | 事件 | 风险 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2704 增量同步 | `OrderSyncJob.syncOrders()`，默认 3 分钟 | `syncLatestWindow()` | `buyin.colonelMultiSettlementOrders` | 是 | `order:sync:last_time` | 是 | Scheduler 与手动时间范围同步共用普通水位 |
| PAY_RECENT | `OrderSyncJob.syncPayRecent()`，默认 30 分钟 | `syncPayRecentWindow()` | `buyin.colonelMultiSettlementOrders` | 是 | `order:sync:pay_recent_last_time` | 是 | 固定 6h 窗口，水位主要用于状态记录 |
| 6468 hot recent | `OrderSyncJob.syncInstituteOrdersHot()`，默认 1 分钟 | `syncInstituteOrdersHotRecent()` | `buyin.instituteOrderColonel` | 是 | `order:sync:institute_hot_last_time` | 是 | fetch 失败不推进；per-order 失败仍可能推进 |
| 6468 recent | `OrderSyncJob.syncInstituteOrdersRecent()`，默认 10 分钟 | `syncInstituteOrdersRecentWindow()` | `buyin.instituteOrderColonel` | 是 | `order:sync:institute_recent_last_time` | 是 | 与 full backfill 共用 institute 锁和水位 |
| 6468 full backfill | `OrderSyncJob.syncInstituteFullBackfill()`，默认每 6 小时 | `syncInstituteFullBackfillWindow()` | `buyin.instituteOrderColonel` | 是 | `order:sync:institute_recent_last_time` | 是 | full/recent 水位不可误读成两个独立 checkpoint |
| 手动时间范围同步 | `OrderController.POST /api/orders/sync` | `syncByTimeRange()` | 2704 | 是 | `order:sync:last_time` | 是 | Controller 编排较重 |
| Webhook 精确同步 | `DouyinWebhookEventService` / `WebhookReplayJob` | `syncByOrderIds()` | 2704 orderIds | 是 | 否 | 是 | Webhook inbox 与订单应用服务边界需明确 |
| 6468 dry-run | `OrderController.POST /api/orders/6468-pagination-dry-run` | `Order6468PaginationDryRunService.dryRun()` | 6468 | 否 | 否 | 否 | 与正式 cursor 循环重复 |

## 4. 6468 链路审查

- Gateway：`RealDouyinOrderGateway.listInstituteOrders()` 调用 `OrderApi.listSettlement()`，对应 `buyin.instituteOrderColonel`。
- 时间窗口：hot 使用 hot lag / hot overlap / hot window；recent 使用 institute 水位 + overlap，首次/超长回退 24h；full backfill 固定 24h。
- 分页：`syncItemsWithLimits()` 支持 `hasMore` 或可遍历 cursor，退出条件包括空页、无 next cursor、重复 cursor、`maxPages`、`maxOrders`。
- 落库：`SyncSource.INSTITUTE` 走 `OrderDualTrackAmountResolver.applyInstituteFactToOrder()`，只写事实/预估轨，不写 settle/effective/settleColonel 字段。
- raw payload：写入 `ColonelsettlementOrder.extraData`。
- checkpoint：fetch RuntimeException 不推进；正常返回后推进 endTime。

风险：6468 当前能入库真实订单，但真实系统转链 `pick_source` 命中样本不足时，渠道归因仍只能登记 `BLOCKED_BY_SAMPLE`。

## 5. 2704 链路审查

- Gateway：`RealDouyinOrderGateway.listSettlement()` 调用 `OrderApi.listColonelMultiSettlementOrders()`，接口为 `buyin.colonelMultiSettlementOrders`，`time_type=update`。
- 2704 负责结算轨字段：`settle_amount`、`effective_service_fee`、`effective_tech_service_fee` 等。
- 更新已有订单时调用 `mergeEstimateSnapshot()` 保护已有预估轨。
- 真实非零结算样本不足时，不能宣称结算轨完成。

风险：`OrderDualTrackAmountResolver.resolve()` 在 settlement 路径中对缺失 `settle_amount` 有回退到 `payAmount` 的逻辑，应通过 `DDD-TEST-ORDER-MONEY-MAPPING-001` 锁定行为，防止结算轨污染。

## 6. hot recent 链路审查

- Cron：默认每分钟。
- lock：`JobLockKeys.ORDER_SYNC_INSTITUTE_HOT`。
- checkpoint：`order:sync:institute_hot_last_time`。
- freshness：成功路径输出 `freshnessLagSeconds`、`latestPayTimeBefore`、`latestPayTimeAfter`、`stopReason`。
- 与普通 recent：hot 独立水位和锁，recent 每 10 分钟补偿。
- 历史阻塞：`order-sync-freshness-optimize-001` 曾因 `isv.signature-invalid` 阻塞 SLA 验证，后续本地上游恢复证据见 `douyin-upstream-reconnect-local-001`。

需要补测试：fetch 失败不推进水位、per-order 失败是否允许推进水位、`MAX_PAGES` / `MAX_ORDERS` 下的 checkpoint 行为。

## 7. cursor 分页审查

- 正式同步：`OrderSyncService.resolveNextCursor()` 读取 `data.cursor`、根 `cursor`、`data.next_cursor` / `data.nextCursor` 和 `response.nextCursor()`。
- Gateway 标准化：`RealDouyinOrderGateway.toOrderListResult()` 兼容 `has_more` / `hasMore` / `has_next` / `hasNext` 与 `next_cursor` / `cursor`。
- dry-run：`Order6468PaginationDryRunService` 独立实现分页循环。

结论：cursor 行为已具备，但正式同步与 dry-run 存在重复逻辑，后续可在测试保护后提取 `CursorPager`。

## 8. Redis checkpoint / lock 审查

checkpoint：

```text
order:sync:last_time
order:sync:pay_recent_last_time
order:sync:institute_recent_last_time
order:sync:institute_hot_last_time
```

lock：

```text
JobLockKeys.ORDER_SYNC
JobLockKeys.ORDER_SYNC_PAY_RECENT
JobLockKeys.ORDER_SYNC_INSTITUTE
JobLockKeys.ORDER_SYNC_INSTITUTE_HOT
```

DDD 建议：抽 `CheckpointStore` / `OrderSyncLockPort`，避免应用服务直接散落 Redis key、读写和测试模式降级逻辑。

## 9. Gateway / SDK 适配审查

当前已有 `DouyinOrderGateway` Port 和 `RealDouyinOrderGateway` Adapter，但 ACL 不彻底：`DouyinOrderItem.rawPayload()` 仍把上游 Map 传给 `OrderSyncService`、`AttributionService`、`OrderDualTrackAmountResolver` 解析。

后续 `DDD-INFRA-ORDER-GATEWAY-001` 应在 Gateway 内将 `colonel_order_info`、`colonel_order_info_second`、金额字段、状态字段映射成订单域输入 DTO，服务层不直接解析上游 JSON Map。

## 10. 落库与幂等审查

- `OrderSyncDedupClaimMapper.claim()` 防并发重复处理。
- 已存在订单走 `mergeBySource()` + `updateSyncedById()` 乐观锁。
- 新订单走 `insertIgnoreByOrderId()`。
- 持久化后执行 `runAttributionFollowUps()`，再 publishAfterCommit 事件。

风险：`runAttributionFollowUps()` 直接调用商品/招商/寄样域服务，导致订单持久化事务内混入跨域副作用。

## 11. 默认归因审查

流程：

```text
source + order
 -> ProductOperationState.assigneeId 作为招商输入
 -> exclusive.enabled=true 时独家商家/达人分支（V1 默认关闭且禁止启用）
 -> colonel_order_info / colonel_buyin_id 原生团长映射
 -> pick_source / pick_extra 映射
 -> talent claim owner conflict guard
 -> ATTRIBUTED / UNATTRIBUTED + reason
```

结论：归因服务输入来源清楚，但跨商品/达人/历史独家能力的 Mapper / Service 依赖较多。`exclusive.enabled=false` 是当前 V1 运行边界，不得把独家分支写成当前已启用能力。

## 12. 双轨金额字段审查

- 6468：`applyInstituteFactToOrder()` 写 `order_amount`、`actual_amount`、`estimate_service_fee`、`estimate_tech_service_fee`，不写结算轨。
- 2704：`applyToOrder()` 写 `settle_amount`、`effective_service_fee`、`effective_tech_service_fee` 等。
- 保护逻辑：6468 更新已有订单时保留结算轨；2704 更新已有订单时保留预估轨。

风险：

- settlement 路径缺 `settle_amount` 时回退 `payAmount`。
- 旧字段 `settle_colonel_commission` 在 effective 为 0 时回退 estimate。
- 不可在审查任务中修改公式，必须先补测试。

## 13. 订单状态映射审查

`RealDouyinOrderGateway.asInteger()` 映射：

```text
PAY_SUCC -> 1
REFUND / REFUND_SUCCESS / CLOSED -> 4
数字/数字字符串 -> int
无法解析 -> null
```

后续可提取 `OrderStatusMapper` / Policy，但必须保证状态语义不变。

## 14. OrderSyncedEvent 事件链路审查

生产者：`OrderSyncPersistenceService.publishOrderSynced()`。

发布时机：事务同步 active 时注册 `afterCommit()`；无事务同步时立即发布。

消费者：

- `PerformanceRecordSyncListener`：异步消费订单事件，查询订单 Mapper，调用 `PerformanceCalculationService.upsertFromOrder()`，再发布 `PerformanceCalculatedEvent`。
- `OrderSyncedEventListener`：异步更新 dashboard summary、清缓存、重置达人保护期。

关键纠偏：寄样自动完成不是事件 listener 消费，而是 `OrderSyncPersistenceService.runAttributionFollowUps()` 直接调用 `SampleLifecycleService.completePendingHomeworkByOrder()`。这是当前订单域跨寄样域的主要边界风险。

## 15. 跨域依赖清单

| 订单域文件 | 依赖对象 | 依赖方式 | 是否合理 | 建议 |
| --- | --- | --- | --- | --- |
| `OrderSyncPersistenceService` | `PickSourceMappingService` | Service | 越界 | 商品 Facade / Event |
| `OrderSyncPersistenceService` | `MerchantService` | Service | 越界 | 商家/招商 Facade |
| `OrderSyncPersistenceService` | `SampleLifecycleService` | Service | 越界且写状态 | 改为事件消费前先补测试 |
| `OrderSyncPersistenceService` | `SysUserMapper` | Mapper | 越界 | UserDomainFacade |
| `AttributionService` | `PickSourceMappingMapper`、`ProductOperationStateMapper` | Mapper | 输入合理但访问越界 | Product / Mapping Port |
| `AttributionService` | `TalentMapper`、`TalentClaimMapper` | Mapper | 输入合理但访问越界 | Talent Facade |
| `PerformanceRecordSyncListener` | `ColonelsettlementOrderMapper` | Mapper | 事件消费合理但穿透 | OrderDomainFacade |
| `OrderController` | `PerformanceBackfillService`、佣金相关服务 | Controller 编排 | 边界混杂 | Application Service 拆分 |

## 16. 分层问题

- `OrderController` 过胖，混合同步、dry-run、归因重算、业绩回填、佣金操作、查询和统计。
- `OrderSyncService` 是订单域最明显 God Service。
- `OrderSyncPersistenceService` 名称是持久化，但执行跨域副作用。
- `DataApplicationService` 虽不属于订单域核心，但跨订单/业绩/分析/独家状态，是后续分析/业绩审查必须覆盖的跨域服务。

## 17. God Service / 胖 Service

1. `OrderSyncService.java`：1058 行，职责最重。
2. `OrderService.java`：1009 行，展示投影和查询辅助多。
3. `OrderController.java`：1356 行，胖 Controller。
4. `Order6468PaginationDryRunService.java`：497 行，与正式分页重复。
5. `OrderDualTrackAmountResolver.java`：461 行，金额字段兼容复杂。

## 18. DDD 拆分建议

1. `DDD-TEST-ORDER-SYNC-001`
2. `DDD-TEST-ORDER-ATTRIBUTION-001`
3. `DDD-TEST-ORDER-MONEY-MAPPING-001`
4. `DDD-FACADE-ORDER-001`
5. `DDD-POLICY-ORDER-ATTRIBUTION-001`
6. `DDD-INFRA-ORDER-GATEWAY-001`
7. `DDD-INFRA-REDIS-CHECKPOINT-001`
8. `DDD-EVENT-ORDER-SYNCED-001`
9. `DDD-APP-ORDER-SYNC-001`

包结构迁移必须继续放在后面，不能提前。

## 19. 后续任务建议

下一任务建议：`DDD-AUDIT-PERFORMANCE-001`。

原因：业绩域直接消费 `OrderSyncedEvent` 并写 `performance_records`，订单域审清后应先只读审查业绩域如何消费订单事实、如何处理双轨金额和历史 settle 污染，而不是立即改订单代码。

## 20. 不建议现在做的事

- 不重写订单同步。
- 不全局 package migration。
- 不改金额公式。
- 不启用独家达人 / 独家商家。
- 不把寄样自动完成直接改成事件消费。
- 不用 mock 或无样本事实证明 real-pre 闭环。

## 21. 相关 reports

- `D:\Projects\SAAS\harness\reports\ddd-audit-order-001-20260608-145000.md`
- `D:\Projects\SAAS\harness\reports\evidence-20260608-145000-ddd-audit-order-001.md`
- `D:\Projects\SAAS\harness\reports\retro-20260608-145000-ddd-audit-order-001.md`
- `D:\Projects\SAAS\harness\reports\order-6468-pagination-fix-001-20260606-153950.md`
- `D:\Projects\SAAS\harness\reports\order-sync-freshness-optimize-001-20260606-165000.md`
- `D:\Projects\SAAS\harness\reports\order-performance-event-after-commit-fix-001-20260606-121000.md`
- `D:\Projects\SAAS\harness\reports\evidence-20260606-125134-douyin-upstream-reconnect-local-001.md`

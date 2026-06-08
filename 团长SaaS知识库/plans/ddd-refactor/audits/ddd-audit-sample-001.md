---
kb_id: "KB-PLAN-DDD-AUDIT-SAMPLE-001"
title: "寄样域 DDD 只读审查"
domain: "sample"
category: "ddd_audit"
source_type: "code_audit"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 15:15:00"
related_files:
  - "D:\\Projects\\SAAS\\backend\\src\\main\\java"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-audit-sample-001-20260608-151500.md"
forbidden_misread:
  - "本审查不代表已经完成寄样域 DDD 重构"
  - "本审查不允许直接改寄样状态机"
  - "无真实 pick_source 样本时不能宣称寄样自动完成闭环"
  - "PENDING_AUDIT 与 PENDING_REVIEW 不得在只读审查中改名"
  - "V1 不默认启用物流 API 自动跟踪或 30 天自动关闭"
---

# 寄样域 DDD 只读审查报告

## 一、 寄样域当前代码结构

寄样域当前代码结构如下：
* **Controller**:
  * [SampleController.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/controller/SampleController.java) (继承自 `SampleApplicationService`)
  * [SampleFilterOptionsController.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/controller/SampleFilterOptionsController.java)
  * [AdminSampleLogisticsController.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/controller/AdminSampleLogisticsController.java)
  * [AdminDouyinQuickSampleController.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/controller/AdminDouyinQuickSampleController.java)
* **ApplicationService**:
  * [SampleApplicationService.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/sample/SampleApplicationService.java) (核心应用服务，包含了 Controller 所有业务实现，3696行，胖服务)
* **DomainService**:
  * [SampleLifecycleService.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/SampleLifecycleService.java) (生命周期管理，如订单驱动自动完成、自动关闭超时寄样等)
  * [SampleEligibilityService.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/SampleEligibilityService.java) (达人寄样资格校验)
  * [ProductQuickSampleService.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/ProductQuickSampleService.java) (商品库快速寄样服务，跨域编排)
  * [SampleWriteTransactionService.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/SampleWriteTransactionService.java) (写事务封装)
  * [SampleStatusLogService.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/SampleStatusLogService.java)
  * [SampleLogisticsSyncService.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/SampleLogisticsSyncService.java)
  * [SampleLogisticsImportService.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/SampleLogisticsImportService.java)
  * [SampleLogisticsSubscriptionService.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/SampleLogisticsSubscriptionService.java)
* **Mapper**:
  * `SampleRequestMapper`
  * `SampleStatusLogMapper`
* **Entity**:
  * `SampleRequest` (寄样单主表)
  * `SampleStatusLog` (状态日志)
  * `SampleLogisticsTrace` (物流轨迹)
* **Event & Consumer**:
  * `SampleDomainEventPublisher` (发布寄样创建、发货、签收、完成、关闭等领域事件)
  * [SampleConfigChangedConsumer.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/domain/event/SampleConfigChangedConsumer.java) (配置变更监听)

---

## 二、 核心业务链路梳理

### 1. 寄样申请入口链路 (手动)
* **入口名称**: 手动申请寄样
* **触发方式**: `POST /samples` -> `SampleController.createSample`
* **文件路径**: [SampleApplicationService.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/sample/SampleApplicationService.java#L318-L384)
* **方法名**: `createSample`
* **是否写库**: 是，写入 `sample_request`，并回写收货地址到达人认领表 `talent_claim`，写入状态日志 `sample_status_log`。
* **跨域查询**:
  * 查询商品: `requireProduct` (跨域查询 `Product` 与 `ProductSnapshot`)
  * 查询达人: `resolveSampleTalentInfo` (跨域查询 `CrawlerTalentInfo`，不存在则自动在 `Talent` 主表中创建达人记录)
  * 查询认领: `ensureChannelTalentClaim` (校验 `talent_claim` 中该达人是否在当前渠道名下，组长/管理员豁免)
* **读取配置**: `checkSevenDaysLimit` 读取 7 天重复限制配置，`ensureEligibilityReasonIfNeeded` 读取寄样默认门槛标准。
* **事务边界**: `SampleWriteTransactionService.execute`，声明式内部控制。
* **风险**: 混用了达人爬虫表和达人主表、商品表和商品快照表，实体边界横穿严重。

### 2. 商品库快速寄样入口链路
* **入口名称**: 批量快速寄样
* **触发方式**: `POST /admin/quick-samples/apply` -> `AdminDouyinQuickSampleController.applyQuickSample` -> `ProductQuickSampleService.applyQuickSample`
* **文件路径**: [ProductQuickSampleService.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/ProductQuickSampleService.java#L188-L239)
* **方法名**: `applyQuickSample`
* **是否写库**: 是，独立事务写库，逐个达人处理 `createSingleSample`。
* **商品主表兜底**: `resolveQuickSampleProductContext` 会首先基于前端传入的商品库 `ProductSnapshot.id` 解析商品快照，并调用 `ensurePersistedProduct`，若主商品表 `product` 不存在对应记录，则将快照物化成 `product` 记录持久化（写入 `product` 表），以避免 `sample_request` 插入时因外键约束而失败。
* **手动私海达人兜底**: 若达人在爬虫达人表中不存在，会回退到 `Talent` 表查找，若仍然没有，则说明是不存在的达人，会报错 `达人不存在`。如果 `Talent` 主表存在该手动达人，则调用 `buildCrawlerSnapshotFromTalent` 生成一个爬虫达人快照。
* **外部抖店寄样网关与本地降级**:
  * 若抖店外部寄样开启并且 SDK 支持，优先调用 `DouyinQuickSampleGateway.apply` 获得外部寄样单 ID，状态为 `PENDING_AUDIT`。
  * 外部网关不通或 SDK 不支持时，本地降级 `APPLY_SOURCE_LOCAL_FALLBACK`。

### 3. 寄样状态机与流转校验
设计状态包含 8 个：
* `PENDING_AUDIT` (1, 待审核)
* `PENDING_SHIP` (2, 待发货)
* `SHIPPING` (3, 发货中)
* `DELIVERED` (4, 已签收)
* `PENDING_HOMEWORK` (5, 待交作业)
* `COMPLETED` (6, 已完成)
* `REJECTED` (7, 已驳回)
* `CLOSED` (8, 已关闭)

**流转与角色限制**:
* 审核 (`PENDING_SHIP` / `REJECTED`): 仅 `ADMIN`、`BIZ_STAFF` (招商角色) 可执行。
* 物流发货和签收推进 (`SHIPPING` / `DELIVERED` / `PENDING_HOMEWORK`): 仅 `ADMIN`、`OPS_STAFF` (运营角色) 可执行。
* 自动完成和关闭 (`COMPLETED` / `CLOSED`): 仅允许系统自动推进，手动请求会抛出 Forbidden 异常。
* 状态兼容转换: 在返回给前端或转换成看板的 legacy 状态时，会将 `SHIPPING` 和 `DELIVERED` 合并映射为 `SHIPPED`，`PENDING_HOMEWORK` 映射为 `PENDING_TASK`，`COMPLETED` 映射为 `FINISHED`。

### 4. 审核与批量审核链路
* **触发方式**: `POST /samples/batch-approve` / `POST /samples/batch-reject`
* **文件路径**: [SampleApplicationService.java](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/sample/SampleApplicationService.java#L1310-L1407)
* **规则**: 逐条加载、确认当前状态为 `PENDING_AUDIT`，更改状态并写入 `SampleStatusLog`，发布审核事件。驳回时 `remark` (拒绝原因) 必填。

### 5. 发货/物流/签收链路
* **录入物流**: 动作 `SHIPPING`，校验 `trackingNo` (快递单号) 必填，设置物流来源 `MANUAL`。调用 `sampleLogisticsSubscriptionService.subscribeAfterShipment` 订阅物流信息。
* **签收确认**: 运营可以调用接口将 `SHIPPING` 推进到 `DELIVERED`，或直接签收进入 `PENDING_HOMEWORK`。
* **物流 API**: V1 阶段仅在手动刷新和批量同步物流时执行轨迹拉取，不提供外部物流的自动轨迹实时推送接收。

### 6. 订单触发寄样完成链路
* **实现路径**: [SampleLifecycleService.completePendingHomeworkByOrder](file:///D:/Projects/SAAS/backend/src/main/java/com/colonel/saas/service/SampleLifecycleService.java#L77-L119)
* **核心匹配条件**:
  1. 通过订单归属人 (`userId` / `channelUserId`) 结合该达人活跃认领关系 (`talent_claim`) 确认最终的渠道负责人 `sampleOwnerId`。
  2. 从订单 `extraData` 中提取达人 UID (`talent_uid` / `author_id`)。
  3. 精确匹配 `channel_user_id = sampleOwnerId` AND `talent_uid = talentUid` AND `product.product_id = order.product_id` 且状态为 `PENDING_HOMEWORK` (5) 的记录。
  4. 按创建时间升序排列，**仅取最早一条 (LIMIT 1)** 执行状态流转，变更为 `COMPLETED`，写入状态日志，并发布 `SampleCompleted` 领域事件。
* **限制**:
  * 若订单无法获取 `product_id`，或无法解析 `talent_uid`，则无法自动触发完成。
  * 仅针对处于 `PENDING_HOMEWORK` 的寄样单。如果处于 `SHIPPING` 或 `DELIVERED` 状态，不会被订单触发完成（需先由物流同步或运营推进到 `PENDING_HOMEWORK`）。

### 7. 7 天重复申请限制
* **配置项**:
  * 限制开关: `SystemConfigKeys.SAMPLE_RESTRICT_ENABLED`
  * 限制天数: `SystemConfigKeys.SAMPLE_RESTRICT_DAYS` (默认 7 天)
* **限制维度**: 限制同一渠道专员 (`channel_user_id`)、同一达人 (`talent_id`)、同一商品 (`product_id`) 且非 `REJECTED` (已驳回) 状态 of 申请。
* **豁免**: 管理员 (`ADMIN`) 和 渠道主管 (`CHANNEL_LEADER`) 享有豁免权，直接跳过此项限制。

### 8. 达人门槛校验
* **评估项**: 最低达人等级 `minLevel`，近 30 天订单销售总额 `min30DaySales`。
* **近 30 天销售额**: 优先读 `Talent.sales30d`，为空时通过 `JdbcTemplate` 对 `colonelsettlement_order` 主表按 `talent_uid` 进行实时 `SUM` 聚合。
* **不达标继续申请**: 达人未满足默认标准时，普通申请必须填写备注 `remark` 作为申请原因，否则拒绝创建。

---

## 三、 跨域依赖与边界审查

寄样域存在以下严重的跨域穿透问题：
1. **Mapper / Repository 横穿**:
   * `SampleApplicationService` 注入了 `ProductMapper`、`ProductOperationStateMapper`、`ProductSnapshotMapper`、`SysUserMapper`、`TalentMapper`、`TalentClaimMapper`，直接操作其它域的数据表。
   * `SampleLifecycleService` 直接操作了 `TalentClaimMapper`，并编写原生 SQL 关联 `product` 表来获取外部商品 ID。
   * 寄样 Mapper SQL 直接做多表 JOIN（商品表、达人表、用户表等）。
2. **DTO / Entity / VO 混用**:
   * `SampleController` 作为 `SampleApplicationService` 的子类，直接暴露了 `SampleVO`。
   * `SampleVO` 承载了太多的跨域冗余数据，如 `ProductSnapshot` 上的 `shop_name`、`shop_id`、`priceText`，以及 `SysUser` 的显示名称格式化等。
3. **数据范围与权限过滤风险**:
   * 列表查询 `getSamplePage` 混杂了复杂的多角色控制（纯运营强制限制状态在 `PENDING_SHIP` 及以后；招商专员限制查看自己负责商品的待审核单据）。
   * `assertCanAccessSample` 内直接通过商品运营状态表 `product_operation_state` 来判断该商品是否分配给当前用户。
   * 查询命令直接横穿权限架构，使得数据越权风险极高，不便单元测试。

---

## 四、 寄样域重构与测试设计

### 1. 拆分与重构建议
* **Phase 1: 防护测试**: 建立 `SampleLifecycleServiceTest` 单元测试，重点覆盖：
  * 订单匹配与归因、认领权回退匹配规则。
  * 7天申请限制及角色豁免测试。
  * 达人门槛校验、`sales30d` 回退 `colonelsettlement_order` 实时聚合逻辑。
* **Phase 2: 提取 Policy / Facade**:
  * 提取 `SampleApplyPolicy`：处理申请限制、达人资质门槛校验。
  * 提取 `SampleCompletionPolicy`：定义如何根据订单事实触发寄样状态变更为已完成。
  * 引入 `TalentDomainFacade`、`ProductDomainFacade`、`UserDomainFacade` 封装跨域数据拉取，不再在寄样服务中直接注入它们的 Mapper。
  * 引入 `SampleLifecycleApplicationService` 承载寄样生命周期的编排，把 Controller 中的胖逻辑移走。

### 2. 下一步任务建议
* 建议先进行 **[DDD-TEST-ORDER-SYNC-001](tasks/ddd-test-order-sync-001.md)** 任务，为订单域和后续寄样完成链路提供集成防护测试，再推进寄样域自身防护测试。

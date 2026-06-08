---
kb_id: "KB-PLAN-DDD-AUDIT-PERFORMANCE-001"
title: "业绩域 DDD 只读审查"
domain: "performance"
category: "ddd_audit"
source_type: "code_audit"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 15:00:00"
related_files:
  - "D:\\Projects\\SAAS\\backend\\src\\main\\java"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-audit-performance-001-20260608-150000.md"
forbidden_misread:
  - "本审查不代表已经完成业绩域 DDD 重构"
  - "本审查不允许直接改业绩计算公式"
  - "订单到业绩 anti-join=0 不代表结算轨已验证完成"
  - "无真实 pick_source 样本时不能宣称渠道归因闭环"
  - "V1 不启用独家达人或独家商家覆盖"
---

# 业绩域 DDD 只读审查报告 (DDD-AUDIT-PERFORMANCE-001)

## 1. 最终审查结论
业绩域（Performance）作为计算服务费收益、提成、冲正的核心自治领域，必须实现公式稳定与分层清晰。目前本域由于在 `CommissionService` 中直接使用 `JdbcTemplate` 进行配置域（Config）的跨域读取，且在 `PerformanceCalculationService` 中承载了较多的查询和映射逻辑，构成了一定的架构风险。下一步应当在防护单测锁定公式口径的前提下，通过建立 `PerformanceDomainFacade` 与 `PerformanceCalculationPolicy` 将计算和基础设施彻底剥离。

## 2. 业绩域当前代码结构
- **Controller**:
  - `PerformanceController`: 业绩单笔/批量/分页查询、汇总以及 Excel 导出和月度业绩重算的端点编排。
- **Service**:
  - `PerformanceCalculationService`: 核心计算，处理双轨金额映射与 upsert 持久化，为本域 God Service。
  - `PerformanceBackfillService`: 执行历史业绩批量补算及未失效业绩重算。
  - `PerformanceQueryService`: 配合数据范围的安全查询。
  - `PerformanceSummaryService`: 指标汇总服务。
  - `PerformanceMonthRecalculationService`: 月度异步重算实现。
  - `PerformanceMetricsQueryService`: 查询特定聚合指标。
  - `PerformanceExportService`: 导出 Excel 编排。
  - `CommissionService`: 计算招商/渠道提成，包含获取活动级或全局默认提成比例。
- **Mapper/Entity**:
  - `PerformanceRecordMapper`: 业绩表 Mapper。
  - `PerformanceRecord`: 业绩明细实体。
- **Listener/Job**:
  - `PerformanceRecordSyncListener`: 消费 `OrderSyncedEvent` 的异步监听器，计算后发布 `PerformanceCalculatedEvent`。
  - `PerformanceBackfillJob` / `PerformanceRecalculateFailedJob` / `PerformanceCacheWarmupJob`: 对应定时与重算任务。

## 3. performance_records 写入与更新链路
- **Event 驱动**: 监听 `OrderSyncedEvent` 触发异步 upsert。
- **手动补算**: 调用 `PerformanceBackfillService.backfill`，支持只回填缺失（`onlyMissing`）或按范围全量覆盖。
- **单笔/重算**: 事务更新 `upsertFromOrder`。
- **并发防护**: 数据库层面的 upsert 主键冲突覆盖以及行级乐观锁控制，更新时 `calculation_version` 自增 1。

## 4. 订单事件进入业绩计算链路
- 监听 `OrderSyncedEvent` 事件，使用 `@Async` 异步执行。
- 监听器内通过 `orderMapper.findByOrderId` 读取最新的订单快照，然后执行 `PerformanceCalculationService.upsertFromOrder` 计算。
- 事件已由之前的 `afterCommit` 修复锁定，排除了原先订单未写入而异步 Listener 读到 null 的时序缺口。

## 5. PerformanceCalculationService 职责与 God Service 风险
- 行数约 219 行，方法高聚度。虽然类文件适中，但它强行合并了：订单读取、三链默认归因映射（最终归因 final_channel/final_recruiter 强等价于 default_*）、双轨金额初始化、状态机校验（ countsTowardPerformance 是否计入业绩）、以及 upsert 调用。
- 建议将双轨提成算法提炼为独立的 `PerformanceCalculationPolicy`。

## 6. PerformanceBackfillService 补算链路
- 暴露了 `POST /api/orders/performance-backfill` 手动触发入口。
- 使用 `NOT EXISTS` 进行防重复回填防护，防止覆盖已有记录或进行无效重写。
- 修复机制：包含 `reconcileInvalidatedPerformance` 接口，用以强制同步修复在订单表已退款（status=5）但业绩表仍处于 `is_valid=true` 的过期残余。

## 7. 双轨金额字段与公式
- 订单与业绩严格实行双轨公式：
  - **预估服务费收益** = 预估服务费收入 - 预估技术服务费（`estimateTechServiceFee`）- 预估服务费支出（`estimateServiceFeeExpense`）。
  - **结算服务费收益** = 实际服务费收入 - 实际服务费支出（已完成扣减技术服务费）。
  - **毛利** = 服务费收益 - 招商提成（`bizCommission`）- 渠道提成（`channelCommission`）。
- **已修复风险**: 曾有 settle_amount 回退导致业绩表 settle_amount 污染的计算错误，现已统一由 `nvl` 防护和零提成重写修复。
- **毛利口径**: 媒介/渠道提成和招募者提成已剥离计算，毛利属于 V1 口径，需在前端正确补齐展示。

## 8. 配置域提成比例读取路径
- 在 `CommissionService` 中通过 `jdbcTemplate` 直接查询 `system_config` 表中对应的 `commission.business_default_ratio` 等参数，这构成了对配置库的 Mapper 直接越界查询。应重构为依赖 `ConfigDomainFacade` 接口。

## 9. 默认归因与最终归因关系
- 业绩表目前将 `final_channel_user_id` 和 `final_recruiter_user_id` 直接赋予订单域归因结果（即 `final = default`）。
- V1 明确跳过独家达人/独家商家的复杂覆盖，在业务实现中保持此静默状态（Dormant/V2）。

## 10. 退款 / 失效 / 冲正处理
- 订单状态为 4（失效）或 5（已退款）时，通过 `OrderCommissionPolicy.countsTowardPerformance` 拦截，在 `zeroCommissions` 方法中将该订单对应业绩的所有提成和收益全部置 0，并标记为 `is_reversed=true` 和 `is_valid=false`。

## 11. 业绩查询与 Dashboard 读取路径
- 看板 `/api/dashboard/metrics` 直接通过 SQL 聚合业绩表（`performance_records`），与明细读取隔离。
- 存在分析域直接跨界消费 `PerformanceRecord` 结构的情况，需要后续在分析模块审计中继续隔离。

## 12. 用户域数据范围过滤
- 使用 `PerformanceAccessScope` 实现 `ALL`、`DEPT`、`PERSONAL` 的数据范围切面过滤。
- 存在越界直接读取用户信息的情况，应通过 `UserDomainFacade` 进行用户鉴权和组织提取。

## 13. 业绩域后续 DDD 拆分建议
1. **[第一步]** `DDD-TEST-PERFORMANCE-CALC-001` (建立双轨公式单测保护) 及 `DDD-TEST-PERFORMANCE-REFUND-001` (退款状态置零验证)。
2. **[第二步]** `DDD-FACADE-PERFORMANCE-001`: 创建 `PerformanceDomainFacade` 隔离外界对业绩表结构的直接访问。
3. **[第三步]** `DDD-POLICY-PERFORMANCE-CALC-001`: 将双轨收益与毛利提取为 `PerformanceCalculationPolicy` 纯领域规则对象。
4. **[第四步]** `DDD-EVENT-PERFORMANCE-CALCULATED-001`: 重构 `PerformanceCalculatedEvent` 的外发机制。
5. **[第五步]** `DDD-QUERY-PERFORMANCE-SUMMARY-001`: 剥离 `PerformanceSummaryQueryService` 实现读写分离 (CQRS)。

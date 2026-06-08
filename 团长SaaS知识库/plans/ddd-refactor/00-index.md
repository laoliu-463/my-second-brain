---
kb_id: "KB-PLAN-DDD-00-INDEX"
title: "DDD 重构计划索引"
domain: "harness"
category: "ddd_plan"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 13:59:08"
related_files:
  - "D:\\Projects\\SAAS\\harness\\CURRENT_STATE.md"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# DDD 重构计划索引

## 1. 定位

这是抖音团长 SaaS V1 的 DDD 渐进式重构长期计划入口。它沉淀到外部知识库，不替代项目 docs 的业务事实，也不表示代码已经完成重构。

## 2. 当前阶段

当前处于 Phase 0 只读审查准备完成 / 待执行第一个审查任务。本次任务只生成计划、任务矩阵和第一批任务卡，不修改业务代码。

## 3. 总入口

- [总路线图](01-master-roadmap.md)
- [任务矩阵](02-task-matrix.md)
- [执行顺序](03-execution-order.md)
- [风险门禁](04-risk-gates.md)
- [测试策略](05-testing-strategy.md)
- [重构规则](06-refactor-rules.md)
- [当前不要做](07-do-not-do-now.md)

## 4. 阶段入口

- [Phase 0：只读审查](phases/phase-0-audit.md)
- [Phase 1：防护测试](phases/phase-1-protection-tests.md)
- [Phase 2：Facade 收敛](phases/phase-2-facade-convergence.md)
- [Phase 3：Application Service 分层](phases/phase-3-application-services.md)
- [Phase 4：Domain Policy 提取](phases/phase-4-domain-policies.md)
- [Phase 5：Infrastructure Adapter 隔离](phases/phase-5-infrastructure-adapters.md)
- [Phase 6：事件与一致性治理](phases/phase-6-events-consistency.md)
- [Phase 7：包结构迁移](phases/phase-7-package-migration.md)

## 5. 领域计划入口

- [用户域](domains/user-ddd-plan.md)
- [配置域](domains/config-ddd-plan.md)
- [商品域](domains/product-ddd-plan.md)
- [达人域](domains/talent-ddd-plan.md)
- [寄样域](domains/sample-ddd-plan.md)
- [订单域](domains/order-ddd-plan.md)
- [业绩域](domains/performance-ddd-plan.md)
- [分析模块](domains/analysis-ddd-plan.md)
- [跨域治理](domains/cross-domain-ddd-plan.md)

## 6. 第一批任务卡入口

- [任务索引](tasks/00-task-index.md)
- [DDD-AUDIT-CROSS-DOMAIN-001](tasks/ddd-audit-cross-domain-001.md)
- [DDD-AUDIT-ORDER-001](tasks/ddd-audit-order-001.md)
- [DDD-AUDIT-PERFORMANCE-001](tasks/ddd-audit-performance-001.md)
- [DDD-AUDIT-SAMPLE-001](tasks/ddd-audit-sample-001.md)
- [DDD-TEST-ORDER-SYNC-001](tasks/ddd-test-order-sync-001.md)
- [DDD-TEST-PERFORMANCE-CALC-001](tasks/ddd-test-performance-calc-001.md)
- [DDD-TEST-SAMPLE-LIFECYCLE-001](tasks/ddd-test-sample-lifecycle-001.md)
- [DDD-FACADE-USER-001](tasks/ddd-facade-user-001.md)
- [DDD-FACADE-CONFIG-001](tasks/ddd-facade-config-001.md)
- [DDD-FACADE-ORDER-001](tasks/ddd-facade-order-001.md)

## 7. 后续 Agent 使用方式

1. 先读本文件，再读总路线图和任务矩阵。
2. 只执行一个任务卡，不跨域混改。
3. 每个子任务结束后必须更新对应任务卡、领域计划和 state 页。
4. 缺真实 pick_source、结算样本或上游响应时只能写 BLOCKED / PENDING。
5. reports 是 evidence，不是长期唯一入口；长期计划以本目录为主。

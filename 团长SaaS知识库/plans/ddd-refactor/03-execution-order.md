---
kb_id: "KB-PLAN-DDD-03-ORDER"
title: "DDD 执行顺序"
domain: "harness"
category: "refactor_plan"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 15:00:00"
related_files:
  - "D:\\Projects\\SAAS\\harness\\TASK_ROUTING.md"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-audit-order-001-20260608-145000.md"
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-audit-performance-001-20260608-150000.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# DDD 执行顺序

## 第一批建议顺序

1. DDD-AUDIT-CROSS-DOMAIN-001
2. DDD-AUDIT-ORDER-001
3. DDD-AUDIT-PERFORMANCE-001
4. DDD-AUDIT-SAMPLE-001
5. DDD-TEST-ORDER-SYNC-001
6. DDD-TEST-PERFORMANCE-CALC-001
7. DDD-TEST-SAMPLE-LIFECYCLE-001
8. DDD-FACADE-USER-001
9. DDD-FACADE-CONFIG-001
10. DDD-FACADE-ORDER-001

## 为什么这个顺序优先

- 先跨域审查，避免盲改。
- 先订单 / 业绩 / 寄样，因为它们是业务闭环核心。
- 先防护测试，再重构。
- 先 Facade 收敛，再迁移包结构。
- 不允许先做大范围 package migration。

## 执行节奏

每个任务只推进一个领域、一个 use case 或一个审查维度。任务结束必须生成 evidence，更新 KB 任务页、领域页和 state 页。没有验证结果时，只能记录阶段性结论。

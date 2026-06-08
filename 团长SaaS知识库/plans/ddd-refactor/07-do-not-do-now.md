---
kb_id: "KB-PLAN-DDD-07-DONOT"
title: "当前不要做"
domain: "harness"
category: "risk_gate"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 13:59:08"
related_files:
  - "D:\\Projects\\SAAS\\harness\\FORBIDDEN_SCOPE.md"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# 当前不要做

1. 不要先做全局包结构迁移。
2. 不要先抽象所有 Repository。
3. 不要先引入复杂 CQRS 框架。
4. 不要先引入完整 Outbox。
5. 不要先做独家达人 / 独家商家。
6. 不要先做差异化提成。
7. 不要先重写 dashboard。
8. 不要先重写订单同步。
9. 不要边重构边改业务公式。
10. 不要把历史问题和 DDD 重构混在一个提交。

## 当前最不能先动

订单同步、业绩计算、寄样自动完成和 dashboard 双轨指标不能在缺少防护测试和 evidence 的情况下直接搬迁。

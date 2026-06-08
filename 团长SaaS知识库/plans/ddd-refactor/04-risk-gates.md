---
kb_id: "KB-PLAN-DDD-04-RISK"
title: "DDD 风险门禁"
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

# DDD 风险门禁

1. 禁止没有测试保护就搬逻辑。
2. 禁止同时改多个领域。
3. 禁止同时改后端、前端、数据库。
4. 禁止业务修复混入纯重构。
5. 禁止 V2 能力混入 V1 重构。
6. 禁止包结构迁移先行。
7. 禁止没有 evidence 就宣称完成。
8. 禁止改接口契约但不更新前端 / 测试。
9. 禁止改金额公式但不做 DB / API 对账。
10. 禁止改订单 / 业绩 / 寄样链路但不跑对应回归测试。

## 升级条件

涉及订单归因、业绩计算、寄样完成、dashboard 指标时，至少升级到业务链路验证。涉及真实上游或 real-pre 时，必须记录真实样本或 BLOCKED 原因。涉及数据库结构时，必须拆为 F 类数据模型任务。

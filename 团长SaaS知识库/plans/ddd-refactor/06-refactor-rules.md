---
kb_id: "KB-PLAN-DDD-06-RULES"
title: "DDD 重构规则"
domain: "harness"
category: "refactor_plan"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 13:59:08"
related_files:
  - "D:\\Projects\\SAAS\\harness\\AGENT_CONTRACT.md"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# DDD 重构规则

1. 每次只改一个领域。
2. 每次只改一个 use case。
3. 每次最多新增一个 Facade / Application Service / Policy。
4. 每次只移动一个方法族。
5. 每次必须有回滚路径。
6. 每次必须有 evidence。
7. 每次必须更新知识库。
8. 每次必须明确行为是否变化。
9. 默认行为不变。
10. 默认接口不变。
11. 默认数据库不变。

## 文件边界

A 类只读；B 类只新增或增强测试；C/D 类按任务卡列出具体允许文件；E 类一次只处理一个事件或事务边界；F 类单独 migration，不与普通重构混批。

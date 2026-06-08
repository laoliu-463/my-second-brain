---
kb_id: "governance/01-knowledge-refresh-rule"
title: "知识库刷新规则"
domain: "harness"
category: "governance"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 13:59:08"
related_files:
  - "D:\\Projects\\SAAS\\harness\\TASK_ROUTING.md"
  - "D:\\Projects\\SAAS\\harness\\AGENT_CONTRACT.md"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
forbidden_misread:
  - "reports 是 evidence，不是长期唯一入口"
  - "DDD 子任务完成后必须更新 KB"
---

# 知识库刷新规则

## 1. 总原则

外部知识库是长期可检索入口；harness/reports 是 evidence 和执行记录。后续 Agent 不能只生成 reports 而不更新知识库。

## 2. DDD 子任务刷新要求

每个 DDD 子任务完成后必须更新：

1. 对应任务卡：plans/ddd-refactor/tasks/<task-id>.md。
2. 对应领域页：plans/ddd-refactor/domains/<domain>-ddd-plan.md。
3. 任务矩阵：plans/ddd-refactor/02-task-matrix.md 中对应任务状态或 evidence。
4. 当前状态：state/00-current-state.md。
5. 领域状态：state/02-domain-status.md。

## 3. 禁止事项

- 禁止把未验证项写成 PASS。
- 禁止把 reports 当成长期唯一入口。
- 禁止把 V2 能力写成 V1 已完成。
- 禁止把业务代码变更沉淀到外部 KB 但不更新项目 docs / evidence。

## 4. 敏感信息规则

知识库只能记录字段名、环境变量名和检查项，不得记录真实 secret、token、password、cookie、private key 或 OAuth code。

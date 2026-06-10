---
kb_id: evidence/01-scripts
title: 验收脚本库
domain: evidence
category: evidence-scripts
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/scripts/*.ps1
  - harness/scripts/*.sh
  - harness/scripts/*.sql
related_reports: []
forbidden_misread:
  - 脚本必须可重复执行
  - test 与 real-pre 脚本分离
---

# 验收脚本库

## 1. 用途

承载"脚本类证据"——可重复执行的验收 / 回归脚本。

## 2. 脚本类型

| 类型 | 用途 | 入口 |
| --- | --- | --- |
| PowerShell QA | real-pre 形态 / 容器 / 接口 | harness/scripts/qa/*.ps1 |
| Playwright E2E | V1-P0 / V1-P1 | npm run e2e:v1-p0 |
| Maven 单元 / 集成 | 后端回归 | cd backend && mvn test |
| Vitest | 前端回归 | cd frontend && npm run test |
| psql / SQL | 数据库验证 | harness/scripts/sql/*.sql |

## 3. V1 P0 入口

```
npm run e2e:v1-p0              # test/mock 基线
npm run e2e:real-pre:p0        # real-pre 统一验收
npm run e2e:real-pre:p0:preflight  # real-pre 预检
```

## 4. 脚本与证据记录

- 每条脚本必须记录：入口、参数、期望输出
- 异常输出必须保留到 `harness/reports/evidence-*.md`
- last_verified_at 必须维护

## 5. 禁止

- 禁止将 mock 脚本输出当成 real-pre 证据
- 禁止删除脚本历史输出
- 禁止改写历史报告中的脚本结果

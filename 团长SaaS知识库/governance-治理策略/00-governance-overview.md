---
kb_id: governance/00-governance-overview
title: 治理与策略总览
domain: governance
category: governance-overview
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/governance/HARNESS_DEBT.md
  - docs/决策/ADR-*.md
related_reports: []
forbidden_misread:
  - 治理是 V1 一等公民
  - 治理与业务代码分离
---

# 治理与策略总览

## 1. 用途

承载 real-pre 安全 / 凭据 / 数据导出 / 域状态 / 阻塞升级 等策略。

## 2. 6 类治理文件

| 文件 | 用途 |
| --- | --- |
| governance/00-overview | 治理总览（本文件） |
| governance/01-real-pre-safety | real-pre 形态安全策略 |
| governance/02-secret-management | 凭据与密钥管理 |
| governance/03-data-export | 数据导出治理 |
| governance/04-domain-status | 域状态与阻塞升级 |
| governance/05-debt-register | DEBT 25 项治理账本 |

## 3. 与领域 / 流程的关系

```
业务域 (domains/) ──┐
业务流程 (workflows/) ──┤── 受治理约束 (governance/)
证据 (evidence/) ──┘
```

## 4. 治理与 V1

- 治理策略必须能落到"配置 / 代码 / 文档"之一
- 治理条款对应 16 条禁做
- 任何策略变更必须先 ADR，再落地

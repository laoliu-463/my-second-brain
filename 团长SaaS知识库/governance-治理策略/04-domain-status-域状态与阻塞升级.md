---
kb_id: governance/04-domain-status
title: 域状态与阻塞升级
domain: governance
category: governance-domain-status
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - domains-业务领域/00-domains-overview.md
  - evidence-证据体系/04-block-classification-BLOCK 分类.md
related_reports: []
forbidden_misread:
  - BLOCKED_BY_SAMPLE 不得升级 PASS
  - 缺真实订单时仍 PENDING
---

# 域状态与阻塞升级

## 1. 用途

约束 V1 域 / 流程的状态机与升级路径。

## 2. 状态机

```
PENDING → IN_PROGRESS → READY
                ↓
        BLOCKED_BY_SAMPLE / BLOCKED_BY_EXTERNAL
                ↓
        FAILED → RISK_ACCEPTED_BY_USER
                ↓
        PASS（需真实闭环 + 三环）
```

## 3. 升级条件

| 起点 | 终点 | 条件 |
| --- | --- | --- |
| PENDING | READY | 真实订单 / 真实样本 / 真实授权 |
| BLOCKED_BY_SAMPLE | READY | pick_source 样本就位 |
| BLOCKED_BY_EXTERNAL | READY | 上游 / 凭据 / Token 修复 |
| FAILED | RISK_ACCEPTED | 用户书面确认 |
| RISK_ACCEPTED | PASS | 仅当真实闭环 + 三环通过 |

## 4. 禁止

- 禁止把 BLOCKED_BY_SAMPLE 升级 PASS
- 禁止把 BLOCKED_BY_EXTERNAL 升级 PASS
- 禁止把"容器 healthy"升级 PASS
- 禁止把"anti-join=0"升级"结算轨完成"

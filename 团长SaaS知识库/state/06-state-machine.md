---
kb_id: state/06-state-machine
title: 状态机与流转规则
domain: state
category: state-machine
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/CURRENT_STATE.md
  - harness/DOMAIN_STATUS.md
related_reports: []
forbidden_misread:
  - 状态机是单向迁移，跨级必须经 ADR
  - 不得从 FAILED 直接跳 PASS
---

# 状态机与流转规则

## 1. 主状态机

```
NOT_STARTED
  → IN_PROGRESS
    → BLOCKED_BY_SAMPLE
    → BLOCKED_BY_EXTERNAL
    → FAILED
    → RISK_ACCEPTED
    → PASS
      → PENDING (后续发现)
```

## 2. 域级状态机

```
PASS → PENDING（已通过但有未结 P0 样本）
PASS → BLOCKED_BY_SAMPLE（样本撤销）
PENDING → BLOCKED_BY_SAMPLE
PENDING → FAILED
FAILED → PASS（修复 + 验收 + ADR）
FAILED → RISK_ACCEPTED（用户接受）
```

## 3. 错误流转（禁止）

- FAILED → PASS（无 ADR）
- BLOCKED_BY_SAMPLE → PASS（无样本）
- NOT_STARTED → PASS（无过程）

## 4. 状态触发与登记

| 流转 | 触发 | 登记 |
| --- | --- | --- |
| NOT_STARTED → IN_PROGRESS | 任务启动 | 任务记录 |
| → PASS | 验收通过 | evidence + CURRENT_STATE |
| → PENDING | 缺样本 | 样本登记 |
| → BLOCKED_BY_* | 客观阻塞 | 阻塞详情 |
| → FAILED | 验收失败 | 失败详情 + 修复计划 |
| → RISK_ACCEPTED | 用户接受 | 用户确认记录 |

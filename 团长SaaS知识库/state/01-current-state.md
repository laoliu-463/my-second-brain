---
kb_id: state/01-current-state
title: CURRENT_STATE 主源
domain: state
category: state-current
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/CURRENT_STATE.md
related_reports: []
forbidden_misread:
  - 不得在 CURRENT_STATE 中"美化"或"漏报"失败
  - 不得删除历史部署结论
---

# CURRENT_STATE 主源

## 1. 用途

记录"项目当前事实"——上一部署结论、运行形态、技术栈版本、最近变更。

## 2. 必含章节

- 项目概览
- 当前形态（test / real-pre）
- 最近部署结论
- 进行中的工作
- 待办/阻塞
- 风险

## 3. 写入时机

- 任务完成并验收后
- 部署（含 preflight / 落地）
- 状态发生重大变化（如 P0 PASS / FAILED）

## 4. 写入格式

```markdown
## YYYY-MM-DD HH:MM <task-id>
- 形态: real-pre
- 部署版本: <commit>
- preflight: PASS / FAIL
- 容器 healthy: ✅ / ❌
- 三环: PASS / PENDING / BLOCKED_*
- 双轨: PASS / PENDING
- 证据: harness/reports/evidence-*.md
- 结论: PASS / PENDING / BLOCKED_* / FAILED / RISK_ACCEPTED
- 备注: <关键观察>
```

## 5. 不得写入

- 推测 / 计划 / 期望
- 未验证的"健康"
- secret / token

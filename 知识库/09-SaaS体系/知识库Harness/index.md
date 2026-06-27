---
title: "知识库Harness"
type: index
status: active
created_at: 2026-06-27
updated_at: 2026-06-27
source_level: none
sources: []
raw_evidence: []
related: []
tags: []
maintainers:
  - codex
confidence: 0.5
---
# 知识库Harness

> 知识库自身运维 Harness——任务路由、完成门禁、Session 退出检查、GC 政策

## 核心文件

| 文件 | 说明 |
|------|------|
| [[AGENT_CONTRACT]] | 知识库管理合同：3条核心原则 + DoD 定义 |
| [[TASK_ROUTING]] | P0/P1/P2 任务路由矩阵 |
| [[COMPLETION_GATES]] | 各任务类型完成门禁 |
| [[SESSION_EXIT_GATE]] | 会话退出检查清单 |
| [[FORBIDDEN_SCOPE]] | 禁止操作范围 |

## Skills

| Skill | 触发条件 |
|-------|---------|
| [[skills/kb-audit]] | 每次任务完成后的 LINT 巡检 |
| [[skills/kb-organize]] | 已入库内容整理、原文归档、来源页与知识页沉淀 |
| [[skills/kb-gc]] | 定期 GC 政策执行 |
| [[skills/kb-session-exit]] | Session 退出前检查 |

## State

| 文件 | 内容 |
|------|------|
| [[state/KB_STATUS]] | 知识库当前状态快照 |
| [[state/KB_TASK_MATRIX]] | 任务矩阵与优先级 |

## 使用说明

1. **P0 任务**（stub/孤立/断链）：直接执行，完成后必 audit
2. **P1 任务**（整理/归档）：按 kb-organize 执行，完成后更新 KB_STATUS
3. **P2 任务**（优化/重构）：按 COMPLETION_GATES P2 节验证
4. **每次会话结束**：执行 SESSION_EXIT_GATE 检查清单

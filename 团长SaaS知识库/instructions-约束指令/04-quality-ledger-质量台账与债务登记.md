---
kb_id: instructions/04-quality-ledger
title: 质量台账与债务登记
domain: instructions
category: quality
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/HARNESS_DEBT.md
  - harness/HARNESS_CHANGELOG.md
related_reports:
  - harness/reports/git-harness-001-worktree-governance-20260603-*.md
  - harness/reports/user-domain-u2_5b-dept-type-minimal-fix-20260603-101503.md
forbidden_misread:
  - 债务项不得"装订"成已完成；OWNER 才可登记收口
---

# 质量台账与债务登记

## 1. 目的

登记 Harness 范围内所有已知债务、技术短板、未决议题、阻塞项、待 Owner 拍板项的最小治理登记。任何 Agent 在新任务开始前必须先扫一眼本台账。

## 2. 主源

- `harness/HARNESS_DEBT.md`（25 项债务治理注册表）

## 3. 债务类型

| 类型 | 含义 | 处理优先级 |
| --- | --- | --- |
| `BLOCKER` | 阻塞 V1 P0 验收 | P0 |
| `MAJOR` | 影响 P0 验收口径 | P1 |
| `MINOR` | 影响可维护性 / 文档一致性 | P2 |
| `NIT` | 命名 / 风格 | P3 |
| `RISK` | 已知风险，需 Owner 接受 | 按 Owner 拍板 |

## 4. 登记规则

每条债务必须包含：

| 字段 | 含义 |
| --- | --- |
| `id` | 唯一 ID（DEBT-NNN） |
| `title` | 标题 |
| `type` | BLOCKER / MAJOR / MINOR / NIT / RISK |
| `owner` | 负责人 |
| `created_at` | 登记日期 |
| `due_at` | 计划收口日期（按业务节奏） |
| `evidence` | 入口路径 / URL |
| `related_adr` | 关联 ADR（如有） |
| `status` | OPEN / IN_PROGRESS / CLOSED / ACCEPTED |
| `closed_at` | 收口日期（仅 CLOSED） |
| `close_evidence` | 收口证据（仅 CLOSED） |

## 5. 典型债务（V1 已知）

| id | title | type | status | 入口 |
| --- | --- | --- | --- | --- |
| DEBT-001 | real-pre 缺真实订单样本 | BLOCKER | OPEN | `docs/验收/real-pre联调手册.md` |
| DEBT-002 | 渠道归因缺真实 pick_source 样本 | BLOCKER | OPEN | `docs/验收/real-pre联调手册.md` |
| DEBT-003 | 寄样自动完成缺成交订单触发 | BLOCKER | OPEN | `docs/验收/real-pre联调手册.md` |
| DEBT-004 | 业绩计算缺真实订单或金额字段 | BLOCKER | OPEN | `docs/验收/real-pre联调手册.md` |
| DEBT-005 | V2.2 旧方案文档残留 | MINOR | OPEN | `docs/归档/` |
| … | … | … | … | `harness/HARNESS_DEBT.md` |

## 6. 收口规则

- 收口必须有 `close_evidence`（脚本 / API / SQL / 文档路径之一）。
- 收口必须更新 `harness/HARNESS_CHANGELOG.md`。
- Agent 不得自行关闭 `BLOCKER` / `MAJOR`，必须升级 Owner。

## 7. 与门禁的关系

- G2（自测 / 构建）失败 → 必登 1 条 MINOR 及以上债务
- G3（真实上游）失败 → 必登 1 条 BLOCKER
- G4（证据）失败 → 必登 1 条 MAJOR

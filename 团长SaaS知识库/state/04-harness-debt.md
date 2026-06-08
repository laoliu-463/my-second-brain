---
kb_id: state/04-harness-debt
title: HARNESS_DEBT 主源
domain: state
category: state-debt
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/HARNESS_DEBT.md
related_reports: []
forbidden_misread:
  - 不得"漏报"已知风险
  - 不得"已修复"实际未验证
---

# HARNESS_DEBT 主源

## 1. 用途

登记项目技术债 / 已知风险 / 待优化项。

## 2. 25 项分类

| 类别 | 项数 |
| --- | --- |
| 死代码 | 5 |
| 重复代码 | 3 |
| 临时方案 | 4 |
| 文档缺失 | 3 |
| 测试不足 | 3 |
| 安全 | 2 |
| 性能 | 2 |
| 可观测性 | 2 |
| 验收盲区 | 1 |

## 3. 字段

- ID: DEBT-NNN
- 标题
- 类别
- 状态: OPEN / ACCEPTED / FIXED / WONTFIX
- 优先级: P0 / P1 / P2
- 引入时间
- 影响范围
- 关联证据

## 4. 状态变更

| 状态 | 触发 |
| --- | --- |
| OPEN → FIXED | 修复 + 验收 + ADR |
| OPEN → ACCEPTED | 用户接受 |
| OPEN → WONTFIX | 永久放弃（须 ADR） |
| FIXED → OPEN | 回归 |

## 5. 与验收的关系

- FIXED 必须有 evidence
- ACCEPTED 必须有用户确认
- WONTFIX 必须有 ADR

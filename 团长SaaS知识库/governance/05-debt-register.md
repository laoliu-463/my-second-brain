---
kb_id: governance/05-debt-register
title: DEBT 治理账本
domain: governance
category: governance-debt
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
  - DEBT 不是 V1 必做
  - 任何 DEBT 项必须经 ADR 审批
---

# DEBT 治理账本

## 1. 用途

记录 V1 阶段被显式延后 / 接受的技术债与流程债。

## 2. DEBT 来源

- V2.2 旧方案暂未实现项
- 真实环境依赖项（pick_source / 真实订单 / 上游授权）
- 治理事件（如 SECURITY-INCIDENT-001）

## 3. 25 项分布（高层分类）

| 分类 | 数量级 | 备注 |
| --- | --- | --- |
| 业务功能 V2.2 | ~10 | 独家达人 / 商家 / 高级看板 / 差异化提成 |
| 真实环境依赖 | ~5 | 真实订单 / 真实物流 / pick_source |
| 工程化债 | ~5 | MQ 化 / 外部 quick_sample_apply / 重算 |
| 治理与安全 | ~3 | 凭据轮换 / 审计扩展 |
| 文档债 | ~2 | 旧 V2.2 迁移 / 决策追溯 |

## 4. 状态字段

每条 DEBT 含：
- 编号 / 标题 / 分类
- 严重度（P0-P3）
- 起源 / 影响范围
- 解决路径 / 解封条件
- 当前负责人

## 5. 治理

- 任何 DEBT 解封需 ADR
- P0 DEBT 必须有 owner
- 季度复盘：是否可关闭 / 是否可降级

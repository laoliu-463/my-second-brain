---
kb_id: domains/08-analysis-domain
title: 分析域
domain: domains
category: domain-analysis
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/领域/分析域.md
  - frontend/src/views/Dashboard.vue
related_reports: []
forbidden_misread:
  - 分析模块只读汇总表，不重算业绩归属
  - V1 不做高级看板
---

# 分析域（analysis）

## 1. 用途

提供业务看板，**只读汇总表，不重算业绩归属**。

## 2. V1 必做

- 订单量趋势
- GMV 趋势
- 服务费收入汇总
- 双轨金额对比
- 部门业绩排行
- 达人/商品业绩排行（基础）

## 3. V1 不做（V2 预留）

- 高级看板
- 实时分析
- 自定义维度
- 看板分享
- 数据导出（CSV/Excel）→ 见 governance/02 数据导出

## 4. 关键 API

| API | 用途 |
| --- | --- |
| `GET /api/analysis/dashboard` | 看板汇总 |
| `GET /api/analysis/trend?metric=gmv` | 趋势 |
| `GET /api/analysis/ranking?dim=department` | 排行 |

## 5. 关键实体（只读视图）

- `V_DashboardSummary`：日 / 周 / 月维度
- `V_PerformanceRanking`：按维度排行

## 6. 验收口径

- 看板数据与业绩表汇总一致
- 性能：单页加载 < 2s
- 部门/用户数据范围生效

## 7. 不变量

> [V1 必做] 分析模块只读汇总表，不重算业绩归属。

任何在分析模块"重新计算"业绩归属 / 提成的尝试都是 V1 禁做。

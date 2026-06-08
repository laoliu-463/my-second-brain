---
kb_id: workflows/07-dashboard-readonly
title: 看板只读流程
domain: workflows
category: workflow-dashboard
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/流程/看板.md
  - frontend/src/views/Dashboard.vue
related_reports: []
forbidden_misread:
  - 看板只读，不重算业绩
  - V1 不做高级看板
---

# 看板只读流程

## 1. 用途

通过汇总表查询业务数据，**不重算业绩归属**。

## 2. 流程节点

```
[用户请求] → 数据范围解析（self/group/all）→ 汇总表查询 → 返回结果
```

## 3. 看板内容

- 订单量趋势（日 / 周 / 月）
- GMV 趋势
- 服务费收入汇总
- 双轨金额对比
- 部门业绩排行
- 达人/商品业绩排行（基础）

## 4. 关键 API

- `GET /api/analysis/dashboard`
- `GET /api/analysis/trend?metric={gmv|orders|service_fee}`
- `GET /api/analysis/ranking?dim={department|user|talent|product}`

## 5. 验收口径

- 看板数据与业绩表汇总一致
- 数据范围生效（self/group/all）
- 性能：单页 < 2s

## 6. 阻塞条件

- 汇总表与业绩表不一致 → FAILED
- 数据范围失效 → FAILED

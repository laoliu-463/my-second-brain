---
kb_id: workflows/02-recruiter-chain
title: 招商链流程
domain: workflows
category: workflow-recruiter
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/流程/招商链.md
  - docs/04-事件契约总表.md
related_reports: []
forbidden_misread:
  - 招商归因 = default_recruiter（V1）
  - 不做独家招商
---

# 招商链流程

## 1. 用途

招商人员对接商家 → 商家订单产生 → 业绩归因到招商 → 招商提成计算。

## 2. 流程节点

```
[商家] → 招商对接（建立商家-招商关系） → 商家产生订单
                                              ↓
                                       订单同步（6468 / 2704）
                                              ↓
                              业绩域：final_recruiter = default_recruiter
                                              ↓
                              招商提成 = 订单额 × 招商提成率
```

## 3. 关键实体

- `MerchantRecruiterMapping`：merchant_id, recruiter_id, bound_at
- 订单 `final_recruiter` 字段

## 4. 关键 API

- `POST /api/recruiters/{id}/merchants`
- `GET /api/orders?recruiter_id={id}`
- `GET /api/performance/summary?dim=recruiter`

## 5. 验收口径

- 商家-招商绑定存在
- 订单 `final_recruiter` 与绑定关系一致
- 招商提成 = 订单额 × 招商提成率

## 6. 阻塞条件

- 商家-招商绑定缺失 → FAILED
- 订单-业绩 anti-join ≠ 0 → FAILED

---
kb_id: workflows/01-channel-chain
title: 渠道链流程
domain: workflows
category: workflow-channel
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/流程/渠道链.md
  - docs/04-事件契约总表.md
related_reports: []
forbidden_misread:
  - 渠道归因 = default_channel（V1）
  - 缺 pick_source 样本 → 归因闭环 BLOCKED_BY_SAMPLE
---

# 渠道链流程

## 1. 用途

渠道方产生的订单 → 业绩归因到渠道 → 渠道提成计算。

## 2. 流程节点

```
[渠道] → 转链（带 pick_source） → 推广链接
                                         ↓
                                     订单生成
                                         ↓
                              订单同步（6468）
                                         ↓
                              业绩域：final_channel = default_channel
                                         ↓
                              渠道提成 = 订单额 × 渠道提成率
```

## 3. 关键事件

| 事件 | 来源 | 消费者 |
| --- | --- | --- |
| `product.converted` | product 域 | 渠道方 |
| `order.synced` | order 域 | performance 域 |
| `performance.calculated` | performance 域 | analysis 域 |

## 4. 关键 API

- `POST /api/products/convert` （带 pick_source）
- `GET /api/orders?pick_source={src}`
- `GET /api/performance/summary?dim=channel`

## 5. 验收口径

- 转链成功 + `pick_source_mapping` 落库
- 订单有 `pick_source` 字段
- 业绩 `final_channel` 与订单 `pick_source` 一致
- 渠道提成 = 订单额 × 渠道提成率

## 6. 阻塞条件

| 现象 | 结论 |
| --- | --- |
| 无 pick_source 样本 | BLOCKED_BY_SAMPLE |
| 上游不可达 | BLOCKED_BY_EXTERNAL |
| 转链失败 | FAILED |
| 归因不一致 | FAILED |

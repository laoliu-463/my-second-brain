---
kb_id: workflows/04-order-sync
title: 订单同步流程
domain: workflows
category: workflow-order-sync
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/流程/订单同步.md
  - backend/src/main/java/com/colonel/saas/service/OrderSyncService.java
related_reports: []
forbidden_misread:
  - 6468 = 团长订单，2704 = 团长结算订单
  - 缺真实订单 → P0 仍 PENDING
---

# 订单同步流程

## 1. 用途

将外部订单源（6468 / 2704）数据同步到本地订单域。

## 2. 流程节点

```
[外部订单源] → 拉取（定时 T+1） → 校验 → 写入 order 表 → 发布 order.synced 事件
                                                                       ↓
                                                              寄样域 + 业绩域
```

## 3. 两源差异

| 源 | 名称 | 用途 | 金额含义 |
| --- | --- | --- | --- |
| 6468 | 团长订单 | 实际发生 | 订单额 |
| 2704 | 团长结算订单 | 结算依据 | 结算额 |

## 4. 关键 API / 任务

- `POST /api/orders/sync` （admin 手动触发）
- 定时任务 `OrderSyncJob`（T+1 03:00）

## 5. 验收口径

- 两源同步成功率 = 100%（有真实订单时）
- 失败订单可重试
- 重复订单幂等
- `order.synced` 事件正确发布

## 6. 阻塞条件

| 现象 | 结论 |
| --- | --- |
| 无真实订单 | PENDING |
| 上游不可达 | BLOCKED_BY_EXTERNAL |
| 同步失败 | FAILED |

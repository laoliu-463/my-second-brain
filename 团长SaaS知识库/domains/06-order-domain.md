---
kb_id: domains/06-order-domain
title: 订单域
domain: domains
category: domain-order
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/领域/订单域.md
  - backend/src/main/java/com/colonel/saas/service/OrderService.java
  - backend/src/main/java/com/colonel/saas/service/OrderSyncService.java
related_reports: []
forbidden_misread:
  - 订单域只存事实，不算提成
  - 不应用独家覆盖
  - 6468 是团长订单源，2704 是团长结算订单源
---

# 订单域（order）

## 1. 用途

存储订单事实数据，提供同步、查询、归因（只读取，不计算）能力。

## 2. V1 必做

### 2.1 订单源

| 源 ID | 名称 | 类型 | 频率 |
| --- | --- | --- | --- |
| 6468 | 团长订单 | INSTITUTE | T+1 |
| 2704 | 团长结算订单 | SETTLEMENT | T+1 |

### 2.2 订单事实字段

- `order_id`、`external_order_id`、`source`（6468/2704）
- `talent_id`、`product_id`、`pick_source`
- `amount`（订单额）、`status`、 `order_time`、`sync_time`
- `final_channel`（V1 = `default_channel`）、`final_recruiter`（V1 = `default_recruiter`）

### 2.3 同步事件

- `order.synced`（订单已同步）→ 寄样域消费
- `order.settled`（订单已结算）→ 业绩域消费

## 3. V1 不做（V2 预留）

- 实时对账
- 独家达人 / 独家商家覆盖归因
- 订单状态回写
- 退款逆向

## 4. 关键 API

| API | 用途 |
| --- | --- |
| `GET /api/orders` | 列表（带数据范围） |
| `GET /api/orders/{id}` | 详情 |
| `POST /api/orders/sync` | 手动触发同步（admin） |
| `GET /api/orders/anti-join` | 订单-业绩 anti-join（验收用） |

## 5. 关键实体

- `Order`：order_id, external_order_id, source, talent_id, product_id, pick_source, amount, status, order_time, sync_time
- `OrderEvent`：order_id, event_type, occurred_at

## 6. 验收口径

- 6468 + 2704 两源同步成功率 = 100%（有真实订单时）
- 订单-业绩 anti-join = 0（无遗漏）
- pick_source 落库率 = 100%
- 订单已同步事件正确发布

## 7. 不变量

> [V1 必做] 订单域只存事实，不算提成，不应用独家覆盖。

任何"在订单域计算金额"或"在订单域应用独家归因"的尝试都是 V1 禁做。

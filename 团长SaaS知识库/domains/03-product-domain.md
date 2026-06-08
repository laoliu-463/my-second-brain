---
kb_id: domains/03-product-domain
title: 商品域
domain: domains
category: domain-product
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/领域/商品域.md
  - backend/src/main/java/com/colonel/saas/service/ProductService.java
related_reports: []
forbidden_misread:
  - V1 不做商品全量同步
  - pick_source_mapping 必须落库
---

# 商品域（product）

## 1. 用途

管理商品档案并提供"转链"能力，将外部商品链接转换为平台可用的推广链接，同时记录 `pick_source`（渠道来源）。

## 2. V1 必做

- 商品档案：name, sku, price, image, status
- 转链 API：外部链接 → 平台推广链接
- `pick_source_mapping` 落库（**强制**）
- 商品状态：在线 / 停售
- 基础检索

## 3. V1 不做

- 商品全量同步
- 商品分类管理
- 库存管理
- 跨平台铺货

## 4. 关键 API

| API | 用途 |
| --- | --- |
| `GET /api/products` | 商品列表 |
| `GET /api/products/{id}` | 详情 |
| `POST /api/products/convert` | 转链（入参：external_url, pick_source） |

## 5. 关键实体

- `Product`：product_id, name, sku, price, status
- `PickSourceMapping`：mapping_id, external_url, platform_url, pick_source, created_at

## 6. 验收口径

- 转链成功 + `pick_source_mapping` 记录存在
- 转链失败不产生脏数据
- pick_source 用于渠道归因（订单域消费）

## 7. 不变量

> [V1 必做] 商品域负责转链并落 `pick_source_mapping`。

订单域消费 `pick_source_mapping` 进行渠道归因。无样本 → 渠道归因 BLOCKED_BY_SAMPLE。

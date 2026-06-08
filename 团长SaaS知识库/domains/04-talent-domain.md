---
kb_id: domains/04-talent-domain
title: 达人域
domain: domains
category: domain-talent
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/领域/达人域.md
  - backend/src/main/java/com/colonel/saas/service/TalentService.java
related_reports: []
forbidden_misread:
  - V1 不做独家达人
  - 达人域不参与订单归因
---

# 达人域（talent）

## 1. 用途

管理达人基础档案与商品绑定关系，**不参与订单归因**——归因由订单域 + 业绩域 + pick_source 共同决定。

## 2. V1 必做

- 达人基础档案：talent_id, name, platform, follower_count, contact
- 达人-商品绑定：多对多
- 达人状态：在职 / 离职 / 黑名单

## 3. V1 不做（V2 预留）

- 独家达人
- 达人画像 / 标签系统
- 业绩归属权重
- 跨平台达人聚合

## 4. 关键 API

| API | 用途 |
| --- | --- |
| `GET /api/talents` | 达人列表 |
| `GET /api/talents/{id}` | 详情 |
| `POST /api/talents/{id}/products` | 绑定商品 |

## 5. 关键实体

- `Talent`：talent_id, name, platform, follower_count, contact, status
- `TalentProduct`：talent_id, product_id, bound_at

## 6. 验收口径

- 达人基础档案可查
- 商品绑定关系正确

## 7. 不变量

> 达人域不参与订单归因。

订单归因 = `default_channel` + `default_recruiter`（V1 默认归因口径），不读达人信息。

---
kb_id: domains/05-sample-domain
title: 寄样域
domain: domains
category: domain-sample
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/领域/寄样域.md
  - backend/src/main/java/com/colonel/saas/service/SampleService.java
related_reports: []
forbidden_misread:
  - V1 不做真实物流自动化
  - 寄样完成由订单已同步事件触发
---

# 寄样域（sample）

## 1. 用途

管理"寄样"流程——商家向达人寄送商品样品，达人完成"交作业"（发布推广内容）。

## 2. V1 必做

- 寄样申请：talent_id, product_id, applicant_id
- 寄样状态：PENDING / SHIPPED / DELIVERED / SUBMITTED / CLOSED
- **交作业完成判定：消费"订单已同步"事件**
- 寄样记录可查

## 3. V1 不做（V2 预留）

- 真实物流自动化
- 物流轨迹回传
- 寄样成本核算

## 4. 关键 API

| API | 用途 |
| --- | --- |
| `POST /api/samples` | 创建寄样申请 |
| `GET /api/samples` | 列表 |
| `PUT /api/samples/{id}/ship` | 标记已发货 |
| `PUT /api/samples/{id}/deliver` | 标记已签收 |
| **事件消费** | 订单已同步 → 自动 CLOSED |

## 5. 关键实体

- `Sample`：sample_id, talent_id, product_id, applicant_id, status, applied_at, shipped_at, delivered_at, closed_at
- `SampleEvent`：sample_id, event_type, event_source, occurred_at

## 6. 验收口径

- 寄样状态机可流转
- **订单已同步事件触发后，对应寄样自动 CLOSED**（关键）
- 事件幂等（重复事件不重复关闭）

## 7. 不变量

> [V1 必做] 寄样域通过订单已同步事件判断交作业完成。

无订单已同步事件 → 寄样不能 CLOSED → 寄样域 PENDING。

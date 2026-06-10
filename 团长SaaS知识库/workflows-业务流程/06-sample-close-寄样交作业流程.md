---
kb_id: workflows/06-sample-close
title: 寄样交作业流程
domain: workflows
category: workflow-sample-close
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/流程/寄样.md
  - backend/src/main/java/com/colonel/saas/service/SampleService.java
related_reports: []
forbidden_misread:
  - 寄样 CLOSED = 订单已同步事件触发
  - V1 不做真实物流自动化
---

# 寄样交作业流程

## 1. 用途

达人收到样品并完成推广内容发布后，关闭寄样单。**关闭由订单已同步事件触发**。

## 2. 流程节点

```
[创建寄样] → PENDING → 发货 → SHIPPED → 签收 → DELIVERED
                                                       ↓
                                              订单已同步事件
                                                       ↓
                                                  CLOSED
```

## 3. 事件消费

- 来源：`order.synced` 事件
- 条件：订单的 talent_id + product_id 与寄样单匹配
- 动作：寄样单 status = CLOSED，记录 `closed_at` 和 `closed_by_event`

## 4. 验收口径

- 事件消费幂等
- 寄样 CLOSED 率 = 100%（有匹配订单时）
- 事件缺失时寄样保持 DELIVERED（PENDING）

## 5. 阻塞条件

| 现象 | 结论 |
| --- | --- |
| 订单已同步事件未发布 | PENDING |
| 上游无订单 | PENDING |
| 事件重复 | 幂等（PASS） |

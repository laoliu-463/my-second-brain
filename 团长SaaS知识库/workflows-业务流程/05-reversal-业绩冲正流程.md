---
kb_id: workflows/05-reversal
title: 业绩冲正流程
domain: workflows
category: workflow-reversal
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/流程/冲正.md
  - backend/src/main/java/com/colonel/saas/service/PerformanceReverseService.java
related_reports: []
forbidden_misread:
  - 冲正 = 退款 / 退单的业绩回退
  - 不得直接删除业绩记录
---

# 业绩冲正流程

## 1. 用途

处理退款 / 退单导致的业绩回退，**通过冲正记录实现，不得直接删除业绩记录**。

## 2. 流程节点

```
[退款 / 退单] → 创建冲正单 → 计算冲正金额 → 写 performance_reverse 表
                                                          ↓
                                                业绩汇总扣减冲正金额
```

## 3. 关键实体

- `PerformanceReverse`：reverse_id, original_order_id, reason, amount, operator, ts

## 4. 关键 API

- `POST /api/performance/reverse` （admin / biz_leader）
- `GET /api/performance/reverses?order_id={id}`

## 5. 验收口径

- 冲正记录可追溯
- 业绩汇总 = 单订单业绩求和 - 冲正金额求和
- 冲正参与下次结算

## 6. 阻塞条件

- 冲正金额 ≠ 退款金额 → FAILED
- 重复冲正 → FAILED

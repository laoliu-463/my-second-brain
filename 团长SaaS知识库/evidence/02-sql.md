---
kb_id: evidence/02-sql
title: 关键 SQL 证据
domain: evidence
category: evidence-sql
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/scripts/sql/*.sql
  - docs/06-数据模型总表.md
related_reports: []
forbidden_misread:
  - SQL 不得修改生产数据
  - 关键 SQL 必须只读
---

# 关键 SQL 证据

## 1. 用途

通过 SQL 查询 / 比对，对数据完整性、归因、双轨、冲正等做证据化验证。

## 2. 必查关键 SQL

### 2.1 订单与业绩 anti-join

```sql
-- 订单表与业绩表 anti-join
SELECT o.order_id FROM orders o
LEFT JOIN performance_summary p ON p.order_id = o.order_id
WHERE p.order_id IS NULL;
-- 期望：0（仅作"结算轨就位"前提，不等于"结算轨完成"）
```

### 2.2 双轨金额合计

```sql
-- 预估轨合计
SELECT SUM(estimated_amount) FROM performance_summary
WHERE track_type = 'ESTIMATE';

-- 结算轨合计
SELECT SUM(settlement_amount) FROM performance_summary
WHERE track_type = 'SETTLEMENT';
```

### 2.3 冲正一致性

```sql
-- 冲正金额合计
SELECT original_order_id, SUM(reverse_amount)
FROM performance_reverse GROUP BY original_order_id;
```

## 3. 验收口径

- SQL 全部 SELECT，不写数据
- 必须记录执行时间、连接信息
- 异常结果需有 `harness/reports/evidence-*.md` 解释

## 4. 阻塞

- 涉及 UPDATE/DELETE 一律 FAILED
- 缺数据时，结论写 PENDING，不写 PASS

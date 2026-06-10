---
kb_id: domains/07-performance-domain
title: 业绩域
domain: domains
category: domain-performance
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/领域/业绩域.md
  - backend/src/main/java/com/colonel/saas/service/PerformanceCalculationService.java
related_reports: []
forbidden_misread:
  - 业绩域负责最终归属、提成、冲正、双轨金额
  - V1 不做差异化提成
---

# 业绩域（performance）

## 1. 用途

**最终归属、提成、冲正、双轨金额**——所有"算钱"的地方都在本域。

## 2. V1 必做

### 2.1 三链归属

| 链 | 字段 | V1 默认值 |
| --- | --- | --- |
| 渠道链 | `final_channel` | `default_channel` |
| 招商链 | `final_recruiter` | `default_recruiter` |
| 管理链 | `admin_dept_id` | 部门树回溯 |

### 2.2 双轨金额（2026-06-06 服务费公式）

**预估轨（estimate）**：
- 预估服务费收入 = 预估订单额 × 服务费率
- 预估服务费收益 = 预估服务费收入 - 预估服务费支出 - 技术服务费

**结算轨（settlement，源 2704）**：
- 结算服务费收入 = 结算订单额 × 服务费率 - 技术服务费
- 结算服务费收益 = 结算服务费收入 - 结算服务费支出

**毛利**：
- 毛利 = 服务费收益 - 招商提成 - 媒介/渠道提成

### 2.3 冲正

- 退款 / 退单 → 冲正记录
- 冲正参与下次结算

## 3. V1 不做（V2 预留）

- 差异化提成（按达人/商家/品类）
- 完整重算（业绩重新归属）
- 实时业绩看板
- 跨部门业绩互斥

## 4. 关键 API

| API | 用途 |
| --- | --- |
| `GET /api/performance/orders/{id}` | 单订单业绩 |
| `GET /api/performance/summary` | 汇总（按部门/用户/时间） |
| `GET /api/performance/dual-track` | 双轨对比 |
| `POST /api/performance/reverse` | 冲正 |

## 5. 关键实体

- `PerformanceOrder`：order_id, final_channel, final_recruiter, admin_dept_id, estimate_amount, settlement_amount
- `PerformanceDualTrack`：order_id, track_type, service_fee_income, service_fee_expense, tech_service_fee, gross_profit
- `PerformanceReverse`：reverse_id, original_order_id, reason, amount, operator, ts

## 6. 验收口径

- 三链归属一致性（每订单归属唯一）
- 双轨金额公式可验证
- 冲正链路完整（冲正记录 + 业绩表）
- 订单-业绩 anti-join = 0

## 7. 不变量

> [V1 必做] 业绩域负责最终归属、提成、冲正、双轨金额计算。

订单域 / 商品域 / 达人域都不算钱。

## 8. 审查发现 (DDD-AUDIT-PERFORMANCE-001)
- **事件消费**: 业绩域通过 `PerformanceRecordSyncListener` 异步消费 `OrderSyncedEvent`。已确定发布时机改为 `afterCommit`，保证了异步查询订单时的数据一致性。
- **公式规则**: 预估服务费收益、结算服务费收益与毛利的双轨公式由 `CommissionService` 严格计算，媒介/渠道提成与招募者提成已计算入账。
- **配置跨域**: `CommissionService` 中使用 `jdbcTemplate` 直接对配置表 `system_config` 进行 Mapper/SQL 级直接越界查询，属于耦合架构问题，建议后续通过 `ConfigDomainFacade` 进行接口防腐收敛。
- **数据范围**: 使用 `PerformanceAccessScope` 控制 `ALL/DEPT/PERSONAL` 数据权限，下沉至 SQL。


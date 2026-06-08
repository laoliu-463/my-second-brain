---
kb_id: "KB-PLAN-DDD-PHASE-1"
title: "Phase 1 防护测试"
domain: "harness"
category: "testing_strategy"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 13:59:08"
related_files:
  - "D:\\Projects\\SAAS\\harness\\TASK_ROUTING.md"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# Phase 1：防护测试

## 阶段目标

先锁定订单、业绩、寄样、商品、用户、配置、Dashboard 的现有行为。

## 阶段非目标

不改变业务口径，不改变接口契约，不改变数据库结构，不把规划写成完成。

## 进入条件

Phase 0 风险清单明确。

## 退出条件

关键 use case 有 targeted tests 或缺口登记。

## 允许任务类型

B

## 禁止事项

禁止改生产逻辑、禁止顺手修 bug。

## 推荐任务

- DDD-TEST-USER-DATASCOPE-001：补数据范围测试
- DDD-TEST-CONFIG-CACHE-001：补配置缓存测试
- DDD-TEST-PRODUCT-DISPLAY-001：补商品展示规则测试
- DDD-TEST-TALENT-CLAIM-001：补认领保护期测试
- DDD-TEST-SAMPLE-LIFECYCLE-001：补寄样状态机测试
- DDD-TEST-ORDER-SYNC-001：补订单同步测试
- DDD-TEST-ORDER-ATTRIBUTION-001：补归因测试
- DDD-TEST-PERFORMANCE-CALC-001：补业绩计算测试
- DDD-TEST-PERFORMANCE-REVERSAL-001：补退款冲正测试
- DDD-TEST-DASHBOARD-RECON-001：补 dashboard 对账测试

## 验证方式

按任务卡执行 targeted verification；docs-only 只读任务至少执行 git 状态、diff check、误改范围检查和 evidence 落盘。

## 相关领域

用户、配置、商品、达人、寄样、订单、业绩、分析、跨域事件。

## 风险

如果跳过本阶段，后续重构会在缺少行为锁定的情况下移动核心链路，无法区分重构引入回归还是原有缺陷。

---
kb_id: "KB-PLAN-DDD-PHASE-3"
title: "Phase 3 Application Service 分层"
domain: "harness"
category: "refactor_plan"
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

# Phase 3：Application Service 分层

## 阶段目标

将 Controller 编排和外部 API 编排逐 use case 下沉到应用服务。

## 阶段非目标

不改变业务口径，不改变接口契约，不改变数据库结构，不把规划写成完成。

## 进入条件

Facade 或边界缺口已明确。

## 退出条件

一个 use case 的编排位置清晰，Controller 入参出参不变。

## 允许任务类型

C/D

## 禁止事项

禁止同时改多个领域或前后端联动改契约。

## 推荐任务

- DDD-APP-USER-SCOPE-001：整理用户应用服务
- DDD-APP-PRODUCT-DISPLAY-001：整理 ProductSyncApplicationService
- DDD-APP-PROMOTION-LINK-001：整理 PromotionLinkApplicationService
- DDD-APP-TALENT-001：整理达人应用服务
- DDD-POLICY-SAMPLE-APPLY-001：提取 SampleApplyPolicy
- DDD-APP-SAMPLE-LIFECYCLE-001：整理 SampleLifecycleApplicationService
- DDD-APP-ORDER-SYNC-001：整理 OrderSyncApplicationService
- DDD-APP-PERFORMANCE-CALC-001：整理 PerformanceApplicationService
- DDD-APP-DASHBOARD-QUERY-001：整理 DashboardQueryService

## 验证方式

按任务卡执行 targeted verification；docs-only 只读任务至少执行 git 状态、diff check、误改范围检查和 evidence 落盘。

## 相关领域

用户、配置、商品、达人、寄样、订单、业绩、分析、跨域事件。

## 风险

如果跳过本阶段，后续重构会在缺少行为锁定的情况下移动核心链路，无法区分重构引入回归还是原有缺陷。

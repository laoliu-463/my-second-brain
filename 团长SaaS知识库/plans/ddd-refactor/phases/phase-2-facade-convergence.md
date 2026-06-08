---
kb_id: "KB-PLAN-DDD-PHASE-2"
title: "Phase 2 Facade 收敛"
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

# Phase 2：Facade 收敛

## 阶段目标

新增极薄 Domain Facade，先收敛 1-3 个跨域读取点。

## 阶段非目标

不改变业务口径，不改变接口契约，不改变数据库结构，不把规划写成完成。

## 进入条件

对应测试已存在或补齐。

## 退出条件

旧调用可保留，新调用有 Facade 入口；接口契约不变。

## 允许任务类型

C

## 禁止事项

禁止一次迁移整个 service 层。

## 推荐任务

- DDD-FACADE-USER-001：新增 UserDomainFacade
- DDD-FACADE-CONFIG-001：新增 ConfigDomainFacade
- DDD-FACADE-PRODUCT-001：新增 ProductDomainFacade
- DDD-FACADE-TALENT-001：新增 TalentDomainFacade
- DDD-FACADE-SAMPLE-001：新增 SampleDomainFacade
- DDD-FACADE-ORDER-001：新增 OrderDomainFacade
- DDD-FACADE-PERFORMANCE-001：新增 PerformanceDomainFacade
- DDD-FACADE-ANALYSIS-001：新增 AnalysisDomainFacade

## 验证方式

按任务卡执行 targeted verification；docs-only 只读任务至少执行 git 状态、diff check、误改范围检查和 evidence 落盘。

## 相关领域

用户、配置、商品、达人、寄样、订单、业绩、分析、跨域事件。

## 风险

如果跳过本阶段，后续重构会在缺少行为锁定的情况下移动核心链路，无法区分重构引入回归还是原有缺陷。

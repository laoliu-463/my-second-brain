---
kb_id: "KB-PLAN-DDD-PHASE-4"
title: "Phase 4 Domain Policy 提取"
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

# Phase 4：Domain Policy 提取

## 阶段目标

把稳定 if/else 业务规则提取为 Policy / Domain Service。

## 阶段非目标

不改变业务口径，不改变接口契约，不改变数据库结构，不把规划写成完成。

## 进入条件

测试覆盖规则分支。

## 退出条件

策略对象仅承载本域规则，行为一致。

## 允许任务类型

D

## 禁止事项

禁止修改业务公式、状态机或权限规则。

## 推荐任务

- DDD-POLICY-USER-DATASCOPE-001：提取 DataScopePolicy
- DDD-POLICY-CONFIG-VALIDATION-001：提取 ConfigValidationPolicy
- DDD-POLICY-PRODUCT-DISPLAY-001：提取 ProductDisplayPolicy
- DDD-POLICY-TALENT-CLAIM-001：提取 TalentClaimPolicy
- DDD-POLICY-SAMPLE-APPLY-001：提取 SampleApplyPolicy
- DDD-POLICY-SAMPLE-COMPLETE-001：提取 SampleCompletionPolicy
- DDD-POLICY-ORDER-ATTRIBUTION-001：提取 OrderAttributionPolicy
- DDD-POLICY-PERFORMANCE-CALC-001：提取 PerformanceCalculationPolicy

## 验证方式

按任务卡执行 targeted verification；docs-only 只读任务至少执行 git 状态、diff check、误改范围检查和 evidence 落盘。

## 相关领域

用户、配置、商品、达人、寄样、订单、业绩、分析、跨域事件。

## 风险

如果跳过本阶段，后续重构会在缺少行为锁定的情况下移动核心链路，无法区分重构引入回归还是原有缺陷。

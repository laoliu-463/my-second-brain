---
kb_id: "KB-PLAN-DDD-PHASE-0"
title: "Phase 0 只读审查"
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

# Phase 0：只读审查

## 阶段目标

不改代码，识别领域边界、跨域依赖、God Service、Mapper 穿透、Controller 胖逻辑、事务和事件风险、测试保护。

## 阶段非目标

不改变业务口径，不改变接口契约，不改变数据库结构，不把规划写成完成。

## 进入条件

当前代码与 KB 可读；完成 code-review-graph / rg 只读扫描。

## 退出条件

每个领域有审查任务卡和证据格式；未产生业务代码修改。

## 允许任务类型

A

## 禁止事项

禁止移动包、禁止抽象空接口、禁止业务修复。

## 推荐任务

- DDD-AUDIT-CROSS-DOMAIN-001：跨域依赖与边界只读审查
- DDD-AUDIT-USER-001：审查数据范围实现
- DDD-AUDIT-USER-MODEL-001：审查用户/角色/部门模型
- DDD-AUDIT-CONFIG-001：审查配置读取路径
- DDD-AUDIT-CONFIG-CACHE-001：审查缓存失效路径
- DDD-AUDIT-PRODUCT-001：审查商品同步与展示规则
- DDD-AUDIT-TALENT-001：审查达人认领、地址与标签
- DDD-AUDIT-SAMPLE-001：审查寄样状态机
- DDD-AUDIT-SAMPLE-SEVEN-DAYS-001：审查 7 天限制
- DDD-AUDIT-SAMPLE-ORDER-COMPLETE-001：审查订单完成寄样逻辑
- DDD-AUDIT-ORDER-001：审查 6468/2704 同步入口
- DDD-AUDIT-ORDER-CURSOR-001：审查 cursor 分页

## 验证方式

按任务卡执行 targeted verification；docs-only 只读任务至少执行 git 状态、diff check、误改范围检查和 evidence 落盘。

## 相关领域

用户、配置、商品、达人、寄样、订单、业绩、分析、跨域事件。

## 风险

如果跳过本阶段，后续重构会在缺少行为锁定的情况下移动核心链路，无法区分重构引入回归还是原有缺陷。

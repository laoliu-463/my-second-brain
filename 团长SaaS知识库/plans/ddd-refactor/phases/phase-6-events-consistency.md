---
kb_id: "KB-PLAN-DDD-PHASE-6"
title: "Phase 6 事件与一致性治理"
domain: "harness"
category: "risk_gate"
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

# Phase 6：事件与一致性治理

## 阶段目标

按单个事件处理 afterCommit、幂等、失败补偿和证据。

## 阶段非目标

不改变业务口径，不改变接口契约，不改变数据库结构，不把规划写成完成。

## 进入条件

事件生产/消费审查完成。

## 退出条件

一个事件边界有幂等和失败证据。

## 允许任务类型

E

## 禁止事项

禁止一次性上完整 Outbox 或 MQ。

## 推荐任务

- DDD-OUTBOX-DESIGN-001：Outbox 预备设计

## 验证方式

按任务卡执行 targeted verification；docs-only 只读任务至少执行 git 状态、diff check、误改范围检查和 evidence 落盘。

## 相关领域

用户、配置、商品、达人、寄样、订单、业绩、分析、跨域事件。

## 风险

如果跳过本阶段，后续重构会在缺少行为锁定的情况下移动核心链路，无法区分重构引入回归还是原有缺陷。

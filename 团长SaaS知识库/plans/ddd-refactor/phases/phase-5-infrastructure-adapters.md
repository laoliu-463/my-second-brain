---
kb_id: "KB-PLAN-DDD-PHASE-5"
title: "Phase 5 Infrastructure Adapter 隔离"
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

# Phase 5：Infrastructure Adapter 隔离

## 阶段目标

将抖音 API、Redis 水位、Mapper 访问、外部网关隔离到 infrastructure/adapter。

## 阶段非目标

不改变业务口径，不改变接口契约，不改变数据库结构，不把规划写成完成。

## 进入条件

应用服务边界清晰。

## 退出条件

Port 与实现分离但行为、日志、配置不变。

## 允许任务类型

C/D

## 禁止事项

禁止引入新外部框架或隐藏 SDK 错误。

## 推荐任务

- DDD-INFRA-PRODUCT-GATEWAY-001：隔离 DouyinProductGateway
- DDD-INFRA-ORDER-GATEWAY-001：隔离 DouyinOrderGateway

## 验证方式

按任务卡执行 targeted verification；docs-only 只读任务至少执行 git 状态、diff check、误改范围检查和 evidence 落盘。

## 相关领域

用户、配置、商品、达人、寄样、订单、业绩、分析、跨域事件。

## 风险

如果跳过本阶段，后续重构会在缺少行为锁定的情况下移动核心链路，无法区分重构引入回归还是原有缺陷。

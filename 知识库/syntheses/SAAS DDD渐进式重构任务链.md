---
title: SAAS DDD渐进式重构任务链
aliases:
  - DDD提示词任务链
  - SAAS DDD 重构路线
created: 2026-06-23
updated: 2026-06-23
topics:
  - SAAS
  - DDD
  - 渐进式重构
tags:
  - synthesis
sources:
  - 知识库/sources/src-20260623-local-ddd-refactor-prompts.md
---

# SAAS DDD渐进式重构任务链

## 概述

这页把 `DDD提示词` 中的长任务包沉淀为可维护的综合页。原始提示词全文保留在 [[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|DDD 提示词原文]]，本页只保留可复用的任务结构和边界。（来源：[[知识库/sources/src-20260623-local-ddd-refactor-prompts|SAAS DDD 渐进式重构提示词包]]；原文：[[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|DDD 提示词原文]]）

## 原文跳转

- [[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|DDD 提示词原文]]

## 任务链结构

| 阶段 | 目标 | 证据来源 | 原文跳转 |
|---|---|---|---|
| 准入基线 | 安全开关、characterization tests、依赖扫描、目标包结构 | [[知识库/sources/src-20260623-local-ddd-refactor-prompts]] | [[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|原文]] |
| 领域门面 | 用户、配置、商品、达人等 facade 先建立旁路入口 | [[知识库/sources/src-20260623-local-ddd-refactor-prompts]] | [[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|原文]] |
| 调用替换 | 订单、寄样、业绩、分析模块逐步改走领域入口 | [[知识库/sources/src-20260623-local-ddd-refactor-prompts]] | [[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|原文]] |
| 事件与瘦身 | Outbox、God Service 方法簇瘦身、跨域 Mapper 清理 | [[知识库/sources/src-20260623-local-ddd-refactor-prompts]] | [[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|原文]] |
| 阶段验收 | 后端、前端、迁移、权限、金额、事件幂等全链路验收 | [[知识库/sources/src-20260623-local-ddd-refactor-prompts]] | [[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|原文]] |

## 可复用结论

- 重构顺序应先保护当前行为，再替换实现路径。（来源：[[知识库/sources/src-20260623-local-ddd-refactor-prompts]]；原文：[[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|DDD 提示词原文]]）
- 跨域依赖清理必须在 facade/policy 稳定后进行。（来源：[[知识库/sources/src-20260623-local-ddd-refactor-prompts]]；原文：[[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|DDD 提示词原文]]）
- 每个任务必须有独立验证，不能把多个领域顺手合并。（来源：[[知识库/sources/src-20260623-local-ddd-refactor-prompts]]；原文：[[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|DDD 提示词原文]]）
- 该任务链是执行提示词，不是当前项目事实；当前事实仍以项目代码、harness 报告和用户确认规则为准。（来源：[[知识库/sources/src-20260623-local-ddd-refactor-prompts]]；原文：[[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|DDD 提示词原文]]）

## 冲突和待验证

- 部分任务可能已在后续 SAAS 项目进度中完成或变更，需要与最新项目状态页对齐。
- 若任务描述与当前代码冲突，优先相信当前代码和已验证报告。

## 关联

- [[知识库/sources/src-20260623-local-ddd-refactor-prompts]]
- [[知识库/09-SaaS体系/index|09-SaaS体系]]

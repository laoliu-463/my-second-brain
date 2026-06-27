---
source_id: src-20260623-local-ddd-refactor-prompts
original_title: DDD提示词（原始）
title: SAAS DDD 渐进式重构提示词包
updated_at: 2026-06-27
aliases:
  - DDD提示词
  - DDD 重构提示词包
source_type: local-prompt-pack
author: 本地知识库
published:
captured: 2026-06-23
canonical_url:
original_path: raw/sources/src-20260623-local-ddd-refactor-prompts/original.md
topics:
  - DDD
  - SAAS
  - 渐进式重构
tags:
  - source
---
# SAAS DDD 渐进式重构提示词包

## 原文跳转

- [[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|原文]]

## 一句话摘要
该来源是一组面向编码 Agent 的 DDD 重构任务提示词，核心是先建立安全开关、基线测试、依赖扫描和目标包结构，再按领域逐步替换调用。

## 作者核心观点

- 重构必须小步执行，每次只做一个任务。
- 先补测试和开关，再做 facade、policy、application service。
- 不改变旧 API、旧响应和数据库行为，默认保持生产行为不变。
- 领域边界优先于代码搬家，跨域依赖需要逐步收口。

## 证据地图

| 证据位置 | 内容 | 影响页面 |
|---|---|---|
| `original.md` 总控提示词 | 技术栈、领域边界、安全红线和验证要求 | [[知识库/syntheses/SAAS DDD渐进式重构任务链|SAAS DDD渐进式重构任务链]] |
| `original.md` Phase 0 | 开关、characterization tests、依赖扫描、包结构 | [[知识库/syntheses/SAAS DDD渐进式重构任务链|SAAS DDD渐进式重构任务链]] |
| `original.md` Phase 1-12 | 用户域、配置域、商品域、事件、瘦身、验收 | [[知识库/syntheses/SAAS DDD渐进式重构任务链|SAAS DDD渐进式重构任务链]] |

## 个人批注

- 该来源是任务包，不是业务规则事实源。实际执行仍必须以当前 `D:\Projects\SAAS` 代码、项目 harness 和用户确认的业务规则为准。

## 待验证项

- 任务编号是否全部仍符合当前 SAAS 项目进度，需要与最新项目状态页交叉确认。

## 影响的知识页

- [[知识库/syntheses/SAAS DDD渐进式重构任务链|SAAS DDD渐进式重构任务链]]
- [[raw/sources/src-20260623-local-ddd-refactor-prompts/original.md|DDD提示词原文]]



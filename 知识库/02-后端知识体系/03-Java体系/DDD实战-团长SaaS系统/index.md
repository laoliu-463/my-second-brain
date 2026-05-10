---
title: DDD实战-团长SaaS系统
tags: [DDD, Java, SpringBoot, PostgreSQL, 抖音开放平台]
created: 2026-05-10
updated: 2026-05-10
sources: [P1-5.2任务上下文, ProductService.java, AttributionService.java, PickSourceMappingService.java]
---

# DDD实战-团长SaaS系统

基于真实业务需求（抖店团长 SaaS 管理平台）进行的 DDD 架构拆解与实战分析。技术栈：Spring Boot + Vue 3 + PostgreSQL + Redis + 抖音开放平台 API。

## 系列索引

### Part 1：战略设计（限界上下文划分）
[[DDD实战-团长SaaS系统/01-战略设计-限界上下文划分]]

### Part 2：核心领域模型详解
[[DDD实战-团长SaaS系统/02-核心领域模型详解]]

### Part 3：本地与三方调用 SOP 分离
[[DDD实战-团长SaaS系统/03-本地与三方调用SOP分离]]

### Part 4：测试规范与 TDD 评估
[[DDD实战-团长SaaS系统/04-测试规范与TDD评估]]

### Part 5：抖店开放平台集成
[[DDD实战-团长SaaS系统/06-抖店开放平台集成]]

### Part 6：认证授权体系
[[DDD实战-团长SaaS系统/05-认证授权体系]]

### Part 7：抖店开放平台集成
[[DDD实战-团长SaaS系统/06-抖店开放平台集成]]

### Part 8：样品生命周期
[[DDD实战-团长SaaS系统/07-样品生命周期]]

### Part 9：招商结算与佣金体系
[[DDD实战-团长SaaS系统/08-招商结算与佣金体系]]

### Part 10：达人管理与资格体系
[[DDD实战-团长SaaS系统/09-达人管理与资格体系]]

### Part 11：商品运营与活动链路
[[DDD实战-团长SaaS系统/10-商品运营与活动链路]]

### Part 12：爬虫数据采集体系
[[DDD实战-团长SaaS系统/11-爬虫数据采集体系]]

### Part 13：数据库架构概览
[[DDD实战-团长SaaS系统/12-数据库架构概览]]

### Part 14：前端技术栈与工程结构
[[DDD实战-团长SaaS系统/13-前端技术栈与工程结构]]

### Part 15：Maven 依赖与版本清单
[[DDD实战-团长SaaS系统/14-Maven依赖与版本清单]]

## 核心问题背景（P1-5.2）

**根因**：活动创建时 `colonel_activity` 表的 `colonel_buyin_id` 主字段为 null（COALESCE UPSERT 问题），但 `extra_data` JSONB 字段有值。旧代码只查主字段不查 `extra_data`，导致抖店原生归因链路断裂。

**修复**：在 `ColonelBuyinIdResolver.resolveFromActivity()` 增加 `extra_data` fallback 查询，让分层解析策略（POLICY）补全最后一层。

## 技术栈

| 层级 | 技术选型 |
|---|---|
| 后端 | Spring Boot + MyBatis-Plus |
| 数据库 | PostgreSQL + Redis |
| 前端 | Vue 3 + Pinia + Axios |
| 三方 API | 抖音开放平台（精选联盟、订单、推广链接） |
| 部署 | Docker Compose + 宝塔面板 |

## 相关概念

- [[Spring实战(第4版)]]（Spring Boot 框架基础）
- [[Thinking_in_Java]]（Java 面向对象设计）
- [[DDD_血色绿茵联赛项目]]（DDD 实战参考）

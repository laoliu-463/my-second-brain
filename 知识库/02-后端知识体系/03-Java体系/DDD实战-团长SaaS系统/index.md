---
title: DDD实战-团长SaaS系统
tags: [DDD, Java, SpringBoot, PostgreSQL, 抖音开放平台]
created: 2026-05-10
updated: 2026-05-18
sources: [ProductService.java, AttributionService.java, PickSourceMappingService.java, OrderAttributionReplayService.java, scripts/, raw/sources/抖音团长SaaS设计文档/]
---

# DDD实战-团长SaaS系统

基于真实业务需求（抖店团长 SaaS 管理平台）进行的 DDD 架构拆解与实战分析。当前系列包含两类材料：既有 Spring Boot + Vue 3 + PostgreSQL + Redis 的实现复盘，以及 2026-05-18 新归档的 FastAPI + Celery V1 设计文档摘要。两套口径可互相对照，但不直接互相覆盖。

## 系列索引

### Part 1：战略设计（限界上下文划分）
[[DDD实战-团长SaaS系统/01-战略设计-限界上下文划分]]

### Part 2：核心领域模型详解
[[DDD实战-团长SaaS系统/02-核心领域模型详解]]

### Part 3：本地与三方调用 SOP 分离
[[DDD实战-团长SaaS系统/03-本地与三方调用SOP分离]]

### Part 4：测试规范与 TDD 评估
[[DDD实战-团长SaaS系统/04-测试规范与TDD评估]]

### Part 5：认证授权体系
[[DDD实战-团长SaaS系统/05-认证授权体系]]

### Part 6：抖店开放平台集成
[[DDD实战-团长SaaS系统/06-抖店开放平台集成]]

### Part 7：样品生命周期
[[DDD实战-团长SaaS系统/07-样品生命周期]]

### Part 8：招商结算与佣金体系
[[DDD实战-团长SaaS系统/08-招商结算与佣金体系]]

### Part 9：达人管理与资格体系
[[DDD实战-团长SaaS系统/09-达人管理与资格体系]]

### Part 10：商品运营与活动链路
[[DDD实战-团长SaaS系统/10-商品运营与活动链路]]

### Part 11：爬虫数据采集体系
[[DDD实战-团长SaaS系统/11-爬虫数据采集体系]]

### Part 12：数据库架构概览
[[DDD实战-团长SaaS系统/12-数据库架构概览]]

### Part 13：前端技术栈与工程结构
[[DDD实战-团长SaaS系统/13-前端技术栈与工程结构]]

### Part 14：Maven 依赖与版本清单
[[DDD实战-团长SaaS系统/14-Maven依赖与版本清单]]

### Part 15：独家达人与独家商家体系
[[DDD实战-团长SaaS系统/15-独家达人与独家商家体系]]

### Part 16：操作审计日志体系
[[DDD实战-团长SaaS系统/16-操作审计日志体系]]

### Part 17：达人数据补全 Provider 体系
[[DDD实战-团长SaaS系统/17-达人数据补全Provider体系]]

### Part 18：Webhook 事件接收与消费体系
[[DDD实战-团长SaaS系统/18-Webhook事件接收与消费体系]]

### Part 19：归因重放与历史订单修复
[[DDD实战-团长SaaS系统/19-归因重放与历史订单修复]]

### Part 20：脚本与 QA 体系
[[DDD实战-团长SaaS系统/20-脚本与QA体系]]

### Part 21：V1 交付范围与业务链
[[DDD实战-团长SaaS系统/21-V1交付范围与业务链]]

### Part 22：FastAPI 技术落地蓝图
[[DDD实战-团长SaaS系统/22-FastAPI技术落地蓝图]]

### Part 23：七领域设计总览
[[DDD实战-团长SaaS系统/23-七领域设计总览]]

### Part 24：V1.6 骨架与当前项目现状对比
[[DDD实战-团长SaaS系统/24-V1.6骨架与当前项目现状对比]]

## 设计来源补充

2026-05-18 新增的 `saas系统文件.zip` 已归档到 `raw/sources/抖音团长SaaS设计文档/`。该来源包含 V1 交付范围表、技术落地设计、总体骨架、V2.2 旧版需求和 8 份领域设计文档。来源追踪见 [[知识库/90-来源与映射/抖音团长SaaS设计文档来源映射|抖音团长SaaS设计文档来源映射]]。

## 核心问题背景

**根因**：活动创建时 `colonel_activity` 表的 `colonel_buyin_id` 主字段为 null（COALESCE UPSERT 问题），但 `extra_data` JSONB 字段有值。旧代码只查主字段不查 `extra_data`，导致抖店原生归因链路断裂。

**修复**：在 `ColonelBuyinIdResolver.resolveFromActivity()` 增加 `extra_data` fallback 查询，让分层解析策略（POLICY）补全最后一层。

## 技术栈

| 层级             | 技术选型                       |      |
| -------------- | -------------------------- | ---- |
| 后端             | Spring Boot + MyBatis-Plus |      |
| 数据库            | PostgreSQL + Redis         |      |
| 前端             | Vue 3 + Pinia + Axios      |      |
| 三方 API         | 抖音开放平台（精选联盟、订单、推广链接）       |      |
| 部署             | Docker Compose + 宝塔面板      |      |
| 账号             | 密码                         | 角色   |
| admin          | admin123                   | 管理员  |
| biz_leader     | admin123                   | 招商组长 |
| biz_staff      | admin123                   | 招商专员 |
| channel_leader | admin123                   | 渠道组长 |
| channel_staff  | admin123                   | 渠道专员 |
| ops_staff      | admin123                   | 运营   |
## 相关概念

- [[Spring实战(第4版)]]（Spring Boot 框架基础）
- [[Thinking_in_Java]]（Java 面向对象设计）
- [[DDD实战-团长SaaS系统/21-V1交付范围与业务链]]
- [[DDD实战-团长SaaS系统/22-FastAPI技术落地蓝图]]
- [[DDD实战-团长SaaS系统/23-七领域设计总览]]
- [[知识库/90-来源与映射/抖音团长SaaS设计文档来源映射]]

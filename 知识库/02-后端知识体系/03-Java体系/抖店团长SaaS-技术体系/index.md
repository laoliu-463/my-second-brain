---
title: 抖店团长SaaS技术体系
tags: [抖店团长, 技术体系, SpringBoot, Vue3, 代码架构, SaaS]
created: 2026-05-29
updated: 2026-06-27
source_level: none
sources:
  - D:/Projects/SAAS
---
# 抖店团长SaaS技术体系

## 概述

本系列从代码架构视角出发，按 **代码结构 → 数据模型 → API → 测试验收 → 部署运行 → ADR** 的顺序组织，基于 `D:\Projects\SAAS` 的实际代码扫描和项目文档。上线前 release 审查和 real-pre 受控部署结论沉淀在 DDD 系列专项页中，不能简化成“生产已上线”。

技术栈：Spring Boot 3.2.5 + Java 17 + PostgreSQL + Redis + Vue 3 + TypeScript + Vite + Playwright。

## 系列结构

```
抖店团长SaaS-技术体系/
├── 01-技术总览              # 项目定位、技术栈、技术决策
├── 02-代码结构/
│   ├── 后端代码结构         # Spring Boot 包结构（23个顶层包）
│   ├── 前端代码结构         # Vue 3 目录（13个目录）
│   └── 前后端映射          # API 文件 ↔ Controller 映射
├── 03-数据模型             # 数据库表、实体与领域对应
├── 04-API契约              # 内部API + 第三方API入口
├── 05-第三方对接/          # 6项第三方接口详情
├── 06-测试验收             # Playwright E2E、状态分类、证据索引
├── 07-部署运行             # test/real-pre 双环境、Docker Compose
├── 08-ADR/                # 架构决策记录（与业务体系共用）
└── 关联专项：DDD/49-real-pre上线前总审查与受控部署
```

## 技术栈地图

| 层级 | 技术 |
| --- | --- |
| 后端 | Spring Boot 3.2.5 + Java 17 + MyBatis-Plus |
| 数据库 | PostgreSQL |
| 缓存 | Redis |
| 前端 | Vue 3 + TypeScript + Vite + Naive UI + Pinia |
| 验收 | Playwright + Vitest + JUnit 5 + JaCoCo |
| 部署 | Docker Compose（test / real-pre 双环境） |
| 第三方 | 抖店/抖音 Gateway 封装（本地 maven-repo） |

## 项目规模

| 指标 | 数值 |
| --- | --- |
| 代码文件数 | 1043 |
| 图谱节点数 | 8677 |
| 图谱边数 | 99347 |
| 后端包数 | 23 个顶层包 |
| 前端视图模块 | 11 个（dashboard/data/dev/layout/ops/orders/product/profile/sample/system/talent） |

## 相关概念

- [[抖店团长SaaS-业务体系/index|抖店团长SaaS业务体系]] — 业务视角
- [[DDD实战-团长SaaS系统/index]] — 原有 DDD 实战系列
- [[DDD实战-团长SaaS系统/49-real-pre上线前总审查与受控部署]]

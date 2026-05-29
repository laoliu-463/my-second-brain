---
title: DDD实战-团长SaaS系统
tags: [DDD, SaaS, SpringBoot, Vue3, 抖音团长, 项目索引]
created: 2026-05-29
updated: 2026-05-29
sources:
  - D:/Projects/SAAS/README.md
  - D:/Projects/SAAS/AGENTS.md
  - D:/Projects/SAAS/docs/README.md
  - 知识库/90-来源与映射/抖音团长SaaS当前项目来源映射.md
  - 知识库/90-来源与映射/抖音团长SaaS设计文档来源映射.md
---

# DDD实战-团长SaaS系统

## 概述

本系列用于维护“抖音团长 SaaS”项目的长期知识地图，分成三类事实：早期 Spring Boot 实战复盘、2026-05-18 归档的 FastAPI / V1 设计来源、以及 `D:\Projects\SAAS` 当前 Spring Boot + Vue 3 活跃代码项目。后续排查和开发必须优先读取当前项目事实，旧 V2.2、FastAPI、Celery 等内容只能作为历史设计背景。

## 当前阅读顺序

1. 当前项目接管：[[DDD实战-团长SaaS系统/27-当前代码项目接管地图|当前代码项目接管地图]]
2. 当前业务口径：[[抖店团长SaaS-业务体系/index|抖店团长SaaS-业务体系]]
3. 当前技术口径：[[抖店团长SaaS-技术体系/index|抖店团长SaaS-技术体系]]
4. 代码图谱入口：[[DDD实战-团长SaaS系统/28-代码图谱总览与脉络索引|代码图谱总览与脉络索引]]
5. 验收与部署：[[DDD实战-团长SaaS系统/47-测试验收总览|测试验收总览]]、[[DDD实战-团长SaaS系统/48-部署运行总览|部署运行总览]]、[[DDD实战-团长SaaS系统/49-real-pre上线前总审查与受控部署|real-pre上线前总审查与受控部署]]

## 系列分层

| 分层 | 页面范围 | 维护口径 |
| --- | --- | --- |
| 早期 Spring Boot 实战复盘 | 01-20 | 保留原有 DDD、认证、抖店集成、寄样、订单归因、脚本 QA 等复盘内容 |
| FastAPI / V1 设计来源 | 21-26 | 来自 2026-05-18 归档设计文档，只作设计背景和差异对照 |
| 当前代码项目接管 | 27-32 | 以 `D:\Projects\SAAS` 当前代码、文档、测试脚本和 code-review-graph 为事实源 |
| 当前专项总览 | 46-49 | 权限、测试验收、部署运行、real-pre 审查等当前执行口径 |
| 业务 / 技术双体系 | 抖店团长SaaS-业务体系、抖店团长SaaS-技术体系 | 当前项目的正式可导航知识体系 |

## 当前项目入口

| 页面 | 作用 |
| --- | --- |
| [[DDD实战-团长SaaS系统/27-当前代码项目接管地图|当前代码项目接管地图]] | 区分当前代码事实、历史设计和验收证据链 |
| [[DDD实战-团长SaaS系统/28-后端代码结构索引|后端代码结构索引]] | 后端包结构与七领域关系 |
| [[DDD实战-团长SaaS系统/29-前端代码结构索引|前端代码结构索引]] | 前端目录、视图、API 与领域映射 |
| [[DDD实战-团长SaaS系统/30-前后端映射对照|前后端映射对照]] | 前端 API 文件与后端 Controller 对照 |
| [[DDD实战-团长SaaS系统/28-代码图谱总览与脉络索引|代码图谱总览与脉络索引]] | code-review-graph 视角的社区、执行流和热点入口 |
| [[DDD实战-团长SaaS系统/29-后端代码图谱脉络|后端代码图谱脉络]] | 后端 Controller、Service、Gateway、Mapper、Security、Job 的结构关系 |
| [[DDD实战-团长SaaS系统/30-前端页面与API图谱脉络|前端页面与API图谱脉络]] | 前端 views、api、router、utils 与 E2E 的结构关系 |
| [[DDD实战-团长SaaS系统/31-测试验收与QA图谱脉络|测试验收与QA图谱脉络]] | Maven、Vitest、Playwright、runtime QA 与证据索引 |
| [[DDD实战-团长SaaS系统/32-代码图谱风险与维护清单|代码图谱风险与维护清单]] | 高连接节点、大文件、大函数和后续治理清单 |
| [[DDD实战-团长SaaS系统/49-real-pre上线前总审查与受控部署|real-pre上线前总审查与受控部署]] | 2026-05-28 release 审查结论、PASS/PENDING/BLOCKED 边界 |

## 证据边界

- `D:\Projects\SAAS` 是活跃代码项目，不复制到 `raw/`，知识库只保存摘要、路径和来源映射。
- `.env`、`.env.real-pre`、`.env.test` 不进入知识库；只允许引用示例文件和文档中的配置字段。
- code-review-graph 只能证明代码结构和调用关系，不能替代 `mvn test`、`npm run build`、Playwright 或真实接口日志。
- `real-pre` 受控部署不等于正式生产全量上线；真实凭据、真实订单样本和上游联调不足时只能标记 `PENDING` 或 `BLOCKED`。

## 相关概念

- [[抖店团长SaaS-业务体系/index|抖店团长SaaS-业务体系]]
- [[抖店团长SaaS-技术体系/index|抖店团长SaaS-技术体系]]
- [[知识库/90-来源与映射/抖音团长SaaS当前项目来源映射|抖音团长SaaS当前项目来源映射]]
- [[知识库/90-来源与映射/抖音团长SaaS设计文档来源映射|抖音团长SaaS设计文档来源映射]]

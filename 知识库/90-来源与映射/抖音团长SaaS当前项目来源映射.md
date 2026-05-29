---
title: 抖音团长SaaS当前项目来源映射
tags: [来源映射, SaaS, DDD, SpringBoot, HarnessEngineering, 抖音团长]
created: 2026-05-29
updated: 2026-05-29
sources:
  - D:/Projects/SAAS/
  - D:/Projects/SAAS/AGENTS.md
  - D:/Projects/SAAS/CLAUDE.md
  - D:/Projects/SAAS/docs/
  - code-review-graph:SAAS
---

# 抖音团长SaaS当前项目来源映射

## 概述

本页追踪 `D:\Projects\SAAS` 当前代码项目与正式 wiki 页面之间的映射关系。它和 [[抖音团长SaaS设计文档来源映射]] 分工不同：后者追踪 2026-05-18 归档的设计资料；本页追踪当前可运行项目、主干文档、代码结构、验收脚本和部署口径。

本次没有把 `D:\Projects\SAAS` 复制到 `raw/`：该目录是活跃代码仓库，不是不可变原始资料。知识库只保存结构化摘要和来源路径，不保存 `.env`、运行报告、缓存、构建产物或敏感配置。

## 来源清单

| 来源 | 类型 | 用途 |
| --- | --- | --- |
| `D:\Projects\SAAS\README.md` | 项目说明 | 项目定位、核心能力、环境端口、快速启动和 secret policy |
| `D:\Projects\SAAS\AGENTS.md` | 项目级代理规范 | Harness Engineering 接管规则、当前阶段、目录导航、风险和强制规则 |
| `D:\Projects\SAAS\CLAUDE.md` | 仓库地图 | 当前事实、阅读路径、不变量和验收命令 |
| `D:\Projects\SAAS\CONTEXT.md` | 术语表 | 团长活动、活动商品、共享商品库、推广链接、归因映射、test、real-pre 等术语 |
| `D:\Projects\SAAS\docs\README.md` | 文档地图 | 主干文档顺序、范围标记、专题目录和不变量 |
| `D:\Projects\SAAS\docs\00-10` | 当前主干事实 | 项目总览、V1 边界、业务闭环、领域架构、事件、API、数据、权限、第三方、验收、部署 |
| `D:\Projects\SAAS\docs\领域\` | 领域合同 | 用户、配置、商品、达人、寄样、订单、业绩、分析模块职责边界 |
| `D:\Projects\SAAS\docs\流程\` | 业务流程 | 渠道、招商、管理、订单归因、寄样交作业、业绩计算 |
| `D:\Projects\SAAS\docs\验收\` | 验收证据入口 | V1 P0、real-pre、E2E、回归脚本和证据索引 |
| `D:\Projects\SAAS\docs\决策\` | ADR | 模块化单体、V1 范围优先级、订单 / 业绩 / 分析边界 |
| `D:\Projects\SAAS\backend\pom.xml` | 后端依赖事实 | Spring Boot、Java、MyBatis-Plus、PostgreSQL、Redis、JWT、Testcontainers、JaCoCo |
| `D:\Projects\SAAS\frontend\package.json` | 前端依赖事实 | Vue 3、TypeScript、Vite、Naive UI、Pinia、Vue Router、Vitest |
| `D:\Projects\SAAS\package.json` | 验收脚本入口 | Playwright、real-pre、P0、角色、视觉、前端测试脚本 |
| code-review-graph | 代码结构图谱 | 文件数、节点数、社区、主要执行流和耦合提示 |

## 页面映射

| 正式页面 | 使用来源 | 沉淀内容 |
| --- | --- | --- |
| [[DDD实战-团长SaaS系统/27-当前代码项目接管地图|当前代码项目接管地图]] | `AGENTS.md`、`CLAUDE.md`、`docs/README.md`、`docs/00-10`、`pom.xml`、`package.json`、code-review-graph | 当前项目定位、技术栈、目录地图、领域闭环、运行验收口径、代码图谱观察和维护提醒 |
| [[DDD实战-团长SaaS系统/index|DDD实战-团长SaaS系统]] | 当前项目地图 + 既有系列 | 将系列从“设计文档和旧实现复盘”扩展为“当前代码项目接管入口” |
| [[DDD实战-团长SaaS系统/24-V1.6骨架与当前项目现状对比|V1.6骨架与当前项目现状对比]] | 历史项目状态 + 当前主干文档 | 后续复核时应以当前 `docs/README.md`、`docs/00-10` 和代码事实重新校准 |
| [[DDD实战-团长SaaS系统/25-V1交付范围逐条对照|V1交付范围逐条对照]] | 历史验收对照 + 当前验收文档 | 后续更新应优先接 `docs/09-测试验收总览.md`、`docs/验收/` 和脚本结果 |

## 明确排除

| 路径 / 类型 | 排除原因 |
| --- | --- |
| `.env`、`.env.real-pre`、`.env.test` | 可能包含真实凭据、Token、数据库密码或联调参数 |
| `node_modules/` | 依赖安装产物，不进入知识库 |
| `out/`、`playwright-report/`、`test-results/` | 运行产物和报告目录，后续只引用已归档证据摘要 |
| `.git/`、`.idea/`、`.vscode/` | 工具状态，不作为业务事实 |
| `.opencode/tmp/`、`.codex-run/` | 临时执行目录，只在需要追溯某次任务时读取 |
| `colonel-saas*.zip/tar.gz` | 压缩包来源未纳入本次整理；如需归档，应先确认是否为不可变来源 |

## 维护规则

- 当 `D:\Projects\SAAS\AGENTS.md`、`CLAUDE.md`、`docs/README.md`、`docs/00-10` 有重要变化时，应优先更新 [[DDD实战-团长SaaS系统/27-当前代码项目接管地图|当前代码项目接管地图]]。
- 当 V1 范围、real-pre 口径、验收脚本或 ADR 变化时，应同步检查 [[DDD实战-团长SaaS系统/index|DDD实战-团长SaaS系统]] 与全局 `index.md`。
- 当前项目是活跃仓库，不复制到 `raw/`。只有用户明确提供不可变来源包、导出文档或验收报告时，才按 `raw/sources/` 归档规范处理。
- 所有“已完成”“已验收”“可上线”结论必须回到脚本结果、API / SQL 证据、日志或项目内证据索引；没有证据时只能写阶段性结论。

## 相关概念

- [[DDD实战-团长SaaS系统/index|DDD实战-团长SaaS系统]]
- [[DDD实战-团长SaaS系统/27-当前代码项目接管地图|当前代码项目接管地图]]
- [[抖音团长SaaS设计文档来源映射]]

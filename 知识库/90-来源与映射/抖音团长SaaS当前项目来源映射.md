---
title: 抖音团长SaaS当前项目来源映射
tags: [来源映射, SaaS, DDD, SpringBoot, HarnessEngineering, 抖音团长]
created: 2026-05-29
updated: 2026-06-27
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
| `D:\Projects\SAAS\docs\release\` | release 审查 | real-pre 上线前总审查报告、PASS/PENDING/BLOCKED 口径 |
| `D:\Projects\SAAS\docs\deploy\` | 部署文档 | 服务器初始化、Docker 手动部署、回滚、Jenkins 规划和部署报告 |
| `D:\Projects\SAAS\backend\pom.xml` | 后端依赖事实 | Spring Boot、Java、MyBatis-Plus、PostgreSQL、Redis、JWT、Testcontainers、JaCoCo |
| `D:\Projects\SAAS\frontend\package.json` | 前端依赖事实 | Vue 3、TypeScript、Vite、Naive UI、Pinia、Vue Router、Vitest |
| `D:\Projects\SAAS\package.json` | 验收脚本入口 | Playwright、real-pre、P0、角色、视觉、前端测试脚本 |
| code-review-graph | 代码结构图谱 | 文件数、节点数、社区、主要执行流和耦合提示 |

## 页面映射

### 业务体系（业务视角，来自 docs/ 主干文档）

| 正式页面 | 使用来源 | 沉淀内容 |
| --- | --- | --- |
| [[抖店团长SaaS-业务体系/index|业务体系索引]] | docs/ 主干文档 + 本次重构 | 业务视角系列入口：V1范围、主链路、七领域、事件/权限 |
| [[抖店团长SaaS-业务体系/01-V1交付范围与边界|V1交付范围与边界]] | `docs/00-10/01-V1交付范围与边界.md` | V1 必做/简化/不做/V2 预留边界，冲突处理规则 |
| [[抖店团长SaaS-业务体系/02-业务闭环总览|业务闭环总览]] | `docs/00-10/02-业务闭环总览.md` | 总体闭环流程图、六条主链路索引 |
| [[抖店团长SaaS-业务体系/03-渠道主链路|渠道主链路]] | `docs/流程/渠道主链路.md` | 渠道用户全链路：登录→商品→转链→达人→寄样→订单→业绩 |
| [[抖店团长SaaS-业务体系/03-招商主链路|招商主链路]] | `docs/流程/招商主链路.md` | 招商链路：商品同步→达人维护→寄样→审批→转链→归因 |
| [[抖店团长SaaS-业务体系/03-管理主链路|管理主链路|管理主链路]] | `docs/流程/管理主链路.md` | 管理员链路：用户/角色/组织/菜单/配置/审计/看板 |
| [[抖店团长SaaS-业务体系/03-订单归因链路|订单归因链路]] | `docs/流程/订单归因链路.md` | 转链→订单同步→pick_source映射→业绩归属 |
| [[抖店团长SaaS-业务体系/03-寄样交作业链路|寄样交作业链路]] | `docs/流程/寄样交作业链路.md` | 申请→审批→发货→订单回流→交作业完成 |
| [[抖店团长SaaS-业务体系/03-业绩计算链路|业绩计算链路]] | `docs/流程/业绩计算链路.md` | 订单+映射+配置→归属→提成→冲正→汇总 |
| [[抖店团长SaaS-业务体系/04-七领域合同/index|七领域合同]] | `docs/领域/` 全部8个领域文档 | 七领域 + 分析模块职责边界、依赖关系、ADR 索引 |
| [[抖店团长SaaS-业务体系/04-七领域合同/用户域|用户域]] | `docs/领域/用户域.md` | 账号、角色、组织、`self/group/all` 数据范围 |
| [[抖店团长SaaS-业务体系/04-七领域合同/配置域|配置域]] | `docs/领域/配置域.md` | 配置读取、变更、审计，不执行具体业务规则 |
| [[抖店团长SaaS-业务体系/04-七领域合同/商品域|商品域]] | `docs/领域/商品域.md` | 活动商品、商品库、转链、`pick_source_mapping` |
| [[抖店团长SaaS-业务体系/04-七领域合同/达人域|达人域]] | `docs/领域/达人域.md` | 达人资料、标签、地址、渠道关系 |
| [[抖店团长SaaS-业务体系/04-七领域合同/寄样域|寄样域]] | `docs/领域/寄样域.md` | 申请→审批→发货→交作业（以订单已同步事件为证据） |
| [[抖店团长SaaS-业务体系/04-七领域合同/订单域|订单域]] | `docs/领域/订单域.md` | 订单事实、退款事实、归因输入，只存事实不算提成 |
| [[抖店团长SaaS-业务体系/04-七领域合同/业绩域|业绩域]] | `docs/领域/业绩域.md` | 最终归属、提成、冲正，双轨金额计算 |
| [[抖店团长SaaS-业务体系/04-七领域合同/分析模块|分析模块]] | `docs/领域/分析模块.md` | 只读汇总、报表、看板，不重算业绩归属 |
| [[抖店团长SaaS-业务体系/05-事件契约|事件契约]] | `docs/04-事件契约总表.md` | 核心领域事件的触发条件和消费方 |
| [[抖店团长SaaS-业务体系/05-权限与数据范围|权限与数据范围]] | `docs/07-权限与数据范围.md` | `self/group/all` 定义与技术实现 |

### 技术体系（代码视角，来自项目代码扫描）

| 正式页面 | 使用来源 | 沉淀内容 |
| --- | --- | --- |
| [[抖店团长SaaS-技术体系/index|技术体系索引]] | 项目代码扫描 + 本次重构 | 代码视角系列入口：后端结构、前端结构、数据/API、第三方、测试、部署、ADR |
| [[抖店团长SaaS-技术体系/02-后端代码结构|后端代码结构]] | `backend/src/main/java/com/colonel/saas/` | 23个顶层包：controller、service、domain、entity、mapper、dto、vo、event、gateway、job、listener 等 |
| [[抖店团长SaaS-技术体系/02-前端代码结构|前端代码结构]] | `frontend/src/` | Vue 3 13个目录：views（11个视图）、api、stores、components 等 |
| [[抖店团长SaaS-技术体系/02-前后端映射|前后端映射]] | 后端 Controller + 前端 api/ 目录对照 | 14个前端 API 文件 ↔ 后端 Controller 映射表 |
| [[抖店团长SaaS-技术体系/03-数据模型|数据模型]] | 数据库表结构 + 项目代码 | 12个数据模型/表族，与七领域对应 |
| [[抖店团长SaaS-技术体系/04-API契约|API契约]] | 后端 Controller 接口定义 | 13类内部 API + 6项第三方 API 入口 |
| [[抖店团长SaaS-技术体系/05-抖音授权与Token|抖音授权与Token]] | `backend/src/main/java/com/colonel/saas/douyin/` + `docs/对接/抖音授权与Token.md` | OAuth 授权码换 Token、刷新、过期处理 |
| [[抖店团长SaaS-技术体系/05-活动商品同步|活动商品同步]] | `douyin/` 模块 + `docs/对接/活动商品同步.md` | 活动商品同步、商品库入库 |
| [[抖店团长SaaS-技术体系/05-转链与pick_source归因|转链与pick_source归因]] | `douyin/` + `docs/对接/转链与pick_source归因.md` | `buyin.instPickSourceConvert`、双开关控制 |
| [[抖店团长SaaS-技术体系/05-订单同步|订单同步]] | `douyin/` + `docs/对接/订单同步.md` | 抖店订单同步、退款事实、幂等 |
| [[抖店团长SaaS-技术体系/05-物流接口|物流接口]] | `douyin/` + `docs/对接/物流接口.md` | 寄样发货、物流查询、BLOCKED 证据 |
| [[抖店团长SaaS-技术体系/05-达人信息获取|达人信息获取]] | `douyin/` + `docs/对接/达人信息获取.md` | 达人资料补全、权限包限制 |
| [[抖店团长SaaS-技术体系/06-测试验收|测试验收]] | `docs/09-测试验收总览.md`、`docs/验收/`、`package.json` | Playwright E2E 命令、状态分类（PASS/BLOCKED/PENDING/FAIL） |
| [[抖店团长SaaS-技术体系/07-部署运行|部署运行]] | `docs/10-部署运行总览.md`、Docker Compose、`.env.test` | test/real-pre 双环境、Docker Compose、端口约束 |
| [[抖店团长SaaS-技术体系/08-ADR/index|ADR 索引]] | `docs/决策/` 全部 ADR 文档 | 6个核心架构决策记录索引 |
| [[抖店团长SaaS-技术体系/08-ADR/ADR-001|ADR-001]] | `docs/决策/ADR-001-模块化单体.md` | Spring Boot 模块化单体，不引入 FastAPI/Celery |
| [[抖店团长SaaS-技术体系/08-ADR/ADR-002|ADR-002]] | `docs/决策/ADR-002-V1范围优先级.md` | 当前代码优先、冲突必须写 ADR |
| [[抖店团长SaaS-技术体系/08-ADR/ADR-003|ADR-003]] | `docs/决策/ADR-003-订单域只存事实.md` | 订单域只存事实，不算提成 |
| [[抖店团长SaaS-技术体系/08-ADR/ADR-004|ADR-004]] | `docs/决策/ADR-004-业绩域负责最终归属.md` | 业绩域负责最终归属 |
| [[抖店团长SaaS-技术体系/08-ADR/ADR-005|ADR-005]] | `docs/决策/ADR-005-分析模块只读汇总.md` | 分析模块只读汇总 |
| [[抖店团长SaaS-技术体系/08-ADR/ADR-006|ADR-006]] | `docs/决策/ADR-006-real-pre作为上线前联调环境.md` | real-pre 关闭 mock，PASS 须真实接口证据 |

### DDD 系列与当前项目专项

| 正式页面 | 使用来源 | 沉淀内容 |
| --- | --- | --- |
| [[DDD实战-团长SaaS系统/index|DDD实战-团长SaaS系统]] | 当前项目地图 + FastAPI 设计文档 + 当前项目专项页 | 系列索引：早期实战、历史设计、当前代码项目、图谱和验收部署口径 |
| [[DDD实战-团长SaaS系统/27-当前代码项目接管地图|当前代码项目接管地图]] | `AGENTS.md`、`CLAUDE.md`、`docs/README.md`、`docs/00-10`、`pom.xml`、`package.json`、code-review-graph | 当前项目定位、技术栈、目录地图、领域闭环、运行验收口径 |
| [[DDD实战-团长SaaS系统/28-代码图谱总览与脉络索引|代码图谱总览与脉络索引]] | code-review-graph:SAAS | 图谱统计、社区、关键执行流、热点节点和排查入口 |
| [[DDD实战-团长SaaS系统/29-后端代码图谱脉络|后端代码图谱脉络]] | code-review-graph + `backend/src/main/java` | 后端 Controller、Service、Gateway、Mapper、Security、Job 的结构关系 |
| [[DDD实战-团长SaaS系统/30-前端页面与API图谱脉络|前端页面与API图谱脉络]] | code-review-graph + `frontend/src` | 前端页面、API、路由、错误提示和 E2E 脉络 |
| [[DDD实战-团长SaaS系统/31-测试验收与QA图谱脉络|测试验收与QA图谱脉络]] | code-review-graph + `package.json` + `docs/验收/` + `.claude/qa/` | 测试资产、QA 脚本、E2E bridge 和证据索引 |
| [[DDD实战-团长SaaS系统/32-代码图谱风险与维护清单|代码图谱风险与维护清单]] | code-review-graph hub / bridge / large function 结果 | 高连接节点、大文件、大函数、criticality flow 和维护取证清单 |
| [[DDD实战-团长SaaS系统/46-权限与数据范围|权限与数据范围]] | `docs/07-权限与数据范围.md` | self/group/all、角色权限、后端校验和 E2E 口径 |
| [[DDD实战-团长SaaS系统/47-测试验收总览|测试验收总览]] | `docs/09-测试验收总览.md` | test/mock 与 real-pre 验收分层、脚本入口和状态分类 |
| [[DDD实战-团长SaaS系统/48-部署运行总览|部署运行总览]] | `docs/10-部署运行总览.md` | test/real-pre 双环境、Docker Compose、端口和 mock 开关 |
| [[DDD实战-团长SaaS系统/49-real-pre上线前总审查与受控部署|real-pre上线前总审查与受控部署]] | `docs/release/real-pre上线总审查报告-20260528-171543.md` | 可受控部署结论、未达成项、PENDING/BLOCKED 边界和后续验证路径 |

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

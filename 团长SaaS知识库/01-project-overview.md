---
kb_id: 01-project-overview
title: 项目总览
domain: project
category: overview
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/01-V1交付范围与边界.md
  - docs/README.md
  - harness/CURRENT_STATE.md
  - harness/AGENT_CONTRACT.md
related_reports: []
forbidden_misread:
  - 绝不允许把 V2.2 旧方案、FastAPI / Celery 设想写为 V1 事实
  - real-pre 状态未达到 PASS 时不可对外宣称真实闭环
---

# 项目总览

## 1. 项目名称

抖音团长 SaaS（V1）。一个面向抖音/抖店生态的团长（联盟）业务管理平台，承载渠道、招商、管理三类角色的核心业务操作。

## 2. 业务范围（V1）

V1 范围由 `docs/01-V1交付范围与边界.md` 定义，V1 优先于旧 V2.2 全量设想。

### 2.1 三条主链

| 主链 | 角色 | 入口合同 | KB 链接 |
| --- | --- | --- | --- |
| 渠道主链 | 渠道组长 / 渠道专员 | `docs/流程/渠道主链路.md` | [workflows/01-channel-main.md](workflows/01-channel-main.md) |
| 招商主链 | 招商组长 / 招商专员 | `docs/流程/招商主链路.md` | [workflows/02-recruiter-main.md](workflows/02-recruiter-main.md) |
| 管理主链 | 管理员 | `docs/流程/管理主链路.md` | [workflows/03-management-main.md](workflows/03-management-main.md) |

### 2.2 八个领域

| 域 | 主合同 | 关键边界 |
| --- | --- | --- |
| 用户域 | `docs/领域/用户域.md` | `self / group / all` 数据范围 |
| 配置域 | `docs/领域/配置域.md` | 配置不执行业务规则 |
| 商品域 | `docs/领域/商品域.md` | 负责转链与 `pick_source_mapping` |
| 达人域 | `docs/领域/达人域.md` | 维护达人资料与跟进 |
| 寄样域 | `docs/领域/寄样域.md` | 通过订单已同步事件判断交作业完成 |
| 订单域 | `docs/领域/订单域.md` | 只存事实，不算提成 |
| 业绩域 | `docs/领域/业绩域.md` | 最终归属、提成、冲正、双轨金额 |
| 分析模块 | `docs/领域/分析模块.md` | 只读汇总表，不重算归属 |

### 2.3 V1 必不做（10 项）

1. 独家达人 / 商家覆盖
2. 经营毛利口径扩展（按 2026-06-05 用户决策纳入 V1 验收，不扩展为财务结算口径）
3. 个别品负责人覆盖
4. 商品负责人变更历史重算
5. 差异化提成
6. Cookie / 代理池
7. 物流 API 自动跟踪
8. 外部抖店快速寄样 `quick_sample_apply`
9. 数据平台整体导出
10. 不用 mock 数据证明真实闭环

## 3. 技术栈（V1）

| 层 | 选型 | 备注 |
| --- | --- | --- |
| 后端 | Spring Boot 3.2 / Java 17 | 模块化单体，非微服务 |
| 持久化 | PostgreSQL | 配合 Redis 缓存 |
| 缓存 | Redis | 业务缓存与会话 |
| 编排 | Docker Compose | `test` / `real-pre` 两个环境 |
| 前端 | Vue 3 / Vite / TypeScript / Pinia / Naive UI | SPA |
| 验证 | Playwright（E2E） / Maven（Java 单测） / Vitest（前端单测） | 三套均需达到验收口径 |
| 外部依赖 | 抖音 / 抖店开放接口 | 详见 `docs/08-第三方对接总览.md` |

## 4. 不变量

[V1 必做] 强约束，写入 `harness/CURRENT_STATE.md`：

- 订单域只存事实，不算提成，不应用独家覆盖。
- 业绩域负责最终归属、提成、冲正、双轨金额计算。
- 配置域负责配置，不执行具体业务规则。
- 分析模块只读汇总表，不重算业绩归属。
- 用户域统一提供 `self / group / all` 数据范围。
- 寄样域通过订单已同步事件判断交作业完成。
- 商品域负责转链并落 `pick_source_mapping`。
- real-pre 验收不得使用 mock 数据冒充真实闭环。

## 5. 业务关键公式

[V1 必做] 服务费收入 / 收益双轨（按 2026-06-06 用户口径）：

| 指标 | 预估轨 | 结算轨 |
| --- | --- | --- |
| 服务费收入 | 预估订单额 × 服务费率（不扣技术服务费） | 结算订单额 × 服务费率 − 技术服务费 |
| 服务费收益 | 预估服务费收入 − 预估服务费支出 − 技术服务费 | 结算服务费收入 − 结算服务费支出 |
| 毛利 | 服务费收益 − 招商提成 − 媒介/渠道提成 | 同上 |

字段命名（数据契约）：

- `estimate_service_fee` = 预估服务费收入
- `effective_service_fee` = 结算服务费收入
- `estimate_service_profit` = 预估服务费收益
- `effective_service_profit` = 结算服务费收益

## 6. 角色与组织（V1 编码）

| role_code | 含义 | 典型 data_scope |
| --- | --- | --- |
| `admin` | 超级管理员 | 3 (all) |
| `biz_leader` | 招商组长 | 2 (group) |
| `biz_staff` | 招商专员 | 1 (self) |
| `channel_leader` | 渠道组长 | 2 (group) |
| `channel_staff` | 渠道专员 | 1 (self) |
| `ops_staff` | 运营 | 1 (self) |

部门类型（V1 统一）：`department / recruiter_group / channel_group / ops_group`。

历史 `colonel_leader` 已于 2026-05-30 合并至 `biz_leader`（迁移脚本 `backend/src/main/resources/db/alter-role-code-merge-colonel-leader.sql`）。

## 7. 验收 / 部署环境

| 环境 | 用途 | 端口 | 关键开关 |
| --- | --- | --- | --- |
| `test` | Mock 回归基线 | 3000 / 8080 | `APP_TEST_ENABLED=true`, `DOUYIN_TEST_ENABLED=true` |
| `real-pre` | 真实上游 / 生产形态联调 | 3001 / 8081 | `APP_TEST_ENABLED=false`, `DOUYIN_TEST_ENABLED=false`, `DOUYIN_REAL_UPSTREAM_MODE=live` |

部署结论口径：

- 无失败 + 无真实订单 → P0 仍 **PENDING**
- 无失败 + 有真实订单 + 三环通过 → 可升级 **PASS**

## 8. 关键入口命令

| 用途 | 命令 |
| --- | --- |
| V1-P0（mock/test） | `npm run e2e:v1-p0` |
| real-pre P0 预检 | `npm run e2e:real-pre:p0:preflight` |
| real-pre P0 统一验收 | `npm run e2e:real-pre:p0` |
| 后端回归 | `cd backend && mvn test` |
| 前端构建 | `cd frontend && npm run build` |

## 9. 来源与归档

- 主源：`docs/`（当前事实）
- 决策：`docs/决策/ADR-*.md`（注册）
- 验收：`docs/验收/`（登记）
- Harness：`harness/`（强约束）
- 归档：`docs/归档/`（V2.2 旧方案、旧领域设计、local-mock 旧口径、FastAPI/Celery 设想）

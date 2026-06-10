---
kb_id: 00-index
title: 团长SaaS知识库总索引
domain: project
category: index
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
forbidden_misread:
  - 本知识库只描述 V1 状态，绝不把 V2.2 旧方案当 V1 事实
  - 知识库生成到 D:\Docs\Books\my second brain\团长SaaS知识库\，不写入 D:\Projects\SAAS\harness\kb\
  - 知识库不包含任何 secret / token / password / cookie / private key
---

# 团长SaaS知识库总索引

## 1. 仓库与知识库位置

| 项 | 路径 |
| --- | --- |
| 业务项目根 | `D:\Projects\SAAS` |
| Harness 子系统 | `D:\Projects\SAAS\harness\` |
| 知识库根（本文件所在） | `D:\Docs\Books\my second brain\团长SaaS知识库\` |
| 业务事实主源 | `D:\Projects\SAAS\docs\` |
| 决策主源 | `D:\Projects\SAAS\docs\决策\ADR-*.md` |
| 验收主源 | `D:\Projects\SAAS\docs\验收\` |
| 归档主源 | `D:\Projects\SAAS\docs\归档\` |

## 2. 五子系统（按 Harness Engineering 规范）

| 子系统 | 目录 | 主线 | 主入口文件 |
| --- | --- | --- | --- |
| Instructions | `instructions/` | 给 Agent / 人的强约束、合同、门禁、债务 | [instructions-约束指令/00-agent-contract.md](instructions-约束指令/00-agent-contract.md) |
| Tools | `tools/` | 可执行命令、SOP、安全自检脚本 | [tools/00-command-index.md](tools/00-command-index.md) |
| Environment | `environment/` | 部署、端口、环境变量、Compose 映射 | [environment/00-cheatsheet.md](environment/00-cheatsheet.md) |
| State | `state/` | 当前 V1 业务状态、领域状态、债务、决策索引 | [state-状态主源/00-current-state-当前状态与 DDD 计划状态.md](state-状态主源/00-current-state-当前状态与 DDD 计划状态.md) |
| Feedback / Governance | `governance/` | 失败模式、虚假完成清单、债务治理 | [governance/00-failure-modes.md](governance/00-failure-modes.md) |

## 3. 领域（Domains）

| 域 | KB 文件 | 业务合同 | 关键边界 |
| --- | --- | --- | --- |
| 用户域 | [domains/00-user.md](domains/00-user.md) | `docs/领域/用户域.md` | `self/group/all` 数据范围 |
| 配置域 | [domains/01-config.md](domains/01-config.md) | `docs/领域/配置域.md` | 配置不执行业务规则 |
| 商品域 | [domains/02-product.md](domains/02-product.md) | `docs/领域/商品域.md` | 负责转链与 `pick_source_mapping` |
| 达人域 | [domains/03-talent.md](domains/03-talent.md) | `docs/领域/达人域.md` | 维护达人资料与跟进 |
| 寄样域 | [domains/04-sample.md](domains/04-sample.md) | `docs/领域/寄样域.md` | 订单已同步事件驱动交作业 |
| 订单域 | [domains/05-order.md](domains/05-order.md) | `docs/领域/订单域.md` | 只存事实，不算提成 |
| 业绩域 | [domains/06-performance.md](domains/06-performance.md) | `docs/领域/业绩域.md` | 最终归属、提成、冲正、双轨 |
| 分析模块 | [domains/07-analysis.md](domains/07-analysis.md) | `docs/领域/分析模块.md` | 只读汇总，不重算归属 |
| 跨域事件 | [domains/08-cross-domain-events.md](domains/08-cross-domain-events.md) | `docs/04-事件契约总表.md` | 事件总线与契约 |

## 4. 流程（Workflows）

| 流程 | KB 文件 | 业务合同 | 入口命令 |
| --- | --- | --- | --- |
| 渠道主链路 | [workflows/01-channel-main.md](workflows/01-channel-main.md) | `docs/流程/渠道主链路.md` | `npm run e2e:v1-p0` |
| 招商主链路 | [workflows/02-recruiter-main.md](workflows/02-recruiter-main.md) | `docs/流程/招商主链路.md` | `npm run e2e:v1-p0` |
| 管理主链路 | [workflows/03-management-main.md](workflows/03-management-main.md) | `docs/流程/管理主链路.md` | `npm run e2e:v1-p0` |
| 订单归因链路 | [workflows/04-order-attribution.md](workflows/04-order-attribution.md) | `docs/流程/订单归因链路.md` | `npm run e2e:v1-p0` |
| 业绩计算链路 | [workflows/05-performance-calculation.md](workflows/05-performance-calculation.md) | `docs/流程/业绩计算链路.md` | `npm run e2e:v1-p0` |
| 寄样交作业链路 | [workflows/06-sample-delivery.md](workflows/06-sample-delivery.md) | `docs/流程/寄样交作业链路.md` | `npm run e2e:v1-p0` |
| real-pre 联调 | [workflows/07-real-pre-handshake.md](workflows/07-real-pre-handshake.md) | `docs/验收/real-pre联调手册.md` | `npm run e2e:real-pre:p0` |
| E2E 浏览器验收 | [workflows/08-e2e-browser.md](workflows/08-e2e-browser.md) | `docs/验收/E2E浏览器测试手册.md` | `npm run e2e:v1-p0` |

## 5. 证据（Evidence）

| KB 文件 | 业务合同 | 登记字段 |
| --- | --- | --- |
| [evidence/00-pass-2026-05-26.md](evidence/00-pass-2026-05-26.md) | `docs/验收/验收证据索引.md` | 1591/0, 52/213, build PASS |
| [evidence/01-pending-2026-05-26.md](evidence/01-pending-2026-05-26.md) | `docs/验收/验收证据索引.md` | product=0, mapping=0, PENDING_PICK_SOURCE |
| [evidence/02-manual-copy-dialog-2026-06-01.md](evidence/02-manual-copy-dialog-2026-06-01.md) | `docs/验收/验收证据索引.md` | ManualCopyDialog 284 字符 |
| [evidence/03-filter-audit-2026-06-02.md](evidence/03-filter-audit-2026-06-02.md) | `docs/验收/筛选代码审计-20260602.md` | 2 commits, 6 uncommitted |
| [evidence/04-real-pre-deployment-conclusion.md](evidence/04-real-pre-deployment-conclusion.md) | `docs/验收/real-pre联调手册.md` | 无失败+无真实订单 → PENDING |
| [evidence/05-block-state-taxonomy.md](evidence/05-block-state-taxonomy.md) | `harness/FORBIDDEN_SCOPE.md` | DONE/PARTIAL/BLOCKED_*/FAILED/RISK_ACCEPTED |

## 6. 治理（Governance）

| KB 文件 | 业务合同 | 主线 |
| --- | --- | --- |
| [governance/00-failure-modes.md](governance/00-failure-modes.md) | `harness/FORBIDDEN_SCOPE.md` | 虚假完成 / 脏退出 / 错口径 |
| [governance/01-debt-register.md](governance/01-debt-register.md) | `harness/HARNESS_DEBT.md` | 25 项债务治理 |
| [governance/02-changelog-rules.md](governance/02-changelog-rules.md) | `harness/HARNESS_CHANGELOG.md` | Harness 变更登记 |
| [governance/03-secret-policy.md](governance/03-secret-policy.md) | `harness/SECURITY.md` | 密钥扫描与输出隔离 |
| [governance/04-git-worktree-rules.md](governance/04-git-worktree-rules.md) | `harness/skills/git-change-control.md` | Intake / Exit / Batch Gate |
| [governance/05-report-conventions.md](governance/05-report-conventions.md) | `harness/reports/` 命名 | 报告前缀与登记规范 |

## 7. DDD 重构计划

| 入口 | 路径 | 说明 |
| --- | --- | --- |
| DDD 计划总入口 | [plans/ddd-refactor/00-index.md](plans/ddd-refactor/00-index.md) | 后续 Agent 优先读取 |
| 总路线图 | [plans/ddd-refactor/01-master-roadmap.md](plans/ddd-refactor/01-master-roadmap.md) | Phase 0-7 渐进路线 |
| 任务矩阵 | [plans/ddd-refactor/02-task-matrix.md](plans/ddd-refactor/02-task-matrix.md) | A-F 类任务拆分 |
| 第一批任务卡 | [plans/ddd-refactor/tasks/00-task-index.md](plans/ddd-refactor/tasks/00-task-index.md) | 从跨域审查开始 |

当前进入 DDD 渐进式重构规划阶段；V1 业务口径、接口契约和数据库结构默认不变。

## 8. 速读路径

新任务 / 新成员建议顺序：

1. [01-project-overview.md](01-project-overview.md)
2. [instructions-约束指令/03-forbidden-scope-禁做范围与失败模式.md](instructions-约束指令/03-forbidden-scope-禁做范围与失败模式.md)
3. [state-状态主源/00-current-state-当前状态与 DDD 计划状态.md](state-状态主源/00-current-state-当前状态与 DDD 计划状态.md)
4. [domains/](domains/) → 命中本任务的域
5. [workflows/](workflows/) → 命中本任务的流程
6. [evidence/](evidence/) → 命中本任务的证据
7. [governance/](governance/) → 失败模式 / 债务 / 提交门禁

## 9. 关键事实快照（不替代 evidence）

- V1 范围：3 主链（渠道 / 招商 / 管理）+ 8 域。
- 8 域：用户 / 配置 / 商品 / 达人 / 寄样 / 订单 / 业绩 / 分析。
- V1 必不做：独家达人/商家、差异化提成、物流 API 自动跟踪、外部 `quick_sample_apply`、数据平台整体导出、Cookie/代理池。
- 服务费双轨（2026-06-06）：
  - 预估服务费收入 = 预估订单额 × 服务费率
  - 结算服务费收入 = 结算订单额 × 服务费率 − 技术服务费
  - 预估服务费收益 = 预估服务费收入 − 预估服务费支出 − 技术服务费
  - 结算服务费收益 = 结算服务费收入 − 结算服务费支出
  - 毛利 = 服务费收益 − 招商提成 − 媒介/渠道提成
- 角色编码：admin / biz_leader / biz_staff / channel_leader / channel_staff / ops_staff。
- 部门类型：department / recruiter_group / channel_group / ops_group。
- 合法状态：DONE / DONE_WITH_REGISTERED_DIRTY / PARTIAL / BLOCKED_BY_SAMPLE / BLOCKED_BY_EXTERNAL / FAILED / RISK_ACCEPTED_BY_USER。

## 10. 不变量（[V1 必做]）

- 订单域只存事实，不算提成，不应用独家覆盖。
- 业绩域负责最终归属、提成、冲正、双轨金额计算。
- 配置域负责配置，不执行具体业务规则。
- 分析模块只读汇总表，不重算业绩归属。
- 用户域统一提供 `self / group / all` 数据范围。
- 寄样域通过订单已同步事件判断交作业完成。
- 商品域负责转链并落 `pick_source_mapping`。
- real-pre 验收不得使用 mock 数据冒充真实闭环。

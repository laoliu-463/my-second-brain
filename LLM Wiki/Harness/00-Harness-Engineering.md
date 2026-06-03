# Harness Engineering

抖音团长 SaaS 的 AI Agent 工程执行系统。把后续 Agent 修改代码后的固定流程沉淀为脚本、清单、模板和证据入口。

## 五个子系统

| 子系统 | 路径 | 作用 |
|---|---|---|
| Instructions | `instructions/`、`AGENT_CONTRACT.md`、`FORBIDDEN_SCOPE.md` | 项目规则、V1 边界、禁止事项、完成标准 |
| Tools | `commands/`、`tools/README.md` | 构建、重启、验证、部署、报告、复盘 |
| Environment | `environment/` | test、real-pre、remote real-pre 和 compose 边界 |
| State | `CURRENT_STATE.md`、`state/`、`HARNESS_CHANGELOG.md` | 当前状态、风险、证据、版本 |
| Feedback | `feedback/`、`evals/`、`reports/` | 验收、证据报告、复盘和 Harness 升级闭环 |

## 核心入口

| 入口 | 路径 |
|---|---|
| 执行合同 | `harness/AGENT_CONTRACT.md` |
| 当前状态 | `harness/CURRENT_STATE.md` |
| 任务路由 | `harness/TASK_ROUTING.md` |
| 禁止范围 | `harness/FORBIDDEN_SCOPE.md` |
| 领域地图 | `harness/DOMAIN_MAP.md` |
| Completion Gates | `harness/COMPLETION_GATES.md` |
| Session Exit Gate | `harness/SESSION_EXIT_GATE.md` |

## 任务入口索引

| 任务 | 入口 |
|---|---|
| 后端变更 | `TASK_ROUTING.md`、`runbooks/backend-change.md` |
| 前端变更 | `TASK_ROUTING.md`、`runbooks/frontend-change.md` |
| 数据库变更 | `TASK_ROUTING.md`、`runbooks/database-change.md` |
| Docker 操作 | `environment/docker-compose-map.md`、`runbooks/docker-compose-operations.md` |
| 测试验收 | `runbooks/test-validation.md`、`evals/` |
| 第三方联调 | `runbooks/third-party-integration.md`、`skills/real-pre-debug.skill.md` |
| 任务收尾 / GC | `runbooks/closeout-and-gc.md`、`feedback/garbage-collection-policy.md` |

## 总命令入口

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\harness\commands\agent-do.ps1 -Env real-pre -Scope full -Message "说明本次修改"
```

`agent-do.ps1` 和主要子命令默认 `Env=real-pre`。`test` 只作为显式指定的专项验证环境；远端部署仍必须显式传 `-DeployRemote true`。

## Harness 与 DDD 的分工

- `docs/03-领域架构总览.md` 和 `docs/领域/*.md` 负责定义 DDD 边界、领域职责和禁止越界项。
- `harness/plans/DDD_OPTIMIZATION_ROADMAP.md` 负责记录 DDD 优化顺序、阶段目标、验收标准和执行原因。
- `harness/plans/DDD_DOMAIN_TASK_MATRIX.md` 负责记录各领域任务卡，不代表任务已经完成。
- `harness/TASK_ROUTING.md` 负责把任务路由到对应领域、Scope、runbook 和验证入口。
- Harness 不新增业务规则；发现业务冲突时，必须回到 `docs/决策/ADR-002-V1范围优先级.md` 或对应领域主源处理。

## 版本

- 当前 Harness 版本：v0.4.0（2026-06-03）
- 记录在 `harness/CURRENT_STATE.md`

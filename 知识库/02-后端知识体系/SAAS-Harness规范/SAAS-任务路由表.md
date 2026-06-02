---
title: SAAS 任务路由表
tags: [harness, saas, 任务路由]
created: 2026-06-02
updated: 2026-06-02
sources: [D:\Projects\SAAS/harness/TASK_ROUTING.md]
---

# SAAS 任务路由表

## 任务类型分流

| 任务类型 | 默认 Scope | 常用命令 |
|---|---|---|
| 后端功能修改/修复 | `backend` | `agent-do.ps1 -Scope backend` |
| 前端功能修改/修复 | `frontend` | `agent-do.ps1 -Scope frontend` |
| 数据库结构变更 | `backend` 或 `full` | `agent-do.ps1 -Scope backend` |
| 接口联调 | `full` | `agent-do.ps1 -Scope full` |
| 第三方 API 联调 | `full` | `npm run e2e:real-pre:p0:preflight` |
| Docker/容器/服务重启 | 按任务 | `restart-compose.ps1`、`verify-local.ps1` |
| 本地部署/real-pre 变更 | `full` | `agent-do.ps1 -Scope full` |
| 远端部署 | `full` | 只有用户明确要求才加 `-DeployRemote true` |
| 测试与验收 | 按任务 | `npm run e2e:v1-p0`、`mvn test` |
| 业务规则修改 | `full` | 按领域选择 Scope |
| Bug 排查 | 先不定 | 先收集日志/API/DB 证据，再选 Scope |
| 文档/Harness 调整 | `docs` | `agent-do.ps1 -Scope docs` |
| 权限/数据范围 | `full` | `npm run e2e:real-pre:roles` |

## 领域判断

| 关键词/现象 | 主责领域 |
|---|---|
| 登录、权限、菜单、角色、组织、数据范围 | 用户域 |
| 系统配置、规则参数、提成比例、复制模板、`pick_extra` | 配置域 |
| 订单同步、`pick_source`、`colonel_buyin_id`、默认归因、`raw_payload`、双轨金额输入 | 订单域 |
| `performance_records`、提成、冲正、最终归属 | 业绩域 |
| 看板、汇总表、趋势、排行、对账 | 分析模块 |
| 商品库、活动商品、展示规则、转链、`pick_source_mapping` | 商品域 |
| 达人、认领、保护期、地址、标签 | 达人域 |
| 寄样申请、审核、发货、签收、待交作业、交作业完成 | 寄样域 |

## DDD 任务必读顺序

当任务涉及 DDD、领域边界、业务规则下沉、跨域依赖治理、Facade 收口、事件解耦或前端领域化时，必须先读：

1. `harness/AGENT_CONTRACT.md`
2. `harness/FORBIDDEN_SCOPE.md`
3. `harness/plans/DDD_OPTIMIZATION_ROADMAP.md`
4. `harness/plans/DDD_DOMAIN_TASK_MATRIX.md`
5. 当前领域对应的 `harness/instructions/*.md`
6. 当前领域对应的 `docs/领域/*.md`

## 固定命令入口

```powershell
# 文档/Harness 变更
powershell -NoProfile -ExecutionPolicy Bypass -File .\harness\commands\agent-do.ps1 -Env real-pre -Scope docs -Message "docs: update harness"

# 后端变更
powershell -NoProfile -ExecutionPolicy Bypass -File .\harness\commands\agent-do.ps1 -Env real-pre -Scope backend -Message "fix: update backend logic"

# 前端变更
powershell -NoProfile -ExecutionPolicy Bypass -File .\harness\commands\agent-do.ps1 -Env real-pre -Scope frontend -Message "fix: update frontend flow"

# real-pre 全链路验证
powershell -NoProfile -ExecutionPolicy Bypass -File .\harness\commands\agent-do.ps1 -Env real-pre -Scope full -Message "fix: update real-pre flow"

# 远端部署（用户明确要求时）
powershell -NoProfile -ExecutionPolicy Bypass -File .\harness\commands\agent-do.ps1 -Env real-pre -Scope full -DeployRemote true -Message "deploy: real-pre update"

# 安全检查
powershell -NoProfile -ExecutionPolicy Bypass -File .\harness\commands\safety-check.ps1 -Env real-pre -Scope docs -DryRun

# 旧内容维护候选计划
powershell -NoProfile -ExecutionPolicy Bypass -File .\harness\commands\retire-content.ps1 -Action Plan -DryRun
```

## 相关概念
- [[SAAS-Harness规范总览]]
- [[SAAS-DDD优化路线图]]
- [[SAAS-领域状态跟踪]]

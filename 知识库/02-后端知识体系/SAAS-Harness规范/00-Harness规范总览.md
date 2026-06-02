---
title: SAAS Harness 规范总览
tags: [harness, saas, ddd, 工程规范]
created: 2026-06-02
updated: 2026-06-02
sources: [D:\Projects\SAAS/harness/README.md, D:\Projects\SAAS/harness/CURRENT_STATE.md]
---

# SAAS Harness 规范总览

## 概述

SAAS 项目（`D:\Projects\SAAS`）的 AI Agent 执行系统。将代码修改后的固定流程（构建、重启、验证、取证、提交、部署）沉淀为脚本、清单、模板和证据入口，确保每次操作可复盘、可追溯。

## 五大子系统

| 子系统 | 路径 | 作用 |
|---|---|---|
| Instructions | `instructions/`、`AGENT_CONTRACT.md`、`FORBIDDEN_SCOPE.md` | 项目规则、V1边界、禁止事项、完成标准 |
| Tools | `commands/`、`tools/README.md` | 构建、重启、验证、部署、报告 |
| Environment | `environment/` | test、real-pre、remote real-pre 和 compose 边界 |
| State | `CURRENT_STATE.md`、`state/`、`HARNESS_CHANGELOG.md` | 当前状态、风险、证据、版本 |
| Feedback | `feedback/`、`evals/`、`reports/` | 验收、证据报告、复盘 |

## 核心文件索引

| 文件 | 作用 |
|---|---|
| `harness/README.md` | Harness 目录地图 |
| `harness/CURRENT_STATE.md` | 当前技术栈、环境事实、DDD 合并状态 |
| `harness/TASK_ROUTING.md` | 任务类型 -> 领域/skill/验证 的分流表 |
| `harness/AGENT_CONTRACT.md` | Agent 执行合同、DoD、证据优先级 |
| `harness/FORBIDDEN_SCOPE.md` | V1/real-pre/Git/密钥/模块边界禁止项 |
| `harness/DOMAIN_MAP.md` | 七域 + 分析模块职责地图、三条主链 |
| `harness/state/DOMAIN_STATUS.md` | 各领域 DDD 优化状态、P0/P1 标记 |
| `harness/plans/DDD_OPTIMIZATION_ROADMAP.md` | DDD 优化 13 阶段路线图 |
| `harness/plans/DDD_DOMAIN_TASK_MATRIX.md` | 各领域任务卡索引（共 218 个任务） |

## 执行入口

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\harness\commands\agent-do.ps1 -Env real-pre -Scope full -Message "说明本次修改"
```

| Scope | 含义 |
|---|---|
| `full` | 全链路：构建 + 重启 + 健康 + 验证 + evidence |
| `backend` | 后端变更：构建 + 重启 + 后端健康 |
| `frontend` | 前端变更：前端构建 + 前端健康 |
| `docs` | 文档变更：跳过构建和重启 |

远端部署只有用户明确要求时加：`-DeployRemote true`

## 完成标准（Definition of Done）

只有同时满足以下条件，才允许声明任务完成：

1. 代码或文档已修改
2. 构建通过，或 `Scope=docs` 明确跳过构建
3. 对应 Docker 服务已重启，或 `Scope=docs` 明确不需要重启
4. 健康检查通过，或明确记录阻塞原因
5. 相关业务验证通过，或明确记录 `BLOCKED` / `PENDING` / `FAIL` 证据
6. 已生成旧内容维护计划，或明确说明本轮无需整理归档删除
7. 已生成 `harness/reports/evidence-*.md`
8. Git commit 已生成并 push 到当前分支上游，或明确说明本轮被用户要求不提交/不推送
9. 若用户明确要求远端部署，远端部署完成并记录远端健康检查
10. 已生成 `harness/reports/retro-*.md`，或明确说明本次无需 Harness 升级
11. 剩余风险已列出

## 状态结论口径

| 状态 | 含义 |
|---|---|
| `PASS` | 验证已执行且证据完整 |
| `PARTIAL` | 部分验证通过，仍有明确未验证项或阻塞项 |
| `BLOCKED` | 外部 Token、权限包、真实样本、远端权限等阻塞 |
| `PENDING` | 未执行或样本不足，不能写成通过 |
| `FAIL` | 已复现失败，需要继续修复或回滚 |

## 证据优先级

1. 自动化测试报告
2. API 响应
3. SQL 查询结果
4. 容器日志 / 后端日志
5. 页面截图 / 浏览器 Network
6. 人工描述（不得用人工描述替代可运行脚本/SQL/API/日志证据）

## 关键禁止事项

### real-pre 绝对禁止
- 禁止清库、禁止 `docker compose down -v`、禁止删除 volume
- 禁止把 real-pre 改成 test/mock
- 禁止打开 `APP_TEST_ENABLED=true`、`DOUYIN_TEST_ENABLED=true`
- 禁止把 `DOUYIN_REAL_UPSTREAM_MODE` 改成非 `live`
- 禁止用 mock 数据证明真实业务闭环

### 领域边界禁止
- 订单域不得计算提成、不得写 `performance_records`、不得直接更新寄样完成状态
- 业绩域不得同步抖音订单、不得修改订单原始事实
- 分析模块不得重算业绩归属
- Controller 不得编排复杂业务规则或状态机
- 禁止跨领域直接访问对方 Repository

### Git/密钥禁止
- 禁止提交 `.env`、`.env.real-pre`、`.env.test`
- 禁止提交 `*.pem`、`*.key`、私钥、凭证
- 禁止输出 Token、密码、OAuth code

## 相关概念
- [[SAAS-DDD优化路线图]]
- [[SAAS-任务路由表]]
- [[SAAS-领域状态跟踪]]

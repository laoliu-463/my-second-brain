---
kb_id: instructions/00-agent-contract
title: Agent 工作合同
domain: instructions
category: contract
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/AGENT_CONTRACT.md
  - harness/CURRENT_STATE.md
  - harness/FORBIDDEN_SCOPE.md
related_reports: []
forbidden_misread:
  - 本合同不替代 FORBIDDEN_SCOPE.md，冲突时以 FORBIDDEN_SCOPE.md 为准
---

# Agent 工作合同

## 1. 目的

定义本仓库 Agent（无论是 Claude / Codex / 本地脚本 / 子代理）在执行任务时必须遵守的最低工作合同。Agent 在 `harness/AGENT_CONTRACT.md` 之上不得新增"自由裁量权"。

## 2. 范围

- 适用于所有对 `D:\Projects\SAAS\` 下的代码、文档、配置、数据库、容器、远端环境产生直接 / 间接影响的 Agent 操作。
- 不适用于纯阅读、纯搜索、对外部网站（不带凭据）的只读查询。

## 3. 角色与责任

| 主体 | 责任 |
| --- | --- |
| 主 Agent | 解释用户请求、调度子 Agent、检查交付、对接人类 |
| 子 Agent（planner / tdd-guide / code-reviewer / security-reviewer / 等） | 单一职责，不跨阶段自由发挥 |
| 人类 Owner | 最终拍板，承担 `RISK_ACCEPTED_BY_USER` |

## 4. 工作流

1. **Git Intake Gate**：工作区脏（`git status` 存在未登记）→ 先登记或收口，不得直接开新任务。
2. **识别任务域**：命中 `docs/领域/` 哪个域？命中 `docs/流程/` 哪条链？命中 `docs/验收/` 哪一项？
3. **读取当前事实**：`docs/` 主源 + `harness/CURRENT_STATE.md` + `harness/FORBIDDEN_SCOPE.md`。
4. **写实现 / 文档**：严格遵守领域边界与 FORBIDDEN_SCOPE。
5. **生成证据**：脚本输出、API/SQL 结果、文件路径三类之一。
6. **Git Exit Gate**：按任务编号或 batch 编号拆分 commit；未授权禁止 `git add .` / `--amend` / `--no-verify`。
7. **Session Exit Gate**：在 `harness/reports/` 输出 `DONE_CLEAN` / `DONE_WITH_REGISTERED_DIRTY` / `PARTIAL_DIRTY_REMAINING` / `BLOCKED_DIRTY_UNKNOWN` 之一。

## 5. 不可越界清单（与 FORBIDDEN_SCOPE 联动）

- 不得修改 Java / Vue / SQL migration / Docker / env / Nginx / 部署脚本（除非本任务明确授权）。
- 不得执行数据库写操作。
- 不得重启容器、不得远端部署。
- 不得 `git add .` / 混批 commit。
- 不得把 mock 数据说成 real-pre 真实闭环。
- 不得把 BLOCKED / PENDING 状态写成 PASS。
- 不得在输出中泄露 token / client_secret / password / cookie / private key。

## 6. 完成状态机

合法状态（详 [state/04-domain-status.md](state/04-domain-status.md)）：

- `DONE`
- `DONE_WITH_REGISTERED_DIRTY`
- `PARTIAL_DIRTY_REMAINING`
- `BLOCKED_BY_SAMPLE`
- `BLOCKED_BY_EXTERNAL`
- `FAILED`
- `RISK_ACCEPTED_BY_USER`

非法状态：把上述任一非 PASS 状态包装为 PASS。

## 7. 失败模式

- 未读 FORBIDDEN_SCOPE 就行动 → 立即停。
- 未生成证据就声明完成 → 立即停。
- 脏工作区未登记就开新任务 → 立即停。
- 同一 Agent 既生成又验证 → 引入"新视角"重审。

## 8. 与 Harness 子系统对齐

- 本合同是 Instructions 子系统的"宪法"。
- Tools / Environment / State / Governance 子系统都不得与本合同冲突；冲突时升级到 Owner 拍板。

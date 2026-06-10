---
kb_id: instructions/06-task-routing
title: 任务路由与 Agent 调度
domain: instructions
category: routing
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/AGENT_CONTRACT.md
  - docs/01-V1交付范围与边界.md
  - harness/HARNESS_DEBT.md
related_reports: []
forbidden_misread:
  - Agent 不得跨职责自由发挥；子 Agent 必须单一职责
  - 创建与验证必须分给两个不同 Agent
---

# 任务路由与 Agent 调度

## 1. 目的

定义主 Agent 接收任务后，如何把任务路由到对应的子 Agent / 文档主源 / 工具入口，并保证"创建者 ≠ 验证者"。

## 2. 任务分类矩阵

| 任务类型 | 主源 | 主 Agent | 验证 Agent | 工具入口 |
| --- | --- | --- | --- | --- |
| 业务代码变更 | `docs/领域/<hit>.md` | code-architect / tdd-guide | code-reviewer | `cd backend && mvn test` |
| 业务文档同步 | `docs/领域/<hit>.md` | doc-updater | 主 Agent | – |
| 数据库 / Migration | `docs/06-数据模型总表.md` | database-reviewer | code-reviewer | `cd backend && mvn test` |
| E2E 流程 | `docs/流程/<hit>.md` | e2e-runner | 主 Agent | `npm run e2e:v1-p0` |
| real-pre 联调 | `docs/验收/real-pre联调手册.md` | 主 Agent | 主 Agent | `npm run e2e:real-pre:p0:preflight` |
| 性能 / 内存 | 业务域 | performance-optimizer | code-reviewer | Profiler |
| 安全 / 密钥 | `docs/决策/ADR-*.md` | security-reviewer | 主 Agent | – |
| 大型重构 | 多域 | planner + code-architect | 独立子 Agent | – |
| 死代码清理 | 全部 | refactor-cleaner | code-reviewer | knip / ts-prune |
| 部署 / 端口 | `harness/environment/*` | 主 Agent | 独立子 Agent | – |
| Harness 规则变更 | `harness/*` | 主 Agent | 独立子 Agent | – |

## 3. 路由决策树

1. 任务是否涉及业务代码？
   - 是 → 主源 = `docs/领域/<hit>.md`，主 Agent = tdd-guide / code-architect
   - 否 → 继续
2. 任务是否涉及数据库 / Schema？
   - 是 → 主源 = `docs/06-数据模型总表.md`，主 Agent = database-reviewer
   - 否 → 继续
3. 任务是否涉及 E2E / 真实上游？
   - 是 → 主源 = `docs/流程/<hit>.md` 或 `docs/验收/real-pre联调手册.md`，主 Agent = e2e-runner
   - 否 → 继续
4. 任务是否涉及 Harness 规则？
   - 是 → 主源 = `harness/FORBIDDEN_SCOPE.md` / `harness/CURRENT_STATE.md`，主 Agent = 主 Agent
   - 否 → 默认路由到 planner

## 4. 创建者 ≠ 验证者

- 任何业务 / 文档 / 配置修改后，必须有独立子 Agent 验证。
- 验证 Agent 不得复用生成 Agent 的同一次会话上下文（避免"生成者偏差"）。
- 验证 Agent 必须有独立的 evidence 路径。

## 5. 多 Agent 并行场景

仅在以下场景允许并行：

- 多域无耦合修改（如：用户域 + 配置域）
- 多视角验证（factual / security / performance / consistency）
- 多份独立证据生成（脚本 / API / 截图）

禁止并行：

- 同一域内串行修改（必须先 G0→G1→G2→G3→G4）
- 共享同一只读主源（避免竞态读取）

## 6. 路由冲突仲裁

| 冲突类型 | 仲裁规则 |
| --- | --- |
| 主源冲突 | 优先 `harness/CURRENT_STATE.md` > `docs/决策/ADR-*.md` > `docs/领域/<hit>.md` |
| Agent 冲突 | 优先分工表 > 经验判断 |
| 工具冲突 | 优先项目内已有工具 > 临时下载 |
| 状态冲突 | 优先 `DOMAIN_STATUS.md` > 报告 |

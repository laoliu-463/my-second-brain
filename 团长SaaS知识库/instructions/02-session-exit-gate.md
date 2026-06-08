---
kb_id: instructions/02-session-exit-gate
title: Session 退出门禁
domain: instructions
category: gates
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/CURRENT_STATE.md
  - harness/FORBIDDEN_SCOPE.md
related_reports: []
forbidden_misread:
  - 退出前必须输出状态码；不得以"已继续下一任务"替代状态码
  - 5 条硬约束任一未满足即不得退出
---

# Session 退出门禁

## 1. 目的

为每次 Agent 会话结束定义最低退出条件。退出前必须满足 5 条硬约束 + 1 个状态码，否则属于"脏状态退出"。

## 2. 5 条硬约束

| 序号 | 约束 | 检查方法 |
| --- | --- | --- |
| C1 | 所有 build / test 失败已说明 | 退出前运行 `mvn test` 与 `npm run build`，失败必须登记到本任务报告或 `docs/验收/验收证据索引.md` |
| C2 | 所有容器 / 端口 / 配置异常已说明 | 退出前 `docker compose ps`，异常必须登记 |
| C3 | 所有临时文件 / debug 残留 / TODO 无归属已清理 | `git status --short` 与 `git diff --stat` 自检 |
| C4 | 所有修改已同步到 `docs/` 与 `harness/` 相应文件 | 检索本次会话修改集，对照 `docs/领域/`、`docs/流程/`、`docs/决策/`、`harness/CURRENT_STATE.md` |
| C5 | 已有最终 Session Exit Report | 写入 `harness/reports/<session-id>-exit-<date>-<time>.md` |

## 3. 7 选 1 退出状态码

| 状态 | 含义 | 后续动作 |
| --- | --- | --- |
| `DONE_CLEAN` | 工作区干净，所有门禁通过 | 提交、推送（按授权） |
| `DONE_WITH_REGISTERED_DIRTY` | 任务完成但工作区有已登记 dirty | 不得再开新任务；先收口 |
| `PARTIAL_DIRTY_REMAINING` | 部分完成，存在待处理 dirty | 不允许 commit / push / deploy |
| `BLOCKED_BY_SAMPLE` | 缺真实样本（商品/订单/达人/转链） | 等待真实样本 |
| `BLOCKED_BY_EXTERNAL` | 外部不可用（抖店授权 / Token / 上游接口） | 等待外部恢复 |
| `FAILED` | 任务失败，原因可追溯 | 回退或升 Owner |
| `RISK_ACCEPTED_BY_USER` | 用户接受风险并继续 | 必须有用户明确授权记录 |

## 4. 退出检查清单

退出前 30 秒内必须自检：

- [ ] `git status --short` 结果已记录
- [ ] 所有 build / test 失败已说明
- [ ] 所有异常容器 / 端口 / 配置已说明
- [ ] 临时文件 / debug 残留 / 无归属 TODO 已清理
- [ ] 修改的 docs / harness 路径已列出
- [ ] Session Exit Report 已写
- [ ] 状态码已选定并记录

## 5. 退出报告最小内容

```text
# Session Exit Report

- session_id: <id>
- task_ids: [<id>, ...]
- branches: [<branch>]
- status_code: DONE_CLEAN | DONE_WITH_REGISTERED_DIRTY | PARTIAL_DIRTY_REMAINING | BLOCKED_BY_SAMPLE | BLOCKED_BY_EXTERNAL | FAILED | RISK_ACCEPTED_BY_USER
- evidence: <path | none>
- dirty: <list | none>
- forbidden_touched: <yes/no>
- followups: <list>
- owner_signoff: <yes/no>
```

## 6. 失败处理

| 检查项 | 失败动作 |
| --- | --- |
| C1 未通过 | 立即补修；无法补修则状态码 = `FAILED` |
| C2 未通过 | 登记异常 → 状态码 = `PARTIAL_DIRTY_REMAINING` |
| C3 未通过 | 先清理；无法清理则 `BLOCKED_DIRTY_UNKNOWN` |
| C4 未通过 | 先补文档；无法补则 `PARTIAL_DIRTY_REMAINING` |
| C5 未通过 | 立即写报告；无法写则任务本身不成立 |

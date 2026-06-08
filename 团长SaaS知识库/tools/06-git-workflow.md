---
kb_id: tools/06-git-workflow
title: Git 工作流工具
domain: tools
category: git
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/state/DECISIONS.md
  - docs/决策/ADR-*.md
  - harness/CURRENT_STATE.md
related_reports:
  - harness/reports/git-harness-001-worktree-governance-20260603-*.md
forbidden_misread:
  - 禁止 `git add .` / `git add -A` / `git add <dir>/`
  - 禁止 `git push --force` 到 main / master
  - 禁止 `git commit --amend` 无授权
  - 禁止 `--no-verify` 无授权
---

# Git 工作流工具

## 1. 主源

- `harness/state/DECISIONS.md`
- `docs/决策/ADR-002-V1范围优先级.md`

## 2. 仓库拓扑

| 远程 | 用途 |
| --- | --- |
| Gitee | 主仓库（国内） |
| GitHub | 镜像 / 备份 |

分支：

- `main` / `master`：受保护
- `feature/<name>`：开发
- `release/<name>`：发布（按需）
- `hotfix/<name>`：紧急修复（按需）

## 3. 常用命令

```bash
# 状态
git status --short
git diff --stat

# 添加（明确文件）
git add <file1> <file2>

# 提交（conventional commits）
git commit -m "feat: 新增..."

# 推送（按授权）
git push origin feature/auth-system
```

## 4. 工作区治理决策（git-harness-001）

- 工作区存在 `unknown dirty` → 不得进入任何 commit / push / deploy
- 已登记 dirty（`REGISTERED_DIRTY`）可以提交，但必须显式声明
- PARTIAL 状态不得 commit
- 一次任务一个 commit，混批 commit 禁止

## 5. 禁忌命令

| 命令 | 原因 |
| --- | --- |
| `git add .` | 误带 secret |
| `git add -A` | 同上 |
| `git add <dir>/` | 范围过大 |
| `git commit --amend` | 破坏已推送 |
| `git push --force` to main | 覆盖上游 |
| `git reset --hard` | 丢未提交 |
| `git checkout .` | 覆盖工作区 |
| `git clean -fd` | 删未跟踪 |

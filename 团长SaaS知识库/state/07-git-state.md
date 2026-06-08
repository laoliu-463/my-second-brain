---
kb_id: state/07-git-state
title: Git 工作区状态
domain: state
category: state-git
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/CURRENT_STATE.md
  - docs/04-事件契约总表.md
related_reports: []
forbidden_misread:
  - unknown dirty 禁入 commit
  - 一次任务一个 commit
---

# Git 工作区状态

## 1. 工作区状态类型

| 状态 | 含义 | 是否可 commit |
| --- | --- | --- |
| CLEAN | 无未跟踪 / 修改 | ✅ |
| REGISTERED_DIRTY | 已知未跟踪（如 harness/reports/） | ✅（需声明） |
| UNKNOWN_DIRTY | 未知修改 | ❌ |
| PARTIAL | 任务只完成部分 | ❌ |

## 2. 决策依据（git-harness-001）

- CLEAN：直接 commit
- REGISTERED_DIRTY：声明后 commit
- UNKNOWN_DIRTY：先 `git status --short` 排查
- PARTIAL：不 commit；继续任务或拆任务

## 3. 当前分支

- 主干: main / master（受保护）
- 当前: feature/auth-system
- 备份: GitHub 镜像

## 4. commit 规则

```bash
git add <file1> <file2>   # 显式文件
git commit -m "type: description"
```

## 5. 禁忌

- `git add .` / `git add -A` / `git add <dir>/`
- `git commit --amend`（未授权）
- `git push --force` 到 main
- `git reset --hard`
- 混批（多任务）提交
- `--no-verify`

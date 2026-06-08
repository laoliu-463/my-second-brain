---
kb_id: tools/08-vcs-protection
title: 受保护路径与防误删
domain: tools
category: protection
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/FORBIDDEN_SCOPE.md
  - harness/CURRENT_STATE.md
related_reports: []
forbidden_misread:
  - 受保护路径不得"清理"或"瘦身"
  - 受保护文件不得"折叠"到主源
---

# 受保护路径与防误删

## 1. 目的

登记本仓库内任何 Agent / 工具不得随意修改、删除、移出、覆盖的路径与文件。

## 2. 受保护路径

| 路径 | 原因 |
| --- | --- |
| `.env` / `.env.*` | 密钥 |
| `nginx/*.conf` | 反代 / 路由 |
| `docker-compose.real-pre.yml` | real-pre 部署 |
| `docs/决策/ADR-*.md` | 已决议 |
| `harness/FORBIDDEN_SCOPE.md` | 禁做主源 |
| `harness/HARNESS_DEBT.md` | 债务登记 |
| `harness/state/DECISIONS.md` | 决策登记 |
| `harness/state/CURRENT_STATE.md` | 当前事实 |
| `harness/state/DOMAIN_STATUS.md` | 域状态 |
| `*.pem` / `*.key` | 私钥 |
| `*.sql`（migration） | 数据库迁移 |

## 3. 受保护 SQL migration

- `backend/src/main/resources/db/migration/V*.sql` 一律视为受保护
- 任何修改必须新增 V(N+1)__*.sql 增量脚本
- 不得编辑历史 V* 脚本

## 4. 受保护配置

- `application.yml` / `application-*.yml` 受保护
- 修改必须先 ADR
- 测试 / mock 配置受同等保护

## 5. 防误删原则

- 任何 `rm / rd / del` 命令必须先列文件再确认
- 任何 `git clean -fd` 必须先 `git status --short`
- 任何 `git reset --hard` 必须先 `git status` + `git diff --stat`
- 任何 `docker compose down -v` 禁止在 real-pre 执行

## 6. 防误覆盖原则

- 写文件前先读
- 写文件后必须 diff
- 关键文件覆写必须 backup

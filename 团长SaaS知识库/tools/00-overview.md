---
kb_id: tools/00-overview
title: 工具与命令总览
domain: tools
category: overview
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - package.json
  - backend/pom.xml
  - docs/10-部署运行总览.md
related_reports: []
forbidden_misread:
  - 命令是入口约定，禁止改写为"看起来更短"形式
  - 不得以 root / admin 权限运行 npm / mvn
---

# 工具与命令总览

## 1. 目的

登记本仓库所有常用命令、Maven / npm / PowerShell / Docker 入口。任何 Agent 不得使用未登记的副作用命令（如 `rm -rf`、`git reset --hard`）。

## 2. 命令分类

| 分类 | 入口 | 工具 |
| --- | --- | --- |
| 后端构建 | `cd backend` | Maven 3.9+ |
| 前端构建 | `cd frontend` | Node 20+, npm/pnpm |
| E2E | 仓库根 | Playwright |
| 容器 | 仓库根 | Docker Compose v2 |
| 验收 | `docs/验收/` | PowerShell + cURL |
| 知识库 | `D:\Docs\Books\...` | Markdown |

## 3. 必读入口命令

```bash
# 后端
cd backend && mvn test
cd backend && mvn spring-boot:run

# 前端
cd frontend && npm run build
cd frontend && npm run dev

# E2E
npm run e2e:v1-p0
npm run e2e:real-pre:p0:preflight
npm run e2e:real-pre:p0

# 容器
docker compose ps
docker compose logs -f <service>
```

## 4. 副作用命令禁忌

| 禁忌 | 原因 |
| --- | --- |
| `rm -rf` / `rd /s /q` | 不可逆；必须显式登记 |
| `git reset --hard` | 丢未提交 |
| `git push --force` to main | 覆盖上游 |
| `docker compose down -v` | 删 real-pre volume |
| `drop / truncate` | real-pre 禁区 |
| `git add .` / `git add -A` | 风险太大 |
| `npm run build -- --force` | 误伤依赖 |
| `mvn clean install -U` 频繁 | 缓存丢失 |

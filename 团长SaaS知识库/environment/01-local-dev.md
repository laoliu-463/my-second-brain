---
kb_id: environment/01-local-dev
title: 本地开发环境
domain: environment
category: env-local
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - backend/src/main/resources/application.yml
  - frontend/vite.config.ts
related_reports: []
forbidden_misread:
  - 本地端口不得占用 8081/3001（real-pre 独占）
  - 不得把本地数据库指向 real-pre
---

# 本地开发环境

## 1. 适用场景

- Agent 调试
- 单测 / 集成测试
- 离线开发

## 2. 启动方式

```bash
# 后端
cd backend && mvn spring-boot:run

# 前端
cd frontend && npm run dev

# 或全栈容器（test/mock 形态）
docker compose up -d
```

## 3. 端口约定

| 端口 | 服务 |
| --- | --- |
| 8080 | 后端（local + test） |
| 3000 | 前端（local + test） |
| 5432 | PostgreSQL（test 容器） |
| 6379 | Redis（test 容器） |

## 4. 已知坑

- Windows 上 Maven 必须用 JDK 17
- Node 20 在 Vite 5 上需 `--openssl-legacy-provider`
- 本地启动若失败，先看 `git status` 是否干扰

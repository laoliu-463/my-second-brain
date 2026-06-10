---
kb_id: tools/04-docker-compose
title: Docker Compose 工具链
domain: tools
category: container
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docker-compose.yml
  - docker-compose.real-pre.yml
  - docs/10-部署运行总览.md
related_reports: []
forbidden_misread:
  - 禁止 `docker compose down -v`
  - 禁止对 real-pre 容器使用 mock 镜像
---

# Docker Compose 工具链

## 1. 主源

- `docker-compose.yml`（test/mock）
- `docker-compose.real-pre.yml`（real-pre）

## 2. 服务清单

| 服务 | 镜像 | 端口 (test) | 端口 (real-pre) |
| --- | --- | --- | --- |
| postgres | postgres:16 | 5432 | 5432 (内部) |
| redis | redis:7 | 6379 | 6379 (内部) |
| backend | 自构建 | 8080 | 8081 (127.0.0.1) |
| frontend | 自构建 | 3000 | 3001 (127.0.0.1) |
| nginx | nginx:1.25 | – | – |

## 3. 常用命令

```bash
# test/mock 启动
docker compose up -d

# real-pre 启动
docker compose -f docker-compose.real-pre.yml up -d

# 查看
docker compose ps

# 日志
docker compose logs -f backend

# 停止（不得 -v）
docker compose down
```

## 4. real-pre 边界

- 端口必须绑定 127.0.0.1
- 禁止 `down -v`
- 禁止删除 volume
- 禁止改 test/mock 配置

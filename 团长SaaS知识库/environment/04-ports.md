---
kb_id: environment/04-ports
title: 端口分配
domain: environment
category: env-port
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docker-compose.yml
  - docker-compose.real-pre.yml
  - nginx/nginx.conf
related_reports: []
forbidden_misread:
  - 8080/3000 = test+local；8081/3001 = real-pre 独占
  - 不得跨形态共享端口
---

# 端口分配

## 1. 端口总表

| 端口 | 服务 | 形态 | 绑定 |
| --- | --- | --- | --- |
| 5432 | PostgreSQL | test 容器 | 内部 |
| 6379 | Redis | test 容器 | 内部 |
| 8080 | Backend (Spring Boot) | test / local | 0.0.0.0 |
| 3000 | Frontend (Vite / Nginx) | test / local | 0.0.0.0 |
| 8081 | Backend (Spring Boot) | real-pre | 127.0.0.1 |
| 3001 | Frontend (Nginx) | real-pre | 127.0.0.1 |

## 2. 端口冲突检测

```bash
# Windows
netstat -ano | findstr ":8081"
netstat -ano | findstr ":3001"

# Git Bash
lsof -i :8081
lsof -i :3001
```

## 3. 端口绑定修复

| 现象 | 修复 |
| --- | --- |
| real-pre 端口暴露给 0.0.0.0 | 必须改回 127.0.0.1 |
| 多形态同时启动 | 显式选择其一 |
| 端口被其他服务占用 | 杀进程 / 换端口（须授权） |

## 4. 端口变更原则

- 不得擅自改端口（须 ADR）
- 改端口必须同步 docker-compose / nginx / 文档 / 验收脚本
- 改端口必须更新 `harness/CURRENT_STATE.md`

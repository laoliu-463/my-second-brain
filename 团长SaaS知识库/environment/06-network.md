---
kb_id: environment/06-network
title: 网络与安全
domain: environment
category: env-network
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
related_reports:
  - harness/reports/SECURITY-INCIDENT-001-*.md
forbidden_misread:
  - 真实环境禁止绑定 0.0.0.0
  - 真实环境禁止对外暴露数据库 / Redis 端口
---

# 网络与安全

## 1. 容器网络

| 网络 | 形态 | 是否隔离 |
| --- | --- | --- |
| `default` | local | 否 |
| `saas_test` | test/mock | 半隔离 |
| `saas_real_pre` | real-pre | 完全隔离 |

## 2. 外部可达

| 入口 | local | test | real-pre |
| --- | --- | --- | --- |
| 后端 | localhost | localhost | 127.0.0.1 |
| 前端 | localhost | localhost | 127.0.0.1 |
| PostgreSQL | localhost | 容器内 | 容器内 |
| Redis | localhost | 容器内 | 容器内 |

## 3. Nginx 反代（real-pre）

- 仅前端到后端的 `/api` 路径
- 不暴露数据库 / Redis
- 不暴露后端容器名
- 强制 HTTPS（按需）

## 4. 安全事件参考

- 2026-06-07 SECURITY-INCIDENT-001：real-pre 端口曾绑定 0.0.0.0，已修复为 127.0.0.1
- 教训：部署前必须 `grep '0.0.0.0'` + preflight

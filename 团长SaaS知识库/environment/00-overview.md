---
kb_id: environment/00-overview
title: 环境总览
domain: environment
category: overview
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
  - 不得跨环境共享数据库 / Redis 实例
  - 不得在 real-pre 注入 mock 样本
---

# 环境总览

## 1. 三种形态

| 形态 | 用途 | 端口 (后端) | 端口 (前端) | 数据库 |
| --- | --- | --- | --- | --- |
| `local` | 单机开发 | 8080 | 3000 | 本地 PG/Redis |
| `test` (mock) | Mock 回归基线 | 8080 | 3000 | 容器内 mock |
| `real-pre` | 真实上游预生产 | 8081 (127.0.0.1) | 3001 (127.0.0.1) | 容器内真实 PG/Redis |

## 2. 关键边界

| 维度 | test/mock | real-pre |
| --- | --- | --- |
| 上游 | 假数据 | 真实抖音开放平台 |
| Token | 假 / mock | 真实应用 token |
| 端口绑定 | 0.0.0.0 允许 | 127.0.0.1 强制 |
| 部署 | 任意 | 预检通过 |
| 数据持久 | 不要求 | 必须 |
| 验收入口 | `npm run e2e:v1-p0` | `npm run e2e:real-pre:p0` |

## 3. 形态切换原则

- 任意时刻只能运行一种形态的 backend / frontend
- 容器重启必须先 down（不得 -v）
- real-pre 部署前必须 preflight

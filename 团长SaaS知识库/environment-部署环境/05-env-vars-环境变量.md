---
kb_id: environment/05-env-vars
title: 环境变量
domain: environment
category: env-env-vars
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - .env.example
  - backend/src/main/resources/application.yml
related_reports: []
forbidden_misread:
  - 禁止硬编码 token / password / cookie / private key
  - 禁止把 secret 写入 git 跟踪文件
  - 禁止把 .env 复制到 KB / 报告
---

# 环境变量

## 1. 主源

- `.env.example`（脱敏模板）
- `application.yml`（default）
- `application-{profile}.yml`（按形态）

## 2. 关键变量

| 变量 | 用途 | 形态 |
| --- | --- | --- |
| `DOUYIN_CLIENT_KEY` | 抖音开放平台 client_key | real-pre |
| `DOUYIN_CLIENT_SECRET` | 抖音开放平台 client_secret | real-pre |
| `DOUYIN_ACCESS_TOKEN` | 访问令牌 | real-pre |
| `DB_URL` | 数据库连接 | 全部 |
| `DB_USER` | 数据库用户 | 全部 |
| `DB_PASSWORD` | 数据库密码 | 全部 |
| `REDIS_URL` | Redis 连接 | 全部 |
| `APP_PORT` | 后端端口 | 全部 |
| `FRONTEND_PORT` | 前端端口 | 全部 |

## 3. 注入方式

```bash
# 临时（bash）
export DOUYIN_ACCESS_TOKEN=xxx

# 临时（PowerShell）
$env:DOUYIN_ACCESS_TOKEN = "xxx"

# 永久（仅本机，不入库）
# 写入 ~/.bashrc / $PROFILE
```

## 4. 验收脱敏

- 报告 / 知识库 / 证据中：必须 `***REDACTED***`
- 日志：禁打 `Authorization` 头
- 前端：禁把 secret 注入到 `VITE_` 公开变量

## 5. secret 旋转

| 触发 | 行动 |
| --- | --- |
| 误提交 | 立刻停机 + 旋转 + ADR |
| 误打印 | 立刻旋转 + 报告 |
| 误日志 | 修日志策略 + 旋转 |

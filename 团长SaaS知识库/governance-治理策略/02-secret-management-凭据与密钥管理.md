---
kb_id: governance/02-secret-management
title: 凭据与密钥管理
domain: governance
category: governance-secret
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - backend/src/main/resources/application.yml
  - frontend/.env.example
related_reports: []
forbidden_misread:
  - 凭据不得入仓
  - 凭据不得入日志
  - 凭据轮换必须有事件登记
---

# 凭据与密钥管理

## 1. 用途

约束 token / client_secret / password / cookie / private key 等敏感凭据的存储、使用、轮换。

## 2. 关键约束

| 类型 | 存储方式 |
| --- | --- |
| 数据库密码 | 环境变量 / secret manager |
| API token | env 注入，不入配置 |
| client_secret | env 注入，不入仓 |
| 私钥 / 证书 | secret manager / 文件系统 600 权限 |
| Cookie | 短期 / httpOnly / secure |

## 3. 凭据轮换

- 季度：检查凭据有效期
- 事件触发：暴露后立即轮换
- 轮换记录：写入 DEBT / 治理报告

## 4. 禁止

- 禁止硬编码到源码
- 禁止在日志中打印
- 禁止在截图 / 报告中明文
- 禁止使用 git diff 泄露（提交前自查）

---
kb_id: evidence/03-api
title: 关键 API 证据
domain: evidence
category: evidence-api
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/05-API契约总表.md
  - harness/scripts/api/*.sh
related_reports: []
forbidden_misread:
  - API 必须认证
  - 真实凭据不得明文保存
---

# 关键 API 证据

## 1. 用途

通过 curl / httpie / Playwright API 调用，对接口契约做证据化验证。

## 2. 必查 API

| 接口 | 用途 | 期望 |
| --- | --- | --- |
| GET /api/system/health | 健康检查 | 200 |
| POST /api/auth/login | 登录 | 200 + token |
| GET /api/users/me | 当前用户 | 用户信息 |
| GET /api/orders?period=... | 订单列表 | 按时间过滤 |
| GET /api/performance/summary | 业绩汇总 | 双轨金额 |
| GET /api/analysis/dashboard | 看板 | 数据范围生效 |

## 3. 证据记录

- 入口：harness/scripts/api/*.sh
- 凭据：使用环境变量注入，不入仓
- 响应：保存到 harness/reports/evidence-*.md

## 4. 治理

- 仅 admin / biz_leader 触发导出
- 角色校验失败：FAILED
- 缺 token：PENDING（不写 PASS）

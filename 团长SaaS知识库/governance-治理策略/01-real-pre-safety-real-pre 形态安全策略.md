---
kb_id: governance/01-real-pre-safety
title: real-pre 形态安全策略
domain: governance
category: governance-real-pre-safety
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/03-部署与安全.md
  - harness/reports/SECURITY-INCIDENT-001-20260607-115744.md
related_reports:
  - harness/reports/SECURITY-INCIDENT-001-20260607-115744.md
  - harness/reports/SECURITY-INCIDENT-001-FINAL-PAUSE-20260607-115800.md
  - harness/reports/SECURITY-INCIDENT-001-FORENSIC-20260607-132211.md
forbidden_misread:
  - real-pre 端口必须 127.0.0.1
  - 禁止公网访问 real-pre
---

# real-pre 形态安全策略

## 1. 用途

约束 real-pre 形态的部署、访问、凭据、对外暴露，避免发生 SECURITY-INCIDENT 类问题。

## 2. 关键约束

| 项 | 约束 |
| --- | --- |
| 端口绑定 | 127.0.0.1，禁止 0.0.0.0 |
| 容器健康 | 端口存活 + 健康检查均通过 |
| 凭据 | 不入仓 / 不入日志 / 仅 env 注入 |
| 远程访问 | 仅本地 / 跳板机 / 内网 |
| 数据写 | 禁止演示 / 测试向生产写 |

## 3. 已知事件

- 2026-06-07：real-pre 后端/前端曾绑定 0.0.0.0
- 修复：2fa05495 fix(deploy): bind backend/frontend ports to 127.0.0.1

## 4. 升级路径

- FAILED → RISK_ACCEPTED：需用户书面确认
- BLOCKED_BY_SAMPLE / BLOCKED_BY_EXTERNAL：保持
- PASS：必须真实订单 + 三环通过

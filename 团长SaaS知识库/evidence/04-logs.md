---
kb_id: evidence/04-logs
title: 部署与同步日志证据
domain: evidence
category: evidence-logs
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/logs/*.log
  - backend/logs/*.log
related_reports:
  - harness/reports/SECURITY-INCIDENT-001-20260607-115744.md
forbidden_misread:
  - 日志不得包含明文 secret
  - 容器 healthy ≠ 业务闭环
---

# 部署与同步日志证据

## 1. 用途

记录容器启动、订单同步、业绩计算等关键事件日志。

## 2. 关键日志

| 来源 | 路径 | 内容 |
| --- | --- | --- |
| 后端应用 | backend/logs/application.log | Spring Boot 启动 + 业务日志 |
| 容器编排 | harness/logs/docker-compose.log | 容器启停 / 健康检查 |
| 订单同步 | harness/logs/order-sync.log | T+1 同步执行情况 |
| 业绩计算 | harness/logs/performance.log | 双轨计算 / 冲正 |

## 3. 关键证据样例

```
Tomcat initialized with port 8080
Tomcat started on port 8080 with context path '/api'
/api/system/health status=200
```

## 4. 注意事项

- 日志中如有 token / cookie / 凭据必须脱敏
- 容器 healthy 仅说明端口存活，不等于业务闭环
- 真实闭环必须依赖真实订单 + 三环验证

## 5. 已知事件

- 2026-06-07 SECURITY-INCIDENT-001：real-pre 端口曾绑定 0.0.0.0，已修复为 127.0.0.1

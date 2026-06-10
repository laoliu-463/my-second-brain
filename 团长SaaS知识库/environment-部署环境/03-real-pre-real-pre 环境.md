---
kb_id: environment/03-real-pre
title: real-pre 环境
domain: environment
category: env-real-pre
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docker-compose.real-pre.yml
  - docs/10-部署运行总览.md
  - harness/CURRENT_STATE.md
related_reports:
  - harness/reports/SECURITY-INCIDENT-001-*.md
  - harness/reports/evidence-20260607-151000.md
forbidden_misread:
  - 容器 healthy ≠ 业务闭环 PASS
  - 缺真实订单 / 真实 pick_source → P0 仍 PENDING
  - 禁止 `docker compose -f docker-compose.real-pre.yml down -v`
---

# real-pre 环境

## 1. 适用场景

- 真实上游预生产验收
- 真实订单 / 真实达人流转
- 真实 pick_source 样本验证

## 2. 启动前必检

1. `git status` 干净
2. `npm run e2e:real-pre:p0:preflight` 通过
3. 真实环境变量已注入
4. 端口 8081/3001 未被占用
5. 备份策略已就绪
6. 上一部署结论已记录

## 3. 端口与绑定

- backend: 127.0.0.1:8081
- frontend: 127.0.0.1:3001
- PostgreSQL / Redis：容器内私有网络
- 外部：仅 nginx 反代（按需）

## 4. 部署后必检

| 维度 | 命令 |
| --- | --- |
| 容器 healthy | `docker compose -f docker-compose.real-pre.yml ps` |
| 后端 health | `curl http://127.0.0.1:8081/api/system/health` |
| 前端可访问 | `curl http://127.0.0.1:3001/` |
| 三环 | 渠道链 / 招商链 / 管理链 端到端 |
| 双轨 | 预估轨 / 结算轨 数据一致 |
| 证据 | `harness/reports/evidence-*.md` 完整 |

## 5. 验收结论口径

| 现象 | 结论 |
| --- | --- |
| 无失败 + 无真实订单 | P0 = PENDING |
| 无失败 + 有真实订单 + 三环通过 | P0 = PASS |
| 缺 pick_source 样本 | P0 = BLOCKED_BY_SAMPLE |
| 上游不可达 | P0 = BLOCKED_BY_EXTERNAL |
| 健康探针失败 | P0 = FAILED |
| 已知风险 + 用户接受 | P0 = RISK_ACCEPTED_BY_USER |

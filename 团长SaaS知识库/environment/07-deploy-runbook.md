---
kb_id: environment/07-deploy-runbook
title: 部署运行手册
domain: environment
category: env-deploy
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/10-部署运行总览.md
  - docker-compose.yml
  - docker-compose.real-pre.yml
related_reports: []
forbidden_misread:
  - 禁止远端部署
  - 禁止无 preflight 的 real-pre 部署
  - 禁止 `down -v`
---

# 部署运行手册

## 1. 部署前必做

1. 读 `harness/CURRENT_STATE.md` 看上一部署结论
2. 读 `harness/FORBIDDEN_SCOPE.md` 确认本任务无禁做项
3. `git status --short` 干净或 REGISTERED_DIRTY
4. 真实环境变量已注入（不在 KB / 报告中泄露）
5. 端口 8081/3001 未被占用
6. 执行 `npm run e2e:real-pre:p0:preflight`
7. 备份：DB 快照 / volume 快照（按需）

## 2. 部署中禁止

- 不得 `docker compose down -v`
- 不得 `mvn clean install` 跳过测试
- 不得删除 volume
- 不得改 `application.yml` 测试配置
- 不得用 mock 镜像
- 不得绑定 0.0.0.0
- 不得重启不相关容器
- 不得用 root / admin 运行 npm / mvn
- 不得无 ADR 修改 migration
- 不得覆盖历史 V* SQL

## 3. 部署后必做

1. `docker compose -f docker-compose.real-pre.yml ps` 看 healthy
2. `curl http://127.0.0.1:8081/api/system/health` 200
3. `curl http://127.0.0.1:3001/` 200
4. 三环端到端（渠道 / 招商 / 管理）
5. 双轨金额对账（预估 vs 结算）
6. 写入 `harness/reports/evidence-*.md`
7. 写入 `harness/CURRENT_STATE.md` 新一节

## 4. 回退流程

| 现象 | 行动 |
| --- | --- |
| 容器起不来 | `docker compose logs` 找根因，**不** `down -v` |
| 后端 5xx | 看 `/api/system/health` + 日志 |
| 前端 404 | 检查 nginx 路由 + Vite dist |
| 数据异常 | 不可回退；新增修复 ADR |
| secret 泄露 | 立刻停 + 旋转 + 报告 |

## 5. 部署结论登记

```markdown
## YYYY-MM-DD HH:MM <task-id>
- 形态: real-pre
- 部署版本: <commit>
- preflight: PASS
- 容器 healthy: ✅
- 三环: PASS / PENDING / BLOCKED_*
- 双轨: PASS / PENDING
- 证据: harness/reports/evidence-YYYYMMDD-HHMM.md
- 结论: PASS / PENDING / BLOCKED_* / FAILED / RISK_ACCEPTED
```

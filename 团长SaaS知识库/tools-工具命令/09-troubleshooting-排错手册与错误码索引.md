---
kb_id: tools/09-troubleshooting
title: 排错手册与错误码索引
domain: tools
category: troubleshooting
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/FORBIDDEN_SCOPE.md
  - harness/CURRENT_STATE.md
  - harness/state/DOMAIN_STATUS.md
related_reports:
  - harness/reports/SECURITY-INCIDENT-001-*.md
  - harness/reports/evidence-20260607-151000.md
forbidden_misread:
  - 排错是"定位根因"，不得用"看似修复"绕过问题
  - 不得在排错时启动任何禁忌命令
---

# 排错手册与错误码索引

## 1. 目的

登记常见错误码、报错现象、根因定位路径、修复方向。不得直接"绕开"，必须落到根因。

## 2. 后端启动类

| 现象 | 根因 | 修复 |
| --- | --- | --- |
| `Port 8080 already in use` | 上一进程未退出 | 任务管理器 / `taskkill /PID /F`（须授权） |
| `Tomcat started on port 8080` 但 `/api/system/health` 500 | 数据库 / Redis 不可达 | 检查 `application.yml` + `docker compose ps` |
| `Bean creation failed` | 循环依赖 / 缺类 | 看 `mvn -DskipTests=false` 完整栈 |
| `Flyway migration failed` | SQL 冲突 | 不得修历史 V* 脚本；新增 V(N+1) |

## 3. 前端构建类

| 现象 | 根因 | 修复 |
| --- | --- | --- |
| `Module not found` | alias 错 / 缺依赖 | 检查 `vite.config.ts` + `tsconfig.json` |
| `Vite 5 + Node 18` 报错 | 缺 legacy provider | `NODE_OPTIONS=--openssl-legacy-provider` |
| `Naive UI` 全局未生效 | 未在 `App.vue` 包裹 `n-config-provider` | 检查入口 |

## 4. E2E / Playwright

| 现象 | 根因 | 修复 |
| --- | --- | --- |
| `real-pre` 测试在 mock 端口 | 配置错位 | 严格 `127.0.0.1:8081` / `127.0.0.1:3001` |
| `pick_source` 样本缺失 | 真实上游未授权 | 标记 `BLOCKED_BY_SAMPLE` |
| Trace 显示 `404` | 前端路由 vs 后端 API 错位 | 看 Network |

## 5. 容器类

| 现象 | 根因 | 修复 |
| --- | --- | --- |
| `healthy` 但业务不通 | health check 仅探进程存活 | 业务闭环测试 |
| `real-pre` 容器重启 | OOM / 配置漂移 | 看 `docker inspect` + 日志 |
| `port already allocated` | 宿主机端口占用 | 换端口 / 修 binding |

## 6. Git 类

| 现象 | 根因 | 修复 |
| --- | --- | --- |
| `fatal: refusing to merge unrelated histories` | 远程历史漂移 | 显式 `--allow-unrelated-histories`（须授权） |
| `unknown dirty` | 工作区有未登记改动 | REGISTERED_DIRTY 登记 / 决定丢弃 |
| `pre-commit hook failed` | 质量门禁 | 修复后再 commit；禁止 `--no-verify` |

## 7. 验收口径

- 排错结果必须落到根因，不得写"修好了"
- 修复必须经过 ADR 决策（若是受保护文件）
- 修复后必须更新 `harness/CURRENT_STATE.md`
- 严重事件必须落 `harness/reports/INCIDENT-*.md`

## 8. 紧急回退

| 触发 | 行动 |
| --- | --- |
| real-pre 业务中断 | `docker compose -f docker-compose.real-pre.yml down`（不 -v） |
| 关键迁移失败 | 不可回退；需新增 V(N+1) 修复 |
| secret 泄露 | 立刻停机 + 报告 + 旋转 |

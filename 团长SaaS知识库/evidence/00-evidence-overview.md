---
kb_id: evidence/00-evidence-overview
title: 证据体系总览
domain: evidence
category: evidence-overview
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/reports/evidence-*.md
  - docs/09-测试验收总览.md
related_reports: []
forbidden_misread:
  - 没有证据不得写 PASS
  - mock 证据不得用于 real-pre
---

# 证据体系总览

## 1. 用途

所有验收必须有"证据"——可核验的脚本、SQL/API、文件路径。

## 2. 三类证据

| 类型 | 用途 | 示例 |
| --- | --- | --- |
| 脚本 | 可重复执行 | PowerShell / Bash 验收脚本 |
| SQL/API | 数据库 / 接口查询 | psql / curl 输出 |
| 证据路径 | 文件 / 日志 / 截图 | harness/reports/evidence-*.md |

## 3. 6 类证据文件

| 文件 | 用途 |
| --- | --- |
| evidence/00-overview | 证据体系总览（本文件） |
| evidence/01-scripts | 验收脚本库 |
| evidence/02-sql | 关键 SQL 查询 |
| evidence/03-api | 关键 API 调用 |
| evidence/04-logs | 部署 / 同步日志 |
| evidence/05-screenshots | 截图与可视化证据 |

## 4. 证据状态

每条证据独立维护：
- 存在性：脚本/SQL/API/路径存在
- 可重现：按记录步骤可复现
- 时效：last_verified_at 在 V1 窗口内
- 归属：关联到具体域 / 流程

## 5. 证据与禁做

- mock 证据用于 test 形态；real-pre 必须有真实证据
- 缺真实订单时，real-pre P0 仍 PENDING，证据状态也是 PENDING
- BLOCKED_BY_* 必须有阻塞详情

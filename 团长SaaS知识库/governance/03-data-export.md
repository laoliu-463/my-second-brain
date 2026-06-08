---
kb_id: governance/03-data-export
title: 数据导出治理
domain: governance
category: governance-data-export
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - workflows/08-data-export.md
  - backend/src/main/java/com/colonel/saas/controller/AnalysisController.java
related_reports: []
forbidden_misread:
  - 仅 admin / biz_leader 可导出
  - 敏感字段必须脱敏
---

# 数据导出治理

## 1. 用途

约束 V1 数据导出的角色、字段、频次、审计与脱敏。

## 2. 关键约束

| 维度 | 约束 |
| --- | --- |
| 角色 | 仅 `admin` / `biz_leader` 可导出 |
| 行数 | 单次 ≤ 100,000 |
| 字段 | 手机号 / 身份证 / 邮箱脱敏 |
| 审计 | 每次导出写入审计日志 |
| 时效 | 异步任务 / 24h 过期 |

## 3. 审计日志

- 字段：operator, dim, period, rows, file_hash, ts
- 留存：≥ 180 天
- 位置：harness/audit/data-export.log

## 4. 异常处理

- 角色越权：FAILED（403）
- 超行数：FAILED
- 敏感字段未脱敏：FAILED

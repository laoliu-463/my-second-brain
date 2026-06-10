---
kb_id: workflows/08-data-export
title: 数据导出流程
domain: workflows
category: workflow-data-export
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/流程/数据导出.md
  - governance/02-data-export-policy.md
related_reports: []
forbidden_misread:
  - 数据导出受治理约束
  - V1 仅 admin / biz_leader 可导出
---

# 数据导出流程

## 1. 用途

将汇总数据导出为 CSV / Excel，供外部审计或财务对账使用。

## 2. 流程节点

```
[用户请求] → 角色校验（admin / biz_leader）→ 数据范围 → 汇总查询 → 导出
```

## 3. 治理约束

- 仅 `admin` / `biz_leader` 可导出
- 必须包含导出审计日志
- 敏感字段（手机号 / 身份证）需脱敏
- 单次导出行数 ≤ 100,000

## 4. 关键 API

- `POST /api/analysis/export?dim=...&period=...`
- `GET /api/analysis/export/{task_id}` （异步下载）

## 5. 验收口径

- 角色校验生效
- 导出审计日志完整
- 敏感字段脱敏
- 行数限制生效

## 6. 阻塞条件

- 角色越权 → FAILED（403）
- 敏感字段未脱敏 → FAILED
- 单次超行数 → FAILED

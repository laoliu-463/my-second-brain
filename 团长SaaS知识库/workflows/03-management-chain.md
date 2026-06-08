---
kb_id: workflows/03-management-chain
title: 管理链流程
domain: workflows
category: workflow-management
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/流程/管理链.md
related_reports: []
forbidden_misread:
  - 管理链 = 部门树回溯
  - 不重算业绩
---

# 管理链流程

## 1. 用途

按部门层级汇总业绩，供管理层查看。

## 2. 流程节点

```
[订单] → 业绩域归属（含 final_channel / final_recruiter）→ 部门树回溯 admin_dept_id
                                                          ↓
                                                管理链汇总（GMV / 服务费 / 毛利）
```

## 3. 部门树

- `department`（业务部门）
- `recruiter_group`（招商组）
- `channel_group`（渠道组）
- `ops_group`（运营组）

## 4. 关键 API

- `GET /api/performance/summary?dim=department&level={1,2,3}`
- `GET /api/performance/ranking?dim=department&period=month`

## 5. 验收口径

- 部门汇总与单订单业绩求和一致
- 数据范围 `all` 才看得到跨部门
- 三种 scope 行为正确

## 6. 阻塞条件

- 部门树缺失 → FAILED
- 跨部门汇总逻辑错误 → FAILED

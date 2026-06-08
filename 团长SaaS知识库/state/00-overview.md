---
kb_id: state/00-overview
title: 状态主源总览
domain: state
category: overview
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/CURRENT_STATE.md
  - harness/DOMAIN_STATUS.md
  - harness/DECISIONS.md
  - harness/HARNESS_DEBT.md
related_reports: []
forbidden_misread:
  - 状态主源是唯一可信的"当前事实"载体
  - 修改状态主源必须经 ADR
---

# 状态主源总览

## 1. 五大状态主源

| 主源 | 职责 | 写入条件 |
| --- | --- | --- |
| `harness/CURRENT_STATE.md` | 全项目当前事实 | 任务级更新 |
| `harness/DOMAIN_STATUS.md` | 8 域状态 | 域级更新 |
| `harness/DECISIONS.md` | 决策记录索引 | ADR 触发 |
| `harness/HARNESS_DEBT.md` | 25 项技术债 | 主动登记 |
| `harness/FORBIDDEN_SCOPE.md` | 禁做清单 | 仅初始化 |

## 2. 单一可信源原则

- 知识库中的"当前事实"必须引用状态主源
- 状态主源与代码冲突时，以**代码 + 实际部署**为准
- 状态主源与知识库冲突时，以**状态主源**为准

## 3. 状态更新触发

| 触发 | 主源 |
| --- | --- |
| 任务完成 | CURRENT_STATE |
| 域状态变化 | DOMAIN_STATUS |
| 决策变更 | DECISIONS |
| 新增技术债 | HARNESS_DEBT |
| 部署结论 | CURRENT_STATE + evidence |

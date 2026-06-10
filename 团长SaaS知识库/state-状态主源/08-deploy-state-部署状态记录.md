---
kb_id: state/08-deploy-state
title: 部署状态记录
domain: state
category: state-deploy
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/CURRENT_STATE.md
  - harness/reports/evidence-*.md
related_reports: []
forbidden_misread:
  - 不得将"容器 healthy"写成"业务闭环通过"
  - 缺真实订单 → 仍 PENDING
---

# 部署状态记录

## 1. 部署结论口径

| 现象 | 结论 |
| --- | --- |
| 无失败 + 无真实订单 | P0 = PENDING |
| 无失败 + 有真实订单 + 三环通过 | P0 = PASS |
| 缺 pick_source 样本 | P0 = BLOCKED_BY_SAMPLE |
| 上游不可达 | P0 = BLOCKED_BY_EXTERNAL |
| 健康探针失败 | P0 = FAILED |
| 已知风险 + 用户接受 | P0 = RISK_ACCEPTED_BY_USER |

## 2. 部署记录章节

- 部署时间
- 部署版本（commit）
- 形态（test / real-pre）
- preflight 结果
- 容器 healthy
- 三环
- 双轨
- 证据路径
- 结论

## 3. 关键观察

- 缺样本的具体来源
- 失败现象与初步定位
- 修复方案（如有）

## 4. 历史安全事件

- 2026-06-07 SECURITY-INCIDENT-001：real-pre 端口曾绑定 0.0.0.0
  - 修复：docker-compose.real-pre.yml 改 127.0.0.1
  - 教训：部署前 `grep '0.0.0.0'`

---
kb_id: domains/02-config-domain
title: 配置域
domain: domains
category: domain-config
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/领域/配置域.md
  - backend/src/main/java/com/colonel/saas/service/ConfigService.java
related_reports: []
forbidden_misread:
  - 配置域不执行具体业务规则
  - 公式由业绩域读取
---

# 配置域（config）

## 1. 用途

存储系统运行所需的所有可配置项，**不执行具体业务规则**——只提供值。

## 2. V1 必做

| 配置项 | 字段 | 默认值 |
| --- | --- | --- |
| 服务费率 | `service_fee_rate` | 0.10 |
| 招商提成率 | `recruiter_commission_rate` | 0.05 |
| 渠道提成率 | `channel_commission_rate` | 0.03 |
| 媒介提成率 | `media_commission_rate` | 0.02 |
| 技术服务费 | `tech_service_fee` | 500.00 |
| 数据保留天数 | `data_retention_days` | 365 |
| 同步窗口 | `sync_window_minutes` | 60 |

## 3. V1 不做

- 公式可视化编辑
- 多版本配置
- 审批流
- 灰度发布

## 4. 关键 API

| API | 用途 |
| --- | --- |
| `GET /api/configs` | 列出所有配置 |
| `PUT /api/configs/{key}` | 更新配置（需 admin） |
| `GET /api/configs/effective` | 当前生效配置（缓存） |

## 5. 关键实体

- `Config`：key, value, type, version, updated_at, updated_by
- `ConfigAudit`：key, old_value, new_value, operator, ts

## 6. 验收口径

- 修改服务费率后，业绩计算即时生效
- 配置变更记录可追溯
- 缓存命中（性能）

## 7. 不变量

> [V1 必做] 配置域负责配置，不执行具体业务规则。

业绩域**读取**配置计算金额；配置域不参与计算。

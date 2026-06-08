---
kb_id: state/02-domain-status
title: DOMAIN_STATUS 主源
domain: state
category: state-domain
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/DOMAIN_STATUS.md
  - docs/09-测试验收总览.md
related_reports: []
forbidden_misread:
  - 8 域状态必须真实反映"当前实现"
  - 不得写"已通过"当实际是 BLOCKED
---

# DOMAIN_STATUS 主源

## 1. 8 域状态

| 域 | 状态字段 | 含义 |
| --- | --- | --- |
| user | 用户域 | 角色 / 部门 / 数据范围 |
| config | 配置域 | 服务费率 / 提成公式 / 默认归属 |
| product | 商品域 | 转链 / pick_source |
| talent | 达人域 | 达人基础信息 |
| sample | 寄样域 | 寄样 / 收作业 |
| order | 订单域 | 订单事实（6468 / 2704） |
| performance | 业绩域 | 归属 / 提成 / 双轨 |
| analysis | 分析域 | 看板（只读汇总） |

## 2. 状态值

| 值 | 含义 |
| --- | --- |
| `PASS` | 验收通过 |
| `PENDING` | 未完成或待样本 |
| `BLOCKED_BY_SAMPLE` | 缺样本 |
| `BLOCKED_BY_EXTERNAL` | 上游不可达 |
| `FAILED` | 验收失败 |
| `RISK_ACCEPTED` | 已知风险已接受 |
| `NOT_STARTED` | 尚未启动 |

## 3. 域契约（不变量）

- 订单域只存事实，不算提成，不应用独家覆盖
- 业绩域负责最终归属、提成、冲正、双轨金额
- 配置域负责配置，不执行业务规则
- 分析模块只读汇总表，不重算业绩归属
- 用户域统一 self/group/all 数据范围
- 寄样域通过订单已同步事件判断交作业完成
- 商品域负责转链并落 `pick_source_mapping`

## 4. DDD 优化顺序

user → config → order → performance → analysis → product → talent → sample → outbox → frontend → E2E → GC

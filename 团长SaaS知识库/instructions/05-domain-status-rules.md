---
kb_id: instructions/05-domain-status-rules
title: DOMAIN_STATUS 与领域状态更新规则
domain: instructions
category: state-rules
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/state/DOMAIN_STATUS.md
  - harness/state/CURRENT_STATE.md
  - harness/FORBIDDEN_SCOPE.md
related_reports: []
forbidden_misread:
  - DOMAIN_STATUS 是按域登记，不是按任务登记
  - 任何域状态变更必须带 evidence 路径
  - 不得把 PENDING / BLOCKED 改成 PASS，缺证据时
---

# DOMAIN_STATUS 与领域状态更新规则

## 1. 目的

定义 `harness/state/DOMAIN_STATUS.md` 的最小更新规则、合法状态机与冲突仲裁流程。本文件不替代 `DOMAIN_STATUS.md` 本体，仅为操作规约。

## 2. 8 域状态字段

| 域 | 状态字段 | 含义 |
| --- | --- | --- |
| user | `users / roles / orgs / menus / data scope` | 用户域自治完成度 |
| config | `config / feature flags / env-bound` | 配置域自治完成度 |
| product | `pick_source_mapping / 转链 / 状态机` | 商品域自治完成度 |
| talent | `talent / 关系 / 归属` | 达人域自治完成度 |
| sample | `寄样 / 状态机 / 触发器` | 寄样域自治完成度 |
| order | `6468 同步 / 2704 结算 / 退货` | 订单域自治完成度 |
| performance | `归因 / 提成 / 冲正 / 双轨` | 业绩域自治完成度 |
| analysis | `汇总表 / 双轨口径 / 看板` | 分析域自治完成度 |

## 3. 合法状态机

| 状态 | 含义 | 转化条件 |
| --- | --- | --- |
| `UNTOUCHED` | 本任务不涉及 | 任何域都允许 |
| `PENDING` | 已识别但未开始 | 仅可由 `UNTOUCHED` 转化 |
| `IN_PROGRESS` | 进行中 | 必须有 owner + 起始日期 |
| `DONE` | 已完成 | 必须有 evidence |
| `BLOCKED_BY_SAMPLE` | 缺真实样本 | 缺 order / product / talent / pick_source 样本 |
| `BLOCKED_BY_EXTERNAL` | 外部阻塞 | 缺 token / 授权 / 上游 |
| `PARTIAL` | 部分完成 | 缺部分域联动 |
| `RISK_ACCEPTED` | 风险接受 | 必须有 Owner 拍板记录 |

## 4. 状态转移矩阵

| From \ To | PENDING | IN_PROGRESS | DONE | BLOCKED_* | PARTIAL | RISK_ACCEPTED |
| --- | --- | --- | --- | --- | --- | --- |
| UNTOUCHED | ✅ | – | – | – | – | – |
| PENDING | – | ✅ | – | ✅ | – | – |
| IN_PROGRESS | – | – | ✅ | ✅ | ✅ | ✅ |
| DONE | – | – | – | – | ✅ | ✅ |
| BLOCKED_* | – | ✅ | – | – | – | – |
| PARTIAL | – | ✅ | ✅ | – | – | – |
| RISK_ACCEPTED | – | ✅ | ✅ | – | – | – |

非法转移（如 PENDING → DONE）必须先回到 IN_PROGRESS。

## 5. 证据要求

| 状态 | 证据类型 |
| --- | --- |
| DONE | 至少 1 条：脚本输出 / API/SQL / 文件路径 |
| PARTIAL | 至少 1 条 + 缺口清单 |
| BLOCKED_BY_SAMPLE | 缺口样本清单（订单 / 商品 / 达人 / 转链） |
| BLOCKED_BY_EXTERNAL | 外部不可用清单（token / 授权 / 上游） |
| RISK_ACCEPTED | Owner 拍板记录（ADR-*.md 或 reports） |

## 6. 更新触发条件

- 任何代码、配置、文档修改 → 检查是否影响 8 域
- 任何状态机变化 → 必须先 ADR，再更新 DOMAIN_STATUS
- 任何跨域调用 → 必须登记到 `harness/state/CROSS_DOMAIN_FLOWS.md`

## 7. 与 CURRENT_STATE 的关系

- `CURRENT_STATE.md` 是全局快照
- `DOMAIN_STATUS.md` 是按域细分
- 两者必须保持一致；冲突以 DOMAIN_STATUS 为准

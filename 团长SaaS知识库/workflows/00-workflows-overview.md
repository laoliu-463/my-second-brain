---
kb_id: workflows/00-workflows-overview
title: 流程与剧本总览
domain: workflows
category: workflows-overview
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/流程/*.md
related_reports: []
forbidden_misread:
  - 流程是 V1 范围子集
  - 不覆盖 V2.2 旧流程
---

# 流程与剧本总览

## 1. 8 类流程

| 流程 | 用途 | 入口 |
| --- | --- | --- |
| 渠道链 | 渠道→招商→订单→业绩 | workflow/01-channel-chain |
| 招商链 | 商家→招商→订单→业绩 | workflow/02-recruiter-chain |
| 管理链 | 部门→业绩汇总 | workflow/03-management-chain |
| 订单同步 | 6468 + 2704 同步 | workflow/04-order-sync |
| 业绩冲正 | 退款 / 退单冲正 | workflow/05-reversal |
| 寄样交作业 | 订单已同步→寄样关闭 | workflow/06-sample-close |
| 看板只读 | 汇总表查询 | workflow/07-dashboard-readonly |
| 数据导出 | 治理过的导出 | workflow/08-data-export |

## 2. 流程依赖

```
渠道链 ─┐
招商链 ─┼─→ 订单同步 ─→ 业绩计算 ─→ 业绩冲正
管理链 ─┘                       │
                                ↓
寄样交作业 ←── 订单已同步事件 ───┘
                                ↓
                              看板只读
```

## 3. 流程状态

每个流程独立维护状态（见 state/02-domain-status.md）：
NOT_STARTED / IN_PROGRESS / PASS / PENDING / BLOCKED_BY_SAMPLE / BLOCKED_BY_EXTERNAL / FAILED / RISK_ACCEPTED

## 4. 流程验收

每个流程必须有：
- 入口文档
- 关键节点 SQL/API 证据
- 失败重试 / 状态回滚

## 5. 流程与禁做

- 流程中**不得**做 V1 范围外的事
- 流程中**不得**改业务代码（V1 禁做）
- 流程中**不得**绕过数据范围（self/group/all）

---
kb_id: state/05-forbidden-scope
title: FORBIDDEN_SCOPE 主源
domain: state
category: state-forbidden
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/FORBIDDEN_SCOPE.md
related_reports: []
forbidden_misread:
  - 禁做清单是 V1 红线
  - 不得以"方便"为由改动
---

# FORBIDDEN_SCOPE 主源

## 1. 用途

明确"绝不能做"的清单——按用户授权维度上锁。

## 2. 16 类禁做

| 类别 | 禁做 |
| --- | --- |
| 业务代码 | 改 Java / Vue / SQL migration / Docker / env / Nginx / 部署脚本 |
| 数据库 | 写库操作 |
| 容器 | 重启 / 重建 |
| 部署 | 远端部署 |
| Git | commit / push（未授权） |
| Git | `git add .` / `git add -A` |
| Git | 混批提交 |
| 安全 | 泄露 token / client_secret / password / cookie / private key |
| 验收 | mock 数据冒充 real-pre 真实闭环 |
| 验收 | BLOCKED_BY_SAMPLE → PASS |
| 验收 | BLOCKED_BY_EXTERNAL → PASS |
| 验收 | 容器 healthy → 业务闭环 PASS |
| 验收 | 订单表与业绩表 anti-join=0 → 结算轨验证完成 |
| 验收 | 订单同步成功 → 渠道归因闭环成功（无 pick_source 样本） |
| 范围 | 旧 V2.2 独家达人 / 独家商家 / 高级看板 / 差异化提成 → V1 必做 |
| KB | 知识库生成到项目仓库内 |

## 3. 禁做来源

- 用户授权对话
- 16 条原则
- V1 范围
- 历史安全事件

## 4. 禁做违反的处置

1. 立刻停止当前操作
2. 报告"误操作"细节
3. 评估影响（数据 / 安全 / 范围）
4. 旋转（如泄露 secret）
5. 写 ADR / DECISIONS

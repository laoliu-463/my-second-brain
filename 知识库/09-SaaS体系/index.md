---
title: "09-SaaS体系"
type: index
status: active
created_at: 2026-06-27
updated_at: 2026-06-27
source_level: none
sources: []
raw_evidence: []
related: []
tags: []
maintainers:
  - codex
confidence: 0.5
---
# 09-SaaS体系

> 抖店 SaaS 项目相关知识库入口

## 知识库管理

| 子目录 | 内容 |
|---|---|
| [[知识库Harness/]] | 知识库自身运维 Harness（入口、Audit、GC、Task Matrix） |
| [[知识库Harness/index]] | 知识库Harness 索引（核心文件、Skills、State） | 2026-06-04 |

---

## 项目 Harness

| 子目录 | 内容 |
|---|---|
| [[知识库/02-后端知识体系/SAAS-Harness规范/index|Harness/]] | AI Agent 工程执行系统（核心入口、Gate、State、DDD） |
| [[Harness-Domains/]] | 8 个领域执行规范（用户/配置/订单/业绩/商品/达人/寄样/分析） |
| [[Harness-Skills/]] | 15 个 AI Agent 可执行技能规范 |
| [[Harness-Runbooks/]] | 13 个执行手册（后端/前端/DB/Docker/部署/回滚等） |
| [[Harness-Evals/]] | 6 个验收规范（订单归因/P0回归/商品库/RBAC等） |
| [[Harness-Environment/]] | 5 个环境说明（test/real-pre/remote/local） |
| [[Harness-State/]] | 9 个状态文件（决策/部署/风险/P0-P1等） |
| [[Harness-Feedback/]] | 4 个反馈模板（证据报告/GC/复盘等） |
| [[Harness-Prompts/]] | 5 个可复用提示词 |

## 综合页

| 页面 | 内容 |
|---|---|
| [[知识库/syntheses/SAAS DDD渐进式重构任务链]] | DDD 提示词包沉淀出的渐进式重构任务结构 |
| [[知识库/syntheses/SAAS代码图谱业务流程图]] | code-review-graph 生成图谱的可维护综合入口 |

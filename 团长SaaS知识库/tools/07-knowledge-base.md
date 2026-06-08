---
kb_id: tools/07-knowledge-base
title: 知识库工具
domain: tools
category: kb
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - 00-index.md
  - instructions/00-agent-contract.md
related_reports:
  - harness/reports/harness-kb-001-*.md
forbidden_misread:
  - 不得把知识库生成到项目仓库内
  - 知识库是只读治理；不得在 KB 中写业务代码
---

# 知识库工具

## 1. 主源

- `D:\Docs\Books\my second brain\团长SaaS知识库\`（外置）

## 2. 目录结构

| 目录 | 文件数 | 用途 |
| --- | --- | --- |
| 根 | 2 | 入口与项目概览 |
| instructions/ | 8 | Instructions 子系统 |
| tools/ | 9 | Tools 子系统 |
| environment/ | 7 | Environment 子系统 |
| state/ | 8 | State 子系统 |
| domains/ | 9 | Domains 子系统 |
| workflows/ | 8 | Workflows 子系统 |
| evidence/ | 6 | Evidence 子系统 |
| governance/ | 6 | Governance 子系统 |

## 3. 知识条目分类

| 类型 | 含义 |
| --- | --- |
| contract | 工作合同 |
| gates | 门禁 |
| forbidden | 禁做 |
| quality | 质量台账 |
| state-rules | 状态规则 |
| routing | 任务路由 |
| safety | 安全清单 |
| overview | 总览 |
| backend | 后端 |
| frontend | 前端 |
| e2e | E2E |
| container | 容器 |
| qa | 验收 |
| git | Git |
| kb | 知识库 |
| env-overview | 环境总览 |
| env-local | 本地 |
| env-test | test/mock |
| env-real-pre | real-pre |
| env-port | 端口 |
| env-env-vars | 环境变量 |
| env-network | 网络 |
| env-deploy | 部署 |
| state-overview | 状态总览 |
| state-decisions | 决策 |
| state-current | 当前事实 |
| state-domain | 域状态 |
| state-debt | 债务 |
| state-changelog | 变更日志 |
| state-cross-domain | 跨域流 |
| state-failure | 失败模式 |
| state-restoration | 恢复策略 |
| domain-user | 用户域 |
| domain-config | 配置域 |
| domain-product | 商品域 |
| domain-talent | 达人域 |
| domain-sample | 寄样域 |
| domain-order | 订单域 |
| domain-performance | 业绩域 |
| domain-analysis | 分析域 |
| domain-integration | 集成域 |
| workflow-overview | 流程总览 |
| workflow-channel | 渠道链 |
| workflow-recruiter | 招商链 |
| workflow-management | 管理链 |
| workflow-order-sync | 订单同步 |
| workflow-attribution | 归因 |
| workflow-sample-flow | 寄样流 |
| workflow-perf-calc | 业绩计算 |
| workflow-settlement | 结算 |
| evidence-overview | 证据总览 |
| evidence-p0 | P0 证据 |
| evidence-real-pre | real-pre 证据 |
| evidence-domain | 域证据 |
| evidence-incident | 事件证据 |
| evidence-api | API 证据 |
| evidence-sql | SQL 证据 |
| gov-overview | 治理总览 |
| gov-changelog | 变更日志规则 |
| gov-adr | ADR 规范 |
| gov-debt | 债务治理 |
| gov-review | 复盘规范 |
| gov-incident | 事件响应 |

## 4. frontmatter 必填字段

| 字段 | 必填 |
| --- | --- |
| `kb_id` | ✅ |
| `title` | ✅ |
| `domain` | ✅ |
| `category` | ✅ |
| `last_verified_at` | ✅ |
| `freshness` | ✅ |
| `owner` | ✅ |
| `related_files` | ✅ |
| `forbidden_misread` | ✅ |
| `project_root` | ✅ |
| `kb_root` | ✅ |
| `source_type` | ✅ |
| `related_reports` | ⚠ 推荐 |

## 5. 知识库与项目仓库的边界

| 维度 | 项目仓库 | 知识库 |
| --- | --- | --- |
| 路径 | `D:\Projects\SAAS\` | `D:\Docs\Books\...` |
| 性质 | 业务代码 + 文档 | 只读治理 |
| 更新 | 开发驱动 | 阶段快照 |
| 提交 | git 跟踪 | 手动同步 |

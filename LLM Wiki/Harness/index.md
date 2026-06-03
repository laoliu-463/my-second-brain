# Harness Engineering 知识索引

> [!info]
> 上次对齐审计：[[知识库对齐报告-20260603]]

## 核心入口（Harness 总览）

- [[00-Harness-Engineering]] - 总览
- [[AGENT_CONTRACT-执行合同]] - Agent 执行合同和 DoD
- [[TASK_ROUTING-任务路由]] - 任务类型到领域、skill、验证的分流
- [[FORBIDDEN_SCOPE-禁止范围]] - V1、real-pre、Git、密钥和模块边界禁止项
- [[DOMAIN_MAP-领域地图]] - 七域 + 分析模块职责地图

## Completion Gates

- [[COMPLETION_GATES-完成门禁]] - Gate 0-4 五个完成门禁定义

## Session Exit Gate

- [[SESSION_EXIT_GATE-会话退出门禁]] - 清洁状态五项硬门禁

## State 状态

- [[CURRENT_STATE-当前状态]] - 当前状态、V1 闭环、旧文档冲突
- [[DOMAIN_STATUS-领域状态]] - 各领域 DDD 优化状态跟踪
- [[QUALITY_LEDGER-质量账本]] - 9 个模块质量评分
- [[HARNESS_CHANGELOG]] - Harness 版本变更记录

## DDD 优化

- [[DDD优化路线]] - DDD 优化总路线、阶段目标、验收标准
- [[DDD领域任务矩阵]] - 各领域任务卡索引（U-1 到 G-8）

## Doc 聚合文档（Harness 五子系统索引）

### 01-Instructions

- [[doc/01-instructions/01-项目执行协议]] - 项目执行协议
- [[doc/01-instructions/02-V1交付合同]] - V1 交付合同
- [[doc/01-instructions/03-禁止范围与安全边界]] - 禁止范围与安全边界
- [[doc/01-instructions/04-文档优先级与冲突处理]] - 文档优先级与冲突处理
- [[doc/01-instructions/05-领域边界总表]] - 领域边界总表

### 02-Tools

- [[doc/02-tools/01-现有脚本与命令索引]] - 现有脚本与命令索引
- [[doc/02-tools/02-后续Agent默认执行流程]] - Agent 默认执行流程
- [[doc/02-tools/03-构建重启部署命令规划]] - 构建重启部署命令规划

### 03-Environment

- [[doc/03-environment/01-test环境说明]] - test 环境说明
- [[doc/03-environment/02-real-pre环境说明]] - real-pre 环境说明
- [[doc/03-environment/03-remote-real-pre部署说明]] - 远端部署说明
- [[doc/03-environment/04-Docker-Compose服务地图]] - 服务地图

### 04-State

- [[doc/04-state/01-当前项目状态]] - 当前项目状态
- [[doc/04-state/02-业务闭环状态]] - 业务闭环状态
- [[doc/04-state/03-P0-P1问题台账]] - P0/P1 问题台账
- [[doc/04-state/04-real-pre证据索引]] - real-pre 证据索引
- [[doc/04-state/05-文档债务与冲突台账]] - 文档债务与冲突台账

### 05-Feedback

- [[doc/05-feedback/01-上线验收清单]] - 上线验收清单
- [[doc/05-feedback/02-业务闭环验证清单]] - 业务闭环验证清单
- [[doc/05-feedback/03-任务完成证据报告模板]] - 证据报告模板
- [[doc/05-feedback/04-任务后复盘模板]] - 任务后复盘模板
- [[doc/05-feedback/05-Harness持续迭代规则]] - Harness 持续迭代规则
- [[doc/05-feedback/06-旧内容生命周期规则]] - 旧内容生命周期规则

---

## 按主题分类（知识库 09-SaaS体系）

详细内容已迁移至：`知识库/09-SaaS体系/`

### 09-SaaS体系/Harness-Domains（领域执行规范）

- 用户域 / 配置域 / 订单域 / 业绩域 / 分析模块 / 商品域 / 达人域 / 寄样域
- safety-rules / definition-of-done / document-priority / v1-business-contract

### 09-SaaS体系/Harness-Skills（技能规范）

- domain-alignment / ddd-domain-optimization / ddd-boundary-check / ddd-post-task-sync
- code-review / order-attribution / sample-lifecycle / product-library
- performance-dashboard / real-pre-debug / frontend-ux / evidence-report
- git-batch-submit / git-change-control / post-task-gc

### 09-SaaS体系/Harness-Runbooks（执行手册）

- backend-change / frontend-change / database-change / docker-compose-operations
- real-pre-change / remote-deploy / rollback
- order-attribution-check / product-library-backfill-check / sample-auto-complete-check
- test-validation / third-party-integration / closeout-and-gc

### 09-SaaS体系/Harness-Evals（验收规范）

- order-attribution / p0-regression / product-library / rbac-scope
- sample-auto-complete / v1-business-closure

### 09-SaaS体系/Harness-Environment（环境说明）

- docker-compose-map / real-pre-env / test-env / local-dev-env / remote-real-pre-env

### 09-SaaS体系/Harness-State（状态文件）

- DECISIONS / DEPLOYMENT_STATE / KNOWN_ISSUES / TASK_HISTORY / VALIDATION_STATE
- current-business-state / known-risks / p0-p1-register / real-pre-evidence-index

### 09-SaaS体系/Harness-Feedback（反馈模板）

- evidence-report-template / feedback-loop / garbage-collection-policy / retro-summary-template

### 09-SaaS体系/Harness-Prompts（提示词）

- domain-alignment / full-review / p0-fix / real-pre-debug / release-check

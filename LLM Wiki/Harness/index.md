# Harness Engineering 知识索引

> [!info]
> 上次对齐审计：[[知识库对齐报告-20260603]]

## 核心入口

- [[00-Harness-Engineering]] - 总览
- [[AGENT_CONTRACT-执行合同]] - Agent 执行合同和 DoD
- [[TASK_ROUTING-任务路由]] - 任务类型到领域、skill、验证的分流
- [[FORBIDDEN_SCOPE-禁止范围]] - V1、real-pre、Git、密钥和模块边界禁止项
- [[DOMAIN_MAP-领域地图]] - 七域 + 分析模块职责地图

## Completion Gates

- [[COMPLETION_GATES-完成门禁]] - Gate 0-4 五个完成门禁定义

## Session Exit Gate

- [[SESSION_EXIT_GATE-会话退出门禁]] - 清洁状态五项硬门禁

## State

- [[CURRENT_STATE-当前状态]] - 当前状态、V1 闭环、旧文档冲突
- [[DOMAIN_STATUS-领域状态]] - 各领域 DDD 优化状态跟踪
- [[QUALITY_LEDGER-质量账本]] - 9 个模块质量评分
- [[HARNESS_CHANGELOG]] - Harness 版本变更记录
- [[state/DECISIONS]] - 架构决策记录
- [[state/DEPLOYMENT_STATE]] - 部署状态
- [[state/KNOWN_ISSUES]] - 已知问题
- [[state/TASK_HISTORY]] - 任务历史
- [[state/VALIDATION_STATE]] - 验证状态
- [[state/current-business-state]] - 业务闭环状态
- [[state/known-risks]] - 已知风险
- [[state/p0-p1-register]] - P0/P1 注册表
- [[state/real-pre-evidence-index]] - real-pre 证据索引

## DDD 优化

- [[DDD优化路线]] - DDD 优化总路线、阶段目标、验收标准
- [[DDD领域任务矩阵]] - 各领域任务卡索引（U-1 到 G-8）

## Skills

- [[skills/domain-alignment]] - 领域对齐 skill
- [[skills/ddd-domain-optimization]] - DDD 领域优化 skill
- [[skills/ddd-boundary-check]] - DDD 边界检查 skill
- [[skills/ddd-post-task-sync]] - DDD 任务后同步 skill
- [[skills/code-review]] - 代码审查 skill
- [[skills/order-attribution]] - 订单归因 skill
- [[skills/sample-lifecycle]] - 寄样状态机 skill
- [[skills/product-library]] - 商品库 skill
- [[skills/performance-dashboard]] - 业绩/看板 skill
- [[skills/real-pre-debug]] - real-pre 排障 skill
- [[skills/frontend-ux]] - 前端 UX skill
- [[skills/evidence-report]] - 证据报告 skill

## Instructions（各领域执行规范）

- [[instructions/user-domain]] - 用户域执行规范
- [[instructions/config-domain]] - 配置域执行规范
- [[instructions/order-domain]] - 订单域执行规范
- [[instructions/performance-domain]] - 业绩域执行规范
- [[instructions/analytics-module]] - 分析模块执行规范
- [[instructions/product-domain]] - 商品域执行规范
- [[instructions/talent-domain]] - 达人域执行规范
- [[instructions/sample-domain]] - 寄样域执行规范
- [[instructions/safety-rules]] - 安全规则
- [[instructions/definition-of-done]] - Done 定义
- [[instructions/document-priority]] - 文档优先级
- [[instructions/v1-business-contract]] - V1 业务合同

## Evals（验收规范）

- [[evals/order-attribution]] - 订单归因验收
- [[evals/p0-regression]] - P0 回归验收
- [[evals/product-library]] - 商品库验收
- [[evals/rbac-scope]] - RBAC 权限范围验收
- [[evals/sample-auto-complete]] - 寄样自动完成验收
- [[evals/v1-business-closure]] - V1 业务闭环验收

## Runbooks（执行手册）

- [[runbooks/backend-change]] - 后端变更手册
- [[runbooks/frontend-change]] - 前端变更手册
- [[runbooks/database-change]] - 数据库变更手册
- [[runbooks/docker-compose-operations]] - Docker 操作手册
- [[runbooks/real-pre-change]] - real-pre 变更手册
- [[runbooks/remote-deploy]] - 远端部署手册
- [[runbooks/rollback]] - 回滚手册
- [[runbooks/order-attribution-check]] - 订单归因检查手册
- [[runbooks/product-library-backfill-check]] - 商品库 backfill 检查手册
- [[runbooks/sample-auto-complete-check]] - 寄样自动完成检查手册
- [[runbooks/test-validation]] - 测试验证手册
- [[runbooks/third-party-integration]] - 第三方联调手册
- [[runbooks/closeout-and-gc]] - 收尾与 GC 手册

## Environment（环境说明）

- [[environment/README]] - 环境入口
- [[environment/docker-compose-map]] - Docker Compose 容器地图
- [[environment/real-pre-env]] - real-pre 环境说明
- [[environment/test-env]] - test 环境说明
- [[environment/local-dev-env]] - 本地开发环境说明
- [[environment/remote-real-pre-env]] - 远端 real-pre 环境说明

## Feedback（反馈与模板）

- [[feedback/evidence-report-template]] - 证据报告模板
- [[feedback/feedback-loop]] - 反馈循环
- [[feedback/garbage-collection-policy]] - 垃圾回收策略
- [[feedback/retro-summary-template]] - 复盘总结模板

## Prompts（可复用提示词）

- [[prompts/domain-alignment]] - 领域对齐提示词
- [[prompts/full-review]] - 全面审查提示词
- [[prompts/p0-fix]] - P0 修复提示词
- [[prompts/real-pre-debug]] - real-pre 排障提示词
- [[prompts/release-check]] - 发布检查提示词

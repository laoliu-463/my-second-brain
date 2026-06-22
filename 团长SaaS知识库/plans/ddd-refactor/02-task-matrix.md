---
kb_id: "KB-PLAN-DDD-02-TASK-MATRIX"
title: "DDD 任务矩阵"
domain: "harness"
category: "task_matrix"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 13:59:08"
related_files:
  - "D:\\Projects\\SAAS\\harness\\plans\\DDD_DOMAIN_TASK_MATRIX.md"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# DDD 任务矩阵

本矩阵是后续 DDD 子任务索引，不代表任务已经完成。所有任务默认行为不变、接口不变、数据库不变；需要变更接口或数据库时必须另起专项任务。

## 任务类型

A 只读审查；B 防护测试；C 命名与边界整理；D 逻辑搬迁；E 事件与事务；F 数据模型。

## 全量任务清单

### DDD-AUDIT-CROSS-DOMAIN-001 - 跨域依赖与边界只读审查

任务 ID：DDD-AUDIT-CROSS-DOMAIN-001
任务名称：跨域依赖与边界只读审查
所属领域：cross
任务类型：A 只读审查
目标：识别 Mapper / Service / Controller 横穿、事件边界和 Facade 优先级。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：git diff --check；只读扫描报告。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：tasks/ddd-audit-cross-domain-001.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。
状态：**DONE_AUDIT** (于 2026-06-08 14:40:00 完成)
证据报告：[evidence-20260608-144000-ddd-audit-cross-domain-001.md](file:///d:/Projects/SAAS/harness/reports/evidence-20260608-144000-ddd-audit-cross-domain-001.md)


### DDD-AUDIT-USER-001 - 审查数据范围实现

任务 ID：DDD-AUDIT-USER-001
任务名称：审查数据范围实现
所属领域：user
任务类型：A 只读审查
目标：盘点 CurrentUser、Role、Dept、DataScope 调用点。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读 rg + 用户域审查报告。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/user-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-USER-MODEL-001 - 审查用户/角色/部门模型

任务 ID：DDD-AUDIT-USER-MODEL-001
任务名称：审查用户/角色/部门模型
所属领域：user
任务类型：A 只读审查
目标：核对 sys_user/sys_role/sys_dept 与实体、Mapper、测试。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读模型清单。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/user-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-TEST-USER-DATASCOPE-001 - 补数据范围测试

任务 ID：DDD-TEST-USER-DATASCOPE-001
任务名称：补数据范围测试
所属领域：user
任务类型：B 防护测试
目标：锁定 admin/group/self 差异。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：mvn -f backend/pom.xml -Dtest=CurrentUserControllerTest,UserMasterDataServiceTest test
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/user-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-FACADE-USER-001 - 新增 UserDomainFacade

任务 ID：DDD-FACADE-USER-001
任务名称：新增 UserDomainFacade
所属领域：user
任务类型：C 边界整理
目标：新增极薄用户域 Facade，先迁移 1-3 个查询点。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：用户域 targeted tests + git diff --check。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：tasks/ddd-facade-user-001.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-POLICY-USER-DATASCOPE-001 - 提取 DataScopePolicy

任务 ID：DDD-POLICY-USER-DATASCOPE-001
任务名称：提取 DataScopePolicy
所属领域：user
任务类型：D 逻辑搬迁
目标：在测试保护后收敛 dataScope 决策。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：权限 targeted tests + roles E2E。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/user-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-APP-USER-SCOPE-001 - 整理用户应用服务

任务 ID：DDD-APP-USER-SCOPE-001
任务名称：整理用户应用服务
所属领域：user
任务类型：C 边界整理
目标：CurrentUser / PermissionContext 编排下沉。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：用户域 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/user-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-PACKAGE-USER-001 - 用户域包结构迁移

任务 ID：DDD-PACKAGE-USER-001
任务名称：用户域包结构迁移
所属领域：user
任务类型：D 逻辑搬迁
目标：仅迁移一个已保护 use case。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：全量后端测试 + API smoke。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/user-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-CONFIG-001 - 审查配置读取路径

任务 ID：DDD-AUDIT-CONFIG-001
任务名称：审查配置读取路径
所属领域：config
任务类型：A 只读审查
目标：盘点配置 API、缓存、审计与消费方。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读配置审查报告。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/config-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-CONFIG-CACHE-001 - 审查缓存失效路径

任务 ID：DDD-AUDIT-CONFIG-CACHE-001
任务名称：审查缓存失效路径
所属领域：config
任务类型：A 只读审查
目标：确认 ConfigChangedEvent 与缓存边界。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读事件/缓存清单。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/config-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-TEST-CONFIG-CACHE-001 - 补配置缓存测试

任务 ID：DDD-TEST-CONFIG-CACHE-001
任务名称：补配置缓存测试
所属领域：config
任务类型：B 防护测试
目标：锁定配置读取、保存、缓存失效和审计。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：mvn -f backend/pom.xml -Dtest=SysConfigServiceTest,RuleCenterServiceTest test
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/config-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-FACADE-CONFIG-001 - 新增 ConfigDomainFacade

任务 ID：DDD-FACADE-CONFIG-001
任务名称：新增 ConfigDomainFacade
所属领域：config
任务类型：C 边界整理
目标：新增只读配置 Facade，收敛消费方读取。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：配置 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：tasks/ddd-facade-config-001.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-POLICY-CONFIG-VALIDATION-001 - 提取 ConfigValidationPolicy

任务 ID：DDD-POLICY-CONFIG-VALIDATION-001
任务名称：提取 ConfigValidationPolicy
所属领域：config
任务类型：D 逻辑搬迁
目标：提取配置校验，不执行业务规则。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：配置保存/异常分支测试。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/config-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-CONFIG-CONSUMER-CONVERGENCE-001 - 收敛各域配置读取

任务 ID：DDD-CONFIG-CONSUMER-CONVERGENCE-001
任务名称：收敛各域配置读取
所属领域：config
任务类型：C 边界整理
目标：让业务域通过配置 Facade / 查询接口读取参数。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：消费方 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/config-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-PRODUCT-001 - 审查商品同步与展示规则

任务 ID：DDD-AUDIT-PRODUCT-001
任务名称：审查商品同步与展示规则
所属领域：product
任务类型：A 只读审查
目标：盘点 ProductService、ProductDisplayRuleService、转链、映射。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读商品域报告。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：[domains/product-ddd-plan.md](file:///d:/Docs/Books/my second brain/团长SaaS知识库/plans/ddd-refactor/domains/product-ddd-plan.md)
相关 evidence：[ddd-audit-product-001-20260619-153000.md](file:///d:/Projects/SAAS/harness/reports/ddd-audit-product-001-20260619-153000.md)
状态：**DONE_AUDIT** (于 2026-06-19 15:30:00 完成)

### DDD-TEST-PRODUCT-DISPLAY-001 - 补商品展示规则测试

任务 ID：DDD-TEST-PRODUCT-DISPLAY-001
任务名称：补商品展示规则测试
所属领域：product
任务类型：B 防护测试
目标：锁定 DISPLAYING/HIDDEN/PENDING 去重和展示口径。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：mvn -f backend/pom.xml -Dtest=ProductDisplayRuleServiceTest test
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/product-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-POLICY-PRODUCT-DISPLAY-001 - 提取 ProductDisplayPolicy

任务 ID：DDD-POLICY-PRODUCT-DISPLAY-001
任务名称：提取 ProductDisplayPolicy
所属领域：product
任务类型：D 逻辑搬迁
目标：把展示判断从大 Service 分离。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：商品展示 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/product-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-FACADE-PRODUCT-001 - 新增 ProductDomainFacade

任务 ID：DDD-FACADE-PRODUCT-001
任务名称：新增 ProductDomainFacade
所属领域：product
任务类型：C 边界整理
目标：对外输出商品、映射、转链只读能力。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：商品 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/product-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-APP-PRODUCT-DISPLAY-001 - 整理 ProductSyncApplicationService

任务 ID：DDD-APP-PRODUCT-DISPLAY-001
任务名称：整理 ProductSyncApplicationService
所属领域：product
任务类型：C 边界整理
目标：商品同步编排与展示策略分离。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：商品同步测试。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/product-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-INFRA-PRODUCT-GATEWAY-001 - 隔离 DouyinProductGateway

任务 ID：DDD-INFRA-PRODUCT-GATEWAY-001
任务名称：隔离 DouyinProductGateway
所属领域：product
任务类型：C 边界整理
目标：将抖音商品接口适配放到 infrastructure。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：网关 contract tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/product-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-APP-PROMOTION-LINK-001 - 整理 PromotionLinkApplicationService

任务 ID：DDD-APP-PROMOTION-LINK-001
任务名称：整理 PromotionLinkApplicationService
所属领域：product
任务类型：C 边界整理
目标：转链编排与 pick_source_mapping 落库边界清晰。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：Promotion/PickSource targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/product-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-TALENT-001 - 审查达人认领、地址与标签

任务 ID：DDD-AUDIT-TALENT-001
任务名称：审查达人认领、地址与标签
所属领域：talent
任务类型：A 只读审查
目标：盘点达人资料、认领、保护期、地址、标签。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读达人域报告。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/talent-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-TEST-TALENT-CLAIM-001 - 补认领保护期测试

任务 ID：DDD-TEST-TALENT-CLAIM-001
任务名称：补认领保护期测试
所属领域：talent
任务类型：B 防护测试
目标：锁定认领和保护期行为。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：Talent targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/talent-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-FACADE-TALENT-001 - 新增 TalentDomainFacade

任务 ID：DDD-FACADE-TALENT-001
任务名称：新增 TalentDomainFacade
所属领域：talent
任务类型：C 边界整理
目标：对寄样/业绩输出达人事实。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：达人 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/talent-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-POLICY-TALENT-CLAIM-001 - 提取 TalentClaimPolicy

任务 ID：DDD-POLICY-TALENT-CLAIM-001
任务名称：提取 TalentClaimPolicy
所属领域：talent
任务类型：D 逻辑搬迁
目标：认领规则从查询/写服务分离。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：认领 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/talent-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-APP-TALENT-001 - 整理达人应用服务

任务 ID：DDD-APP-TALENT-001
任务名称：整理达人应用服务
所属领域：talent
任务类型：C 边界整理
目标：达人资料、标签、跟进编排明确。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：TalentService/TalentQueryService tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/talent-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-SAMPLE-001 - 审查寄样状态机

任务 ID：DDD-AUDIT-SAMPLE-001
任务名称：审查寄样状态机
所属领域：sample
任务类型：A 只读审查
目标：盘点申请、审核、发货、签收、待交作业、完成状态。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读寄样域报告。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：tasks/ddd-audit-sample-001.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。
状态：**DONE_AUDIT** (于 2026-06-08 15:15:00 完成)
证据报告：[ddd-audit-sample-001-20260608-151500.md](file:///D:/Projects/SAAS/harness/reports/ddd-audit-sample-001-20260608-151500.md)

### DDD-AUDIT-SAMPLE-SEVEN-DAYS-001 - 审查 7 天限制

任务 ID：DDD-AUDIT-SAMPLE-SEVEN-DAYS-001
任务名称：审查 7 天限制
所属领域：sample
任务类型：A 只读审查
目标：确认寄样限制规则来源与边界。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读规则清单。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/sample-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-SAMPLE-ORDER-COMPLETE-001 - 审查订单完成寄样逻辑

任务 ID：DDD-AUDIT-SAMPLE-ORDER-COMPLETE-001
任务名称：审查订单完成寄样逻辑
所属领域：sample
任务类型：A 只读审查
目标：检查订单事件消费、匹配条件和幂等。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读事件消费清单。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/sample-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-TEST-SAMPLE-LIFECYCLE-001 - 补寄样状态机测试

任务 ID：DDD-TEST-SAMPLE-LIFECYCLE-001
任务名称：补寄样状态机测试
所属领域：sample
任务类型：B 防护测试
目标：锁定寄样生命周期和非法流转。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：mvn -f backend/pom.xml -Dtest=SampleLifecycleServiceTest,SampleControllerTest test
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：tasks/ddd-test-sample-lifecycle-001.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-POLICY-SAMPLE-APPLY-001 - 提取 SampleApplyPolicy

任务 ID：DDD-POLICY-SAMPLE-APPLY-001
任务名称：提取 SampleApplyPolicy
所属领域：sample
任务类型：D 逻辑搬迁
目标：申请资格和限制规则从应用服务中分离。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：寄样申请 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/sample-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-POLICY-SAMPLE-COMPLETE-001 - 提取 SampleCompletionPolicy

任务 ID：DDD-POLICY-SAMPLE-COMPLETE-001
任务名称：提取 SampleCompletionPolicy
所属领域：sample
任务类型：D 逻辑搬迁
目标：订单事件完成条件独立可测。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：订单事件消费 tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/sample-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-FACADE-SAMPLE-001 - 新增 SampleDomainFacade

任务 ID：DDD-FACADE-SAMPLE-001
任务名称：新增 SampleDomainFacade
所属领域：sample
任务类型：C 边界整理
目标：对外提供寄样事实/状态只读能力。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：寄样 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/sample-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-APP-SAMPLE-LIFECYCLE-001 - 整理 SampleLifecycleApplicationService

任务 ID：DDD-APP-SAMPLE-LIFECYCLE-001
任务名称：整理 SampleLifecycleApplicationService
所属领域：sample
任务类型：C/D 逻辑搬迁
目标：一次只搬一个状态流转 use case。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：寄样生命周期 targeted tests + E2E。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/sample-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-ORDER-001 - 审查 6468/2704 同步入口

任务 ID：DDD-AUDIT-ORDER-001
任务名称：审查 6468/2704 同步入口
所属领域：order
任务类型：A 只读审查
目标：盘点订单同步、分页、水位、归因、afterCommit。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读订单域报告。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：tasks/ddd-audit-order-001.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-ORDER-CURSOR-001 - 审查 cursor 分页

任务 ID：DDD-AUDIT-ORDER-CURSOR-001
任务名称：审查 cursor 分页
所属领域：order
任务类型：A 只读审查
目标：确认 6468/2704 分页、水位和失败证据。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读同步清单。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/order-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-ORDER-HOT-RECENT-001 - 审查 hot recent

任务 ID：DDD-AUDIT-ORDER-HOT-RECENT-001
任务名称：审查 hot recent
所属领域：order
任务类型：A 只读审查
目标：检查 PAY_RECENT/INCREMENTAL 互不污染。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读日志/配置清单。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/order-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-ORDER-ATTRIBUTION-001 - 审查 default attribution

任务 ID：DDD-AUDIT-ORDER-ATTRIBUTION-001
任务名称：审查 default attribution
所属领域：order
任务类型：A 只读审查
目标：确认 pick_source、mapping、默认渠道/招商输入。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读归因输入清单。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/order-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-ORDER-AFTER-COMMIT-001 - 审查 afterCommit 事件

任务 ID：DDD-AUDIT-ORDER-AFTER-COMMIT-001
任务名称：审查 afterCommit 事件
所属领域：order
任务类型：A 只读审查
目标：检查订单事件发布时机、消费者和历史缺口。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读事件边界报告。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/order-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-TEST-ORDER-SYNC-001 - 补订单同步测试

任务 ID：DDD-TEST-ORDER-SYNC-001
任务名称：补订单同步测试
所属领域：order
任务类型：B 防护测试
目标：锁定双源同步、幂等、日志和错误分支。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：mvn -f backend/pom.xml -Dtest=OrderSyncServiceTest,OrderSyncPersistenceServiceTest test
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：tasks/ddd-test-order-sync-001.md
相关 evidence：[latest-evidence-20260619.md](file:///d:/Projects/SAAS/harness/reports/latest-evidence-20260619.md)
状态：**DONE_TEST** (于 2026-06-19 15:45:00 完成)

### DDD-TEST-ORDER-ATTRIBUTION-001 - 补归因测试

任务 ID：DDD-TEST-ORDER-ATTRIBUTION-001
任务名称：补归因测试
所属领域：order
任务类型：B 防护测试
目标：锁定 pick_source 映射和 default attribution。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：OrderAttribution targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/order-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-FACADE-ORDER-001 - 新增 OrderDomainFacade

任务 ID：DDD-FACADE-ORDER-001
任务名称：新增 OrderDomainFacade
所属领域：order
任务类型：C 边界整理
目标：对外输出订单事实和事件，不暴露同步细节。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：订单 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：tasks/ddd-facade-order-001.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-POLICY-ORDER-ATTRIBUTION-001 - 提取 OrderAttributionPolicy

任务 ID：DDD-POLICY-ORDER-ATTRIBUTION-001
任务名称：提取 OrderAttributionPolicy
所属领域：order
任务类型：D 逻辑搬迁
目标：将归因输入解析从同步编排中分离。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：归因 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/order-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-INFRA-ORDER-GATEWAY-001 - 隔离 DouyinOrderGateway

任务 ID：DDD-INFRA-ORDER-GATEWAY-001
任务名称：隔离 DouyinOrderGateway
所属领域：order
任务类型：C 边界整理
目标：将抖音订单 SDK/HTTP 适配隔离。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：网关 contract tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/order-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-APP-ORDER-SYNC-001 - 整理 OrderSyncApplicationService

任务 ID：DDD-APP-ORDER-SYNC-001
任务名称：整理 OrderSyncApplicationService
所属领域：order
任务类型：C/D 逻辑搬迁
目标：同步编排、持久化、事件发布边界分离。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：订单同步 targeted tests + preflight。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/order-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-PERFORMANCE-001 - 审查 PerformanceCalculationService

任务 ID：DDD-AUDIT-PERFORMANCE-001
任务名称：审查 PerformanceCalculationService
所属领域：performance
任务类型：A 只读审查
目标：盘点业绩计算、补算、公式、冲正和汇总。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读业绩域报告。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：tasks/ddd-audit-performance-001.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-PERFORMANCE-BACKFILL-001 - 审查补算服务

任务 ID：DDD-AUDIT-PERFORMANCE-BACKFILL-001
任务名称：审查补算服务
所属领域：performance
任务类型：A 只读审查
目标：确认历史缺口 backfill 和回滚边界。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读补算清单。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/performance-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-PERFORMANCE-FORMULA-001 - 审查公式口径

任务 ID：DDD-AUDIT-PERFORMANCE-FORMULA-001
任务名称：审查公式口径
所属领域：performance
任务类型：A 只读审查
目标：核对服务费收入/收益双轨公式。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读公式映射清单。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/performance-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-TEST-PERFORMANCE-CALC-001 - 补业绩计算测试

任务 ID：DDD-TEST-PERFORMANCE-CALC-001
任务名称：补业绩计算测试
所属领域：performance
任务类型：B 防护测试
目标：锁定最终归属、服务费收益、提成公式。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：mvn -f backend/pom.xml -Dtest=PerformanceCalculationServiceTest,ServiceFeeMoneyFormula8291Test test
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：tasks/ddd-test-performance-calc-001.md
相关 evidence：[latest-evidence-20260619.md](file:///d:/Projects/SAAS/harness/reports/latest-evidence-20260619.md)
状态：**DONE_TEST** (于 2026-06-19 17:10:00 完成)

### DDD-TEST-PERFORMANCE-REVERSAL-001 - 补退款冲正测试

任务 ID：DDD-TEST-PERFORMANCE-REVERSAL-001
任务名称：补退款冲正测试
所属领域：performance
任务类型：B 防护测试
目标：锁定退款事实消费和冲正汇总。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：Performance targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/performance-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-FACADE-PERFORMANCE-001 - 新增 PerformanceDomainFacade

任务 ID：DDD-FACADE-PERFORMANCE-001
任务名称：新增 PerformanceDomainFacade
所属领域：performance
任务类型：C 边界整理
目标：对分析模块提供业绩只读结果和汇总查询。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：业绩 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/performance-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-POLICY-PERFORMANCE-CALC-001 - 提取 PerformanceCalculationPolicy

任务 ID：DDD-POLICY-PERFORMANCE-CALC-001
任务名称：提取 PerformanceCalculationPolicy
所属领域：performance
任务类型：D 逻辑搬迁
目标：将公式和归属规则从大 Service 分离。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：业绩公式 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/performance-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-APP-PERFORMANCE-CALC-001 - 整理 PerformanceApplicationService

任务 ID：DDD-APP-PERFORMANCE-CALC-001
任务名称：整理 PerformanceApplicationService
所属领域：performance
任务类型：C/D 逻辑搬迁
目标：计算命令与查询/汇总分离。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：业绩 targeted tests + SQL 对账。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/performance-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-QUERY-PERFORMANCE-SUMMARY-001 - 整理 PerformanceSummaryQueryService

任务 ID：DDD-QUERY-PERFORMANCE-SUMMARY-001
任务名称：整理 PerformanceSummaryQueryService
所属领域：performance
任务类型：C 边界整理
目标：分析模块只通过只读查询消费。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：Dashboard/API SQL 对账。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/performance-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-ANALYSIS-001 - 审查 dashboard 查询路径

任务 ID：DDD-AUDIT-ANALYSIS-001
任务名称：审查 dashboard 查询路径
所属领域：analysis
任务类型：A 只读审查
目标：盘点 DashboardService、DataApplicationService、DataController。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读分析模块报告。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/analysis-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-ANALYSIS-SUMMARY-001 - 审查 summary API

任务 ID：DDD-AUDIT-ANALYSIS-SUMMARY-001
任务名称：审查 summary API
所属领域：analysis
任务类型：A 只读审查
目标：确认旧 summary 单轨风险和双轨需求。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读 API 清单。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/analysis-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-AUDIT-ANALYSIS-CACHE-001 - 审查 dashboard 缓存

任务 ID：DDD-AUDIT-ANALYSIS-CACHE-001
任务名称：审查 dashboard 缓存
所属领域：analysis
任务类型：A 只读审查
目标：检查 ShortTtlCache 和汇总缓存边界。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：只读缓存清单。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/analysis-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-TEST-DASHBOARD-RECON-001 - 补 dashboard 对账测试

任务 ID：DDD-TEST-DASHBOARD-RECON-001
任务名称：补 dashboard 对账测试
所属领域：analysis
任务类型：B 防护测试
目标：锁定 API/SQL 双轨指标一致。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：Dashboard targeted tests + SQL 只读对账。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/analysis-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-FACADE-ANALYSIS-001 - 新增 AnalysisDomainFacade

任务 ID：DDD-FACADE-ANALYSIS-001
任务名称：新增 AnalysisDomainFacade
所属领域：analysis
任务类型：C 边界整理
目标：对前端/BFF 输出只读指标查询。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：分析 targeted tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/analysis-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-APP-DASHBOARD-QUERY-001 - 整理 DashboardQueryService

任务 ID：DDD-APP-DASHBOARD-QUERY-001
任务名称：整理 DashboardQueryService
所属领域：analysis
任务类型：C 边界整理
目标：dashboard 查询和聚合读模型分离。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：DashboardService/DataApplicationService tests。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/analysis-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-ANALYSIS-READMODEL-001 - 分离聚合读模型

任务 ID：DDD-ANALYSIS-READMODEL-001
任务名称：分离聚合读模型
所属领域：analysis
任务类型：C/D 逻辑搬迁
目标：不重算归属，只读汇总。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：API/SQL 对账 + E2E。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/analysis-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

### DDD-OUTBOX-DESIGN-001 - Outbox 预备设计

任务 ID：DDD-OUTBOX-DESIGN-001
任务名称：Outbox 预备设计
所属领域：cross
任务类型：A 只读审查
目标：只输出事件一致性设计，不落地表或 MQ。
非目标：不改业务口径；不改接口契约；不改数据库结构；不混入 bug 修复。
允许修改范围：按任务类型限定；A 类只读；B 类只加/改测试；C/D/E/F 必须在独立任务中声明具体文件。
禁止修改范围：禁止跨多个领域；禁止 Java/Vue/SQL/Docker/env 混改；禁止全局 package migration；禁止 V2 能力混入 V1。
前置条件：读取 plans/ddd-refactor/00-index.md、对应领域计划和当前 task card；确认当前 Git dirty 来源。
验证命令：设计报告 + 禁止实现声明。
回滚方式：还原本任务允许修改文件；若是测试/代码任务按 Git 单文件回滚，不使用 git reset --hard。
完成判定：有 evidence；验证命令结果明确；对应 KB 任务页、领域页和 state 页已更新。
不能宣称完成的条件：缺测试、缺 evidence、缺样本、改了非目标范围、业务口径有争议但未进入 ADR。
相关知识库文件：domains/cross-domain-ddd-plan.md
相关 evidence：本任务启动后生成 harness/reports/evidence-*-<task-id>.md。

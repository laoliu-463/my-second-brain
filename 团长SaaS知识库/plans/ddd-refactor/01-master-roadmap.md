---
kb_id: "KB-PLAN-DDD-01-ROADMAP"
title: "DDD 重构总路线图"
domain: "harness"
category: "refactor_plan"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 13:59:08"
related_files:
  - "D:\\Projects\\SAAS\\harness\\plans\\DDD_OPTIMIZATION_ROADMAP.md"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# DDD 重构总路线图

## 1. 当前 DDD 重构目标

在不改变 V1 业务口径、接口契约和数据库结构的前提下，逐步把当前模块化单体中的跨域调用、大 Service、胖 Controller、Mapper 穿透和事件事务边界整理为可验证的 DDD 分层。

## 2. 为什么采用渐进式重构

当前项目已经具备真实业务链路和 real-pre 环境，订单、业绩、寄样、商品链路存在上游样本依赖。一次性重构会放大回归风险，尤其会影响 pick_source 归因、performance_records、寄样自动完成和 dashboard 双轨口径。

## 3. 为什么不能先做包结构大迁移

代码图谱和文件统计显示 ProductService、OrderSyncService、SampleApplicationService、DataApplicationService 等热点文件承担大量编排和规则。先迁包只会制造路径变化和 review 成本，不能证明行为不变。包结构迁移必须放在 Phase 7，并且一次只迁一个有测试保护的 use case。

## 4. 七个阶段

### Phase 0：只读审查

目标：不改代码，识别领域边界、跨域依赖、God Service、Mapper 穿透、Controller 胖逻辑、事务和事件风险、测试保护。
进入条件：当前代码与 KB 可读；完成 code-review-graph / rg 只读扫描。
退出条件：每个领域有审查任务卡和证据格式；未产生业务代码修改。
不能做：禁止移动包、禁止抽象空接口、禁止业务修复。
允许任务类型：A

### Phase 1：防护测试

目标：先锁定订单、业绩、寄样、商品、用户、配置、Dashboard 的现有行为。
进入条件：Phase 0 风险清单明确。
退出条件：关键 use case 有 targeted tests 或缺口登记。
不能做：禁止改生产逻辑、禁止顺手修 bug。
允许任务类型：B

### Phase 2：Facade 收敛

目标：新增极薄 Domain Facade，先收敛 1-3 个跨域读取点。
进入条件：对应测试已存在或补齐。
退出条件：旧调用可保留，新调用有 Facade 入口；接口契约不变。
不能做：禁止一次迁移整个 service 层。
允许任务类型：C

### Phase 3：Application Service 分层

目标：将 Controller 编排和外部 API 编排逐 use case 下沉到应用服务。
进入条件：Facade 或边界缺口已明确。
退出条件：一个 use case 的编排位置清晰，Controller 入参出参不变。
不能做：禁止同时改多个领域或前后端联动改契约。
允许任务类型：C/D

### Phase 4：Domain Policy 提取

目标：把稳定 if/else 业务规则提取为 Policy / Domain Service。
进入条件：测试覆盖规则分支。
退出条件：策略对象仅承载本域规则，行为一致。
不能做：禁止修改业务公式、状态机或权限规则。
允许任务类型：D

### Phase 5：Infrastructure Adapter 隔离

目标：将抖音 API、Redis 水位、Mapper 访问、外部网关隔离到 infrastructure/adapter。
进入条件：应用服务边界清晰。
退出条件：Port 与实现分离但行为、日志、配置不变。
不能做：禁止引入新外部框架或隐藏 SDK 错误。
允许任务类型：C/D

### Phase 6：事件与一致性治理

目标：按单个事件处理 afterCommit、幂等、失败补偿和证据。
进入条件：事件生产/消费审查完成。
退出条件：一个事件边界有幂等和失败证据。
不能做：禁止一次性上完整 Outbox 或 MQ。
允许任务类型：E

### Phase 7：包结构迁移

目标：在测试和边界收敛后逐领域迁移包结构。
进入条件：目标领域关键 use case 已有测试保护和 Facade/应用服务。
退出条件：一次只迁一个 use case，API/DB/前端不变。
不能做：禁止全局 package migration。
允许任务类型：C/D

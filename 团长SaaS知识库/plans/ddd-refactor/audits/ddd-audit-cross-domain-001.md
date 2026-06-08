---
kb_id: "KB-PLAN-DDD-AUDIT-CROSS-DOMAIN-001-REPORT"
title: "DDD 跨域依赖只读审查报告"
domain: "cross"
category: "audit_report"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 14:40:00"
related_files:
  - "D:\\Projects\\SAAS\\harness\\TASK_ROUTING.md"
  - "D:\\Docs\\Books\\my second brain\\团长SaaS知识库\\plans\\ddd-refactor\\tasks\\ddd-audit-cross-domain-001.md"
---

# DDD 跨域依赖只读审查报告 (DDD-AUDIT-CROSS-DOMAIN-001)

## 1. 领域划分分布情况
SaaS 项目采用扁平的后端包结构：所有类分别位于 `com.colonel.saas.controller`、`com.colonel.saas.service`、`com.colonel.saas.mapper`、`com.colonel.saas.entity` 中。
按照业务语义，代码实质上分散在以下 9 个逻辑领域：
1. **用户与权限域 (User)**: `SysUser`, `SysRole`, `SysDept`
2. **达人域 (Talent)**: `Talent`, `TalentClaim`, `ExclusiveTalent`
3. **商品域 (Product)**: `Product`, `ProductSnapshot`, `ProductDisplayRule`
4. **寄样域 (Sample)**: `SampleRequest`, `SampleLifecycle`
5. **订单域 (Order)**: `ColonelsettlementOrder`
6. **业绩域 (Performance)**: `PerformanceRecord`
7. **配置域 (Config)**: `BusinessRuleConfig`
8. **招商域 (Merchant)**: `ExclusiveMerchant`, `ColonelsettlementActivity`
9. **分析域 (Analysis)**: `Dashboard`, `DashboardPerformanceSummary`

## 2. 跨域调用图谱
由于缺乏物理包隔离，各领域逻辑处于网状调用关系中，最核心的耦合枢纽有：
- **达人域 (Talent)** -> **用户域 (User)** / **订单域 (Order)** / **寄样域 (Sample)**
- **寄样域 (Sample)** -> **商品域 (Product)** / **达人域 (Talent)** / **用户域 (User)**
- **数据应用服务 (DataApplicationService)** -> 跨越**订单**、**业绩**、**用户**、**达人**、**招商**等几乎所有领域。
- **业绩域 (Performance)** -> **订单域 (Order)**

## 3. 跨域 Mapper/Service 穿透清单
以下 Service 绕过领域边界，直接注入并操作了其他领域的 Mapper，构成了核心跨域依赖：
1. **TalentService**: 注入了 `ColonelsettlementOrderMapper` (Order), `SampleRequestMapper` (Sample), `SysUserMapper` (User)
2. **TalentQueryService**: 注入了 `SysUserMapper` (User), `SampleRequestMapper` (Sample)
3. **ProductService**: 注入了 `ColonelsettlementOrderMapper` (Order), `SysUserMapper` (User)
4. **SampleApplicationService**: 注入了 `ProductSnapshotMapper` (Product), `SysUserMapper` (User), `TalentMapper` (Talent), `TalentClaimMapper` (Talent)
5. **SampleFilterOptionsService**: 注入了 `ProductSnapshotMapper` (Product), `SysUserMapper` (User)
6. **OrderService**: 注入了 `ProductSnapshotMapper` (Product)
7. **OrderSyncPersistenceService**: 注入了 `SysUserMapper` (User)
8. **PerformanceQueryService**: 注入了 `ColonelsettlementOrderMapper` (Order)
9. **DataApplicationService**: 注入了 `ColonelsettlementOrderMapper` (Order), `PerformanceRecordMapper` (Performance), `SysUserMapper` (User), `ExclusiveTalentMapper` (Talent), `ExclusiveMerchantMapper` (Merchant), `ColonelsettlementActivityMapper` (Merchant)
10. **ProductQuickSampleService**: 注入了 `SampleRequestMapper` (Sample), `TalentMapper` (Talent), `TalentClaimMapper` (Talent)
11. **SampleLifecycleService**: 注入了 `TalentClaimMapper` (Talent)

## 4. 胖 Service (God Service) 排行榜及统计
以下为代码行数与文件大小排名前列的“上帝服务”：
1. **ProductService.java (246KB)**: 承载了商品基础信息、转链、讲解复制、佣金计算、达人结算等多项逻辑，亟需拆分。
2. **SampleApplicationService.java (191KB)**: 杂糅了寄样申请、审核、归因、状态更新、数据范围过滤等逻辑。
3. **DataApplicationService.java (110KB)**: 这是一个严重的架构误区——它虽然命名为 Service，但实际是一个 `@RestController` 并继承了 `BaseController`，直接注入了 6 个 Mapper 并大量使用 `JdbcTemplate` 执行裸 SQL 聚合。
4. **TalentService.java (71KB)**
5. **TalentQueryService.java (69KB)**

## 5. 胖 Controller (Controller fat logic) 盘点
有些 Controller 存在大量的编排和复杂的业务逻辑：
1. **OrderController.java (75KB)**: 负责订单同步、对账、业绩归因重算等操作的编排。
2. **ColonelActivityProductController.java (59KB)**: 混杂了招商活动商品的状态维护及数据权限逻辑。
3. **ProductController.java (53KB)**
4. **DouyinController.java (53KB)**: 包含了抖音 API 的直接回调逻辑和处理，应收敛至 Gateway / Webhook 层。

## 6. 事务一致性边界风险
- 项目中存在 120 多个 `@Transactional` 注解方法，大部分标注在巨型 Service 的公共方法上。
- **跨域大事务风险**: `SampleApplicationService` 和 `TalentService` 的方法在开启本地事务的同时，直接包含了跨领域的 Mapper 更新（如更新达人认领状态时，顺便更新寄样单或订单，或者进行外部 API 的调用）。若调用失败，会导致不必要的数据库回滚或资源锁定。

## 7. 事件发布一致性风险
目前有 3 个事件 (`OrderSyncedEvent`, `PerformanceCalculatedEvent`, `ConfigChangedApplicationEvent`) 和 5 个监听器。
- **本地事务提交一致性**: 订单同步持久化 `OrderSyncPersistenceService` 已经通过 `TransactionSynchronization.afterCompletion` 实现了在事务提交后发布事件（即 after-commit 模式），修复了之前的并发一致性风险。
- **缺乏统一 Outbox 设计**: 除订单同步外，其他事件（如配置变更、业绩计算等）缺乏统一的消息 Outbox 保障，在异常情况下可能导致事件丢失或不一致。
- **监听器跨域耦合**: `OrderSyncedEventListener` 监听器直接注入了 `TalentClaimMapper` (Talent) 以及 `BusinessRuleConfigService` 并修改了达人防骚扰保护期。事件驱动虽解耦了同步调用，但在监听器内部又重新引入了强耦合。

## 8. DTO/Entity/VO 混乱依赖现状
- **直接返回 Entity**: 许多 Controller 仍直接返回 JPA / MyBatis-Plus 的 Entity 实体对象给前端，导致内部数据库结构直接暴露。
- **入参使用 Entity / 跨域 DTO 混用**: Service 方法接收的参数经常是直接从前端传入的 Controller 层 DTO，或者是直接将 Entity 从一层传到另一层。
- **缺少防腐层 (ACL)**: 外部抖音网关接口的实体数据直接渗透到了核心业务 Service 中，使得核心逻辑直接依赖第三方结构。

## 9. Facade 收敛优先级
推荐 Facade 收敛的优先级如下（从高到低）：
1. **用户域 (User)**: 注入点最广（几乎每个 Service 都注入了 `SysUserMapper`），应最先收敛为 `UserFacade`，防止用户信息越界。
2. **配置域 (Config)**: 配置读取分散，应收敛为 `ConfigFacade` 统一缓存及读取入口。
3. **达人域 (Talent)**: 达人信息查询和状态控制极度网状，收敛至 `TalentFacade`。
4. **订单域 (Order)**: 业绩和商品强依赖订单状态，收敛至 `OrderFacade`。

## 10. 第一批 DDD 重构子任务推荐
根据本次审查，第一批推进的子任务为：
- `DDD-FACADE-USER-001`: 实现 `UserFacade` 接口，替代其他 Service 中对 `SysUserMapper` 的直接依赖。
- `DDD-FACADE-CONFIG-001`: 实现 `ConfigFacade` 接口，隔离对全局配置库的散落访问。
- `DDD-FACADE-ORDER-001`: 实现 `OrderFacade`，隔离寄样和业绩对订单 Mapper 的越界访问。

## 11. 当前绝对禁止做的事项
- **禁止进行全局包结构物理迁移**：当前包高度网状，直接移动包会导致大面积编译报错和代码冲突，第一阶段只做接口 Facade 隔离。
- **禁止同时重构多个领域的 Service**：如 `ProductService` 与 `SampleApplicationService` 必须隔离在独立任务中，逐一进行。
- **禁止在重构任务中加入业务功能修改或 Bug 修复**：必须保证重构前后行为一致、测试表现一致。

## 12. 审计结论
当前 SaaS V1 系统的 DDD 结构尚处于高度扁平、网状耦合的初级阶段。系统的核心闭环链条（渠道、招商、管理）具有强耦合的实体依赖特征。为达成渐进式重构，应当坚决贯彻 **“先 Facade 隔离，再防护测试跟进，最后进行逻辑内聚与包结构调整”** 的 Phase 0-3 路线，切勿急躁进行全局包迁移。

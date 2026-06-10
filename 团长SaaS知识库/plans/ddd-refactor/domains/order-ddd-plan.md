---
kb_id: "KB-PLAN-DDD-DOMAIN-ORDER"
title: "订单域 DDD 计划"
domain: "order"
category: "ddd_plan"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 14:50:00"
related_files:
  - "D:\\Projects\\SAAS\\docs\\领域"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-audit-order-001-20260608-145000.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# 订单域 DDD 计划

## 1. 当前领域职责

订单同步、原始订单落库、默认归因、双轨金额事实、pick_source 映射、6468/2704 上游适配。

## 2. 当前主要代码位置

OrderSyncService.java 1147 行、OrderSyncPersistenceService.java、OrderService.java、OrderQueryService.java、Order6468PaginationDryRunService.java；OrderController；ColonelsettlementOrderMapper、OrderSyncDedupClaimMapper；RealDouyinOrderGateway。

## 3. 当前主要 Service / Controller / Mapper

见上一节；本轮仅做只读统计，未修改任何代码。

## 4. 当前 DDD 问题

同步编排、上游适配、持久化和事件发布边界仍需继续拆分；afterCommit 已修但历史缺口需 backfill；真实 pick_source 样本仍不足。

## 5. 推荐重构方向

先跨域/订单审查，再补同步测试，后续新增 OrderDomainFacade 和隔离 DouyinOrderGateway。

## 6. 第一批任务

DDD-AUDIT-ORDER-001、DDD-TEST-ORDER-SYNC-001、DDD-FACADE-ORDER-001

## 7. 禁止先做的事

禁止先迁包；禁止同时改多个领域；禁止把业务修复混入重构；禁止改变接口契约或数据库结构。

## 8. 需要补的测试

mvn -f backend/pom.xml -Dtest=OrderSyncServiceTest,OrderSyncPersistenceServiceTest,OrderControllerTest test

## 9. 验证命令

A 类审查执行 git diff --check + 只读扫描报告。B/C/D 类按任务卡执行 mvn -f backend/pom.xml -Dtest=OrderSyncServiceTest,OrderSyncPersistenceServiceTest,OrderControllerTest test 或更小 targeted tests。

## 10. 相关 KB 领域文档链接

- ../../domains-业务领域/06-order-domain-订单域.md
- [任务矩阵](../02-task-matrix.md)

## 11. 订单域只读审查结论 (2026-06-08 14:50:00)
- 订单域只读审查已完成，详见 [ddd-audit-order-001.md](file:///D:/Docs/Books/my%20second%20brain/%E5%9B%A2%E9%95%BFSaaS%E7%9F%A5%E8%AF%86%E5%BA%93/plans/ddd-refactor/audits/ddd-audit-order-001.md)。
- **核心风险**: 上游 API 实体字段（如 colonel_order_info 等嵌套 Map）直接渗透进了 OrderSyncService 逻辑层，未真正建立防腐层 (ACL)；OrderSyncService (1147行) 是典型的上帝服务，承担了过多的网络、转换、编排逻辑。
- **推荐任务顺序**:
  1. `DDD-TEST-ORDER-SYNC-001` (建立订单同步的单测保护)
  2. `DDD-FACADE-ORDER-001` (建立订单 Facade 隔离层)
  3. `DDD-POLICY-ORDER-ATTRIBUTION-001` (剥离归因策略)
  4. `DDD-INFRA-ORDER-GATEWAY-001` (网关防腐隔离)


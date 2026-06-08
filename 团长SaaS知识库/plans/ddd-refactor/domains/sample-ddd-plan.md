---
kb_id: "KB-PLAN-DDD-DOMAIN-SAMPLE"
title: "寄样域 DDD 计划"
domain: "sample"
category: "ddd_plan"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 15:15:00"
related_files:
  - "D:\\Projects\\SAAS\\docs\\领域"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-audit-sample-001-20260608-151500.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# 寄样域 DDD 计划

## 1. 当前领域职责

申请、审核、发货、签收、待交作业、完成、7 天限制校验、寄样状态机。

## 2. 当前主要代码位置

`SampleApplicationService.java` (3696 行)、`SampleLifecycleService.java`、`SampleEligibilityService.java`、`ProductQuickSampleService.java`；`SampleController`；`SampleRequestMapper`、`SampleStatusLogMapper`。

## 3. 当前主要 Service / Controller / Mapper

见上一节；本轮仅做只读统计，未修改任何代码。

## 4. 当前 DDD 问题与风险

- `SampleApplicationService` 过于臃肿 (3696 行)，直接继承了 `BaseController`，将 API 处理层和应用逻辑编排、权限过滤甚至参数格式化全部混合在一起，是一个巨大的 God Service。
- Mapper / Repository 横穿极为严重：`SampleApplicationService` 与 `SampleLifecycleService` 直接操作了其它域的数据表（如 `ProductMapper`、`ProductOperationStateMapper`、`TalentMapper`、`TalentClaimMapper` 等），甚至通过多表 JOIN 和复杂的 SQL 实现了跨域的数据校验。
- 事务和事件边界不清：虽然大部分写操作封装在 `SampleWriteTransactionService.execute` 内运行，但各状态流转之间缺少统一的业务中介。订单触发自动完成的 `SampleLifecycleService` 直接由订单同步任务驱动，并使用 Native SQL 关联多表来进行样本负责人的匹配及 LIMIT 1 提取。
- 权限与数据隔离混乱：招商专员与渠道人员的数据范围控制在 Controller-Service 代码级直接与业务逻辑糅合，导致难以进行核心业务的单元测试。

## 5. 推荐重构方向

先审查状态机和订单完成条件，完成 Phase 1 相关的测试保护（订单同步测试与寄样周期测试），再提取 Facade 隔离依赖，最后重构提取 `SampleApplyPolicy` / `SampleCompletionPolicy`。

## 6. 第一批任务

DDD-AUDIT-SAMPLE-001、DDD-TEST-SAMPLE-LIFECYCLE-001、DDD-POLICY-SAMPLE-COMPLETE-001

## 7. 禁止先做的事

禁止先迁包；禁止同时改多个领域；禁止把业务修复混入重构；禁止改变接口契约或数据库结构。

## 8. 需要补的测试

`mvn -f backend/pom.xml -Dtest=SampleLifecycleServiceTest,SampleControllerTest test`

## 9. 验证命令

A 类审查执行 git diff --check + 只读扫描报告。B/C/D 类按任务卡执行 `mvn -f backend/pom.xml -Dtest=SampleLifecycleServiceTest,SampleControllerTest test` 或更小 targeted tests。

## 10. 相关 KB 领域文档链接

- [05-sample-domain.md](../../domains/05-sample-domain.md)
- [ddd-audit-sample-001.md](../audits/ddd-audit-sample-001.md)
- [任务矩阵](../02-task-matrix.md)

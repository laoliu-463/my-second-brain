---
kb_id: "KB-PLAN-DDD-DOMAIN-PERFORMANCE"
title: "业绩域 DDD 计划"
domain: "performance"
category: "ddd_plan"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 15:00:00"
related_files:
  - "D:\\Projects\\SAAS\\docs\\领域"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-audit-performance-001-20260608-150000.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# 业绩域 DDD 计划

## 1. 当前领域职责

performance_records、final_channel/final_recruiter、服务费收益、招商提成、渠道提成、退款冲正、业绩补算。

## 2. 当前主要代码位置

PerformanceCalculationService.java、PerformanceBackfillService.java、PerformanceSummaryService.java、PerformanceQueryService.java、PerformanceMetricsQueryService.java；PerformanceController；PerformanceRecordMapper。

## 3. 当前主要 Service / Controller / Mapper

见上一节；本轮仅做只读统计，未修改任何代码。

## 4. 当前 DDD 问题

公式和查询边界需继续拆分；历史 settle_amount 污染和 anti-join 缺口需单独任务；分析模块不能反向重算业绩。

## 5. 推荐重构方向

先审查计算/补算/公式，再补业绩计算测试，再提 PerformanceCalculationPolicy。

## 6. 第一批任务

DDD-AUDIT-PERFORMANCE-001、DDD-TEST-PERFORMANCE-CALC-001、DDD-FACADE-PERFORMANCE-001

## 7. 禁止先做的事

禁止先迁包；禁止同时改多个领域；禁止把业务修复混入重构；禁止改变接口契约或数据库结构。

## 8. 需要补的测试

mvn -f backend/pom.xml -Dtest=PerformanceCalculationServiceTest,PerformanceBackfillServiceTest,ServiceFeeMoneyFormula8291Test test

## 9. 验证命令

A 类审查执行 git diff --check + 只读扫描报告。B/C/D 类按任务卡执行 mvn -f backend/pom.xml -Dtest=PerformanceCalculationServiceTest,PerformanceBackfillServiceTest,ServiceFeeMoneyFormula8291Test test 或更小 targeted tests。

## 10. 相关 KB 领域文档链接

- ../../domains/07-performance-domain.md
- [任务矩阵](../02-task-matrix.md)

## 11. 业绩域只读审查结论 (2026-06-08 15:00:00)
- 业绩域只读审查已完成，详见 [ddd-audit-performance-001.md](file:///D:/Docs/Books/my second brain/团长SaaS知识库/plans/ddd-refactor/audits/ddd-audit-performance-001.md)。
- **核心风险**: `CommissionService` 存在对系统配置表 `system_config` 的直接 Mapper/SQL 越界读取；`PerformanceCalculationService` 承载了太多的流程和映射细节。
- **推荐任务顺序**:
  1. `DDD-TEST-PERFORMANCE-CALC-001` (建立双轨公式单测保护)
  2. `DDD-FACADE-PERFORMANCE-001` (建立业绩 Facade 隔离层)
  3. `DDD-POLICY-PERFORMANCE-CALC-001` (剥离提成与收益 Policy)
  4. `DDD-QUERY-PERFORMANCE-SUMMARY-001` (封装汇总查询以解耦分析模块的耦合)


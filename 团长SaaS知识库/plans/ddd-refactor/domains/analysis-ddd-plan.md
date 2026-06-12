---
kb_id: "KB-PLAN-DDD-DOMAIN-ANALYSIS"
title: "分析模块 DDD 计划"
domain: "analysis"
category: "ddd_plan"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 13:59:08"
related_files:
  - "D:\\Projects\\SAAS\\docs\\领域"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# 分析模块 DDD 计划

## 1. 当前领域职责

dashboard 查询、汇总表、指标卡片、趋势、排行、导出，只读展示。

## 2. 当前主要代码位置

data/DataApplicationService.java 2280 行、DashboardService.java 1139 行、DashboardPerformanceSummaryService.java；DataController、DashboardController；前端 data/index.vue、dashboard/index.vue、OrderList.vue。

## 3. 当前主要 Service / Controller / Mapper

见上一节；本轮仅做只读统计，未修改任何代码。

## 4. 当前 DDD 问题

DataApplicationService 继承 BaseController 且包含订单明细/汇总/指标构造；Dashboard summary 双轨和历史污染仍需专项；只读边界需防止重算归属。

## 5. 推荐重构方向

先审查 dashboard 查询路径和 summary API，再补 API/SQL 对账测试，后续整理 DashboardQueryService。

## 6. 第一批任务

DDD-AUDIT-ANALYSIS-001、DDD-TEST-DASHBOARD-RECON-001、DDD-APP-DASHBOARD-QUERY-001

## 7. 禁止先做的事

禁止先迁包；禁止同时改多个领域；禁止把业务修复混入重构；禁止改变接口契约或数据库结构。

## 8. 需要补的测试

mvn -f backend/pom.xml -Dtest=DashboardServiceTest,DataControllerTest,PerformanceSummaryServiceTest test

## 9. 验证命令

A 类审查执行 git diff --check + 只读扫描报告。B/C/D 类按任务卡执行 mvn -f backend/pom.xml -Dtest=DashboardServiceTest,DataControllerTest,PerformanceSummaryServiceTest test 或更小 targeted tests。

## 10. 相关 KB 领域文档链接

- ../../domains-业务领域/08-analysis-domain-分析域.md
- [任务矩阵](../02-task-matrix.md)

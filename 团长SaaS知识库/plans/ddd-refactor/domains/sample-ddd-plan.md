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

# 寄样域 DDD 计划

## 1. 当前领域职责

申请、审核、发货、签收、待交作业、完成、7 天限制校验、寄样状态机。

## 2. 当前主要代码位置

sample/SampleApplicationService.java 3696 行、SampleLifecycleService.java、SampleEligibilityService.java、ProductQuickSampleService.java；SampleController；SampleRequestMapper、SampleStatusLogMapper。

## 3. 当前主要 Service / Controller / Mapper

见上一节；本轮仅做只读统计，未修改任何代码。

## 4. 当前 DDD 问题

SampleApplicationService 过大且继承 BaseController；状态机、查询过滤、展示转换和订单事件消费混合；真实自动完成仍依赖归因订单样本。

## 5. 推荐重构方向

先审查状态机和订单完成条件，再补状态机测试，之后提 SampleApplyPolicy / SampleCompletionPolicy。

## 6. 第一批任务

DDD-AUDIT-SAMPLE-001、DDD-TEST-SAMPLE-LIFECYCLE-001、DDD-POLICY-SAMPLE-COMPLETE-001

## 7. 禁止先做的事

禁止先迁包；禁止同时改多个领域；禁止把业务修复混入重构；禁止改变接口契约或数据库结构。

## 8. 需要补的测试

mvn -f backend/pom.xml -Dtest=SampleLifecycleServiceTest,SampleControllerTest test

## 9. 验证命令

A 类审查执行 git diff --check + 只读扫描报告。B/C/D 类按任务卡执行 mvn -f backend/pom.xml -Dtest=SampleLifecycleServiceTest,SampleControllerTest test 或更小 targeted tests。

## 10. 相关 KB 领域文档链接

- ../../domains/05-sample-domain.md
- [任务矩阵](../02-task-matrix.md)

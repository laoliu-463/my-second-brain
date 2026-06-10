---
kb_id: "KB-PLAN-DDD-DOMAIN-PRODUCT"
title: "商品域 DDD 计划"
domain: "product"
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

# 商品域 DDD 计划

## 1. 当前领域职责

商品库、活动商品、展示规则、转链、pick_source_mapping、快速寄样入口商品上下文。

## 2. 当前主要代码位置

ProductService.java 5457 行、ProductDisplayRuleService.java、PickSourceMappingService.java、ProductQuickSampleService.java；ProductController、ColonelActivityProductController；Product*Mapper、PickSourceMappingMapper。

## 3. 当前主要 Service / Controller / Mapper

见上一节；本轮仅做只读统计，未修改任何代码。

## 4. 当前 DDD 问题

ProductService 是当前最大 God Service；转链、展示、同步、映射编排混在同一服务；商品域和寄样域通过快速寄样入口耦合。

## 5. 推荐重构方向

先补展示规则和转链映射测试，再提 ProductDisplayPolicy 和 PromotionLinkApplicationService。

## 6. 第一批任务

DDD-AUDIT-PRODUCT-001、DDD-TEST-PRODUCT-DISPLAY-001、DDD-POLICY-PRODUCT-DISPLAY-001

## 7. 禁止先做的事

禁止先迁包；禁止同时改多个领域；禁止把业务修复混入重构；禁止改变接口契约或数据库结构。

## 8. 需要补的测试

mvn -f backend/pom.xml -Dtest=ProductDisplayRuleServiceTest,ProductServiceFilterTest,PickSourceMappingServiceTest test

## 9. 验证命令

A 类审查执行 git diff --check + 只读扫描报告。B/C/D 类按任务卡执行 mvn -f backend/pom.xml -Dtest=ProductDisplayRuleServiceTest,ProductServiceFilterTest,PickSourceMappingServiceTest test 或更小 targeted tests。

## 10. 相关 KB 领域文档链接

- ../../domains-业务领域/03-product-domain-商品域.md
- [任务矩阵](../02-task-matrix.md)

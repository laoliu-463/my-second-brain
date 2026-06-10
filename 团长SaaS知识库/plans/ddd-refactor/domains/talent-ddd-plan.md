---
kb_id: "KB-PLAN-DDD-DOMAIN-TALENT"
title: "达人域 DDD 计划"
domain: "talent"
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

# 达人域 DDD 计划

## 1. 当前领域职责

达人资料、认领、私海/公海、标签、地址、保护期、跟进。

## 2. 当前主要代码位置

TalentService.java、TalentQueryService.java、talent/profile/TalentProfileSyncService.java；TalentController、TalentProfileController；Talent*Mapper、TalentClaimMapper。

## 3. 当前主要 Service / Controller / Mapper

见上一节；本轮仅做只读统计，未修改任何代码。

## 4. 当前 DDD 问题

达人认领、地址、标签、第三方补充和寄样地址消费边界需要审查；gender 筛选缺口仍是当前事实。

## 5. 推荐重构方向

先只读审查达人认领/地址/标签，再补认领保护期测试，后续新增 TalentDomainFacade。

## 6. 第一批任务

DDD-AUDIT-TALENT-001、DDD-TEST-TALENT-CLAIM-001、DDD-FACADE-TALENT-001

## 7. 禁止先做的事

禁止先迁包；禁止同时改多个领域；禁止把业务修复混入重构；禁止改变接口契约或数据库结构。

## 8. 需要补的测试

mvn -f backend/pom.xml -Dtest=TalentServiceTest,TalentQueryServiceTest,TalentTagServiceTest test

## 9. 验证命令

A 类审查执行 git diff --check + 只读扫描报告。B/C/D 类按任务卡执行 mvn -f backend/pom.xml -Dtest=TalentServiceTest,TalentQueryServiceTest,TalentTagServiceTest test 或更小 targeted tests。

## 10. 相关 KB 领域文档链接

- ../../domains-业务领域/04-talent-domain-达人域.md
- [任务矩阵](../02-task-matrix.md)

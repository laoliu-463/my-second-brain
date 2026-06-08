---
kb_id: "KB-PLAN-DDD-DOMAIN-CONFIG"
title: "配置域 DDD 计划"
domain: "config"
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

# 配置域 DDD 计划

## 1. 当前领域职责

system_config、业务规则参数、提成比例、寄样限制天数、复制模板、缓存失效。

## 2. 当前主要代码位置

SysConfigService.java、RuleCenterService.java、CommissionRuleService.java、BusinessRuleConfigService.java；SysConfigController、RuleCenterController；SystemConfigMapper、CommissionRuleMapper。

## 3. 当前主要 Service / Controller / Mapper

见上一节；本轮仅做只读统计，未修改任何代码。

## 4. 当前 DDD 问题

配置读取和规则执行边界需要审查；缓存失效与审计链路需要防护测试；业务域直接读取配置的路径需要收敛。

## 5. 推荐重构方向

先盘点配置读取和缓存，再补缓存/审计测试，随后新增 ConfigDomainFacade。

## 6. 第一批任务

DDD-AUDIT-CONFIG-001、DDD-TEST-CONFIG-CACHE-001、DDD-FACADE-CONFIG-001

## 7. 禁止先做的事

禁止先迁包；禁止同时改多个领域；禁止把业务修复混入重构；禁止改变接口契约或数据库结构。

## 8. 需要补的测试

mvn -f backend/pom.xml -Dtest=SysConfigServiceTest,RuleCenterServiceTest,CommissionRuleServiceTest test

## 9. 验证命令

A 类审查执行 git diff --check + 只读扫描报告。B/C/D 类按任务卡执行 mvn -f backend/pom.xml -Dtest=SysConfigServiceTest,RuleCenterServiceTest,CommissionRuleServiceTest test 或更小 targeted tests。

## 10. 相关 KB 领域文档链接

- ../../domains/02-config-domain.md
- [任务矩阵](../02-task-matrix.md)

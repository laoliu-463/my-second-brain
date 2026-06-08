---
kb_id: "KB-PLAN-DDD-DOMAIN-CROSS"
title: "跨域 DDD 计划"
domain: "cross"
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

# 跨域 DDD 计划

## 1. 当前领域职责

跨域依赖、事件、Facade 收敛、事务一致性和知识库状态同步。

## 2. 当前主要代码位置

MapperScan 覆盖 mapper 和 domain.event；OrderSyncPersistenceService afterCommit；SysConfigService ConfigChangedEvent；Product/User domain event publisher tests。

## 3. 当前主要 Service / Controller / Mapper

见上一节；本轮仅做只读统计，未修改任何代码。

## 4. 当前 DDD 问题

Service / Mapper 横穿尚未系统审查；当前图谱存在高耦合社区和多个大 Service；事件一致性尚未统一 Outbox 设计。

## 5. 推荐重构方向

先执行 DDD-AUDIT-CROSS-DOMAIN-001，确定 Facade 收敛顺序和禁止跨域直接访问清单。

## 6. 第一批任务

DDD-AUDIT-CROSS-DOMAIN-001、DDD-OUTBOX-DESIGN-001

## 7. 禁止先做的事

禁止先迁包；禁止同时改多个领域；禁止把业务修复混入重构；禁止改变接口契约或数据库结构。

## 8. 需要补的测试

git diff --check；只读 cross-domain report；后续事件任务再跑 targeted tests。

## 9. 验证命令

A 类审查执行 git diff --check + 只读扫描报告。B/C/D 类按任务卡执行 git diff --check；只读 cross-domain report；后续事件任务再跑 targeted tests。 或更小 targeted tests。

## 10. 相关 KB 领域文档链接

- ../00-index.md
- [任务矩阵](../02-task-matrix.md)

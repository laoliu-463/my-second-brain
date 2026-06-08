---
kb_id: "KB-PLAN-DDD-DDD-AUDIT-PERFORMANCE-001"
title: "DDD-AUDIT-PERFORMANCE-001"
domain: "performance"
category: "task_card"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 15:00:00"
related_files:
  - "D:\\Projects\\SAAS\\harness\\TASK_ROUTING.md"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-audit-performance-001-20260608-150000.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# DDD-AUDIT-PERFORMANCE-001

## 1. 任务目标

审查 PerformanceCalculationService、补算、公式口径、冲正、汇总和分析模块消费边界。

## 2. 只读范围

本任务默认不改生产代码。若任务类型为 B/C，必须先在任务开始时重新声明允许修改文件；未声明前只读。

## 3. 读取文件

docs/领域/业绩域.md、harness/instructions/performance-domain.md、PerformanceCalculationService.java、PerformanceBackfillService.java、PerformanceRecordMapper.java、相关测试。

## 4. 输出文件

- D:\Projects\SAAS\harness\reports\<task-id>-YYYYMMDD-HHMMSS.md
- 更新本任务卡状态。
- 更新对应领域计划 and state 页。

## 5. 审查维度

领域职责是否越界；Controller 是否承载复杂业务规则；Service 是否同时承担编排、规则、持久化、外部 SDK；Mapper / Repository 是否跨域穿透；事务边界和事件发布是否可验证；测试是否能证明行为不变。

## 6. 验证要求

至少执行 git diff --check。若进入测试任务，执行任务卡指定 targeted tests。若缺真实样本，只能登记 BLOCKED_BY_SAMPLE。

## 7. 禁止事项

禁止改业务口径、接口契约、数据库结构；禁止顺手修 bug；禁止全局包迁移；禁止把未验证项写成 PASS.

## 8. 结果格式

现象 / 证据 / 推论 / 阶段性结论 / 下一步任务 / 风险。

## 9. 完成判定

有 evidence report；KB 任务页、领域页、state 页已更新；没有误改 Java/Vue/SQL/Docker/env。

## 10. 需要更新 of the KB 文件

- plans/ddd-refactor/tasks/ddd-audit-performance-001.md
- plans/ddd-refactor/domains/performance-ddd-plan.md
- plans/ddd-refactor/02-task-matrix.md

## 执行状态
- 状态: **DONE_AUDIT**
- 产出报告: [ddd-audit-performance-001.md](file:///D:/Docs/Books/my%20second%20brain/%E5%9B%A2%E9%95%BFSaaS%E7%9F%A5%E8%AF%86%E5%BA%93/plans/ddd-refactor/audits/ddd-audit-performance-001.md)
- Harness 报告:
  - 主报告: [ddd-audit-performance-001-20260608-150000.md](file:///d:/Projects/SAAS/harness/reports/ddd-audit-performance-001-20260608-150000.md)
  - 证据报告: [evidence-20260608-150000-ddd-audit-performance-001.md](file:///d:/Projects/SAAS/harness/reports/evidence-20260608-150000-ddd-audit-performance-001.md)
  - 复盘报告: [retro-20260608-150000-ddd-audit-performance-001.md](file:///d:/Projects/SAAS/harness/reports/retro-20260608-150000-ddd-audit-performance-001.md)
- 结论: 已理清业绩表持久化 upsert 链路、订单 afterCommit 事件的消费机制，明确了招商/渠道提成的多级比例读取优先级与公式。识别出在 CommissionService 中直接通过 JdbcTemplate 跨域读取配置表的架构风险。
- 下一任务建议: **DDD-AUDIT-SAMPLE-001** (寄样域只读审查)


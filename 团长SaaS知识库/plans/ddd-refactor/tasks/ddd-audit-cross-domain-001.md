---
kb_id: "KB-PLAN-DDD-DDD-AUDIT-CROSS-DOMAIN-001"
title: "DDD-AUDIT-CROSS-DOMAIN-001"
domain: "cross"
category: "task_card"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 14:40:00"
related_files:
  - "D:\\Projects\\SAAS\\harness\\TASK_ROUTING.md"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-audit-cross-domain-001-20260608-144000.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# DDD-AUDIT-CROSS-DOMAIN-001

## 1. 任务目标

识别跨域 Mapper / Service 横穿、事件一致性风险、Facade 收敛顺序和禁止先做的包迁移项。

## 2. 只读范围

本任务默认不改生产代码。若任务类型为 B/C，必须先在任务开始时重新声明允许修改文件；未声明前只读。

## 3. 读取文件

CLAUDE.md、docs/README.md、harness/CURRENT_STATE.md、harness/TASK_ROUTING.md、docs/领域/*.md、backend/src/main/java/**/*.java、backend/src/test/java/**/*.java。

## 4. 输出文件

- D:\Projects\SAAS\harness\reports\<task-id>-YYYYMMDD-HHMMSS.md
- 更新本任务卡状态。
- 更新对应领域计划和 state 页。

## 5. 审查维度

领域职责是否越界；Controller 是否承载复杂业务规则；Service 是否同时承担编排、规则、持久化、外部 SDK；Mapper / Repository 是否跨域穿透；事务边界和事件发布是否可验证；测试是否能证明行为不变。

## 6. 验证要求

至少执行 git diff --check。若进入测试任务，执行任务卡指定 targeted tests。若缺真实样本，只能登记 BLOCKED_BY_SAMPLE。

## 7. 禁止事项

禁止改业务口径、接口契约、数据库结构；禁止顺手修 bug；禁止全局包迁移；禁止把未验证项写成 PASS。

## 8. 结果格式

现象 / 证据 / 推论 / 阶段性结论 / 下一步任务 / 风险。

## 9. 完成判定

有 evidence report；KB 任务页、领域页、state 页已更新；没有误改 Java/Vue/SQL/Docker/env。

## 10. 需要更新的 KB 文件

- plans/ddd-refactor/tasks/ddd-audit-cross-domain-001.md
- plans/ddd-refactor/domains/cross-ddd-plan.md
- plans/ddd-refactor/02-task-matrix.md

## 执行状态
- 状态: **DONE_AUDIT**
- 产出报告: [ddd-audit-cross-domain-001.md](file:///D:/Docs/Books/my%20second%20brain/%E5%9B%A2%E9%95%BFSaaS%E7%9F%A5%E8%AF%86%E5%BA%93/plans/ddd-refactor/audits/ddd-audit-cross-domain-001.md)
- Harness 报告:
  - 主报告: [ddd-audit-cross-domain-001-20260608-144000.md](file:///d:/Projects/SAAS/harness/reports/ddd-audit-cross-domain-001-20260608-144000.md)
  - 证据报告: [evidence-20260608-144000-ddd-audit-cross-domain-001.md](file:///d:/Projects/SAAS/harness/reports/evidence-20260608-144000-ddd-audit-cross-domain-001.md)
  - 复盘报告: [retro-20260608-144000-ddd-audit-cross-domain-001.md](file:///d:/Projects/SAAS/harness/reports/retro-20260608-144000-ddd-audit-cross-domain-001.md)
- 结论: 已确认 9 个领域划分、胖 Service（尤其是 DataApplicationService 的 Controller 属性）和跨域 Mapper 穿透，Facade 优先级为 User -> Config -> Talent -> Order。符合只读审查门禁。

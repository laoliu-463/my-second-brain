---
kb_id: "KB-PLAN-DDD-05-TESTING"
title: "DDD 测试策略"
domain: "harness"
category: "testing_strategy"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 13:59:08"
related_files:
  - "D:\\Projects\\SAAS\\docs\\09-测试验收总览.md"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# DDD 测试策略

## DDD 重构前必须补哪些测试

1. 订单同步：6468/2704、分页、水位、幂等、afterCommit 事件。
2. 业绩计算：最终归属、服务费收入/收益双轨、提成、退款冲正。
3. 寄样状态机：申请、审核、发货、签收、待交作业、完成、非法流转。
4. 商品展示规则：DISPLAYING/HIDDEN/PENDING、去重、推广中入库、转链映射。
5. 用户数据范围：admin/group/self 和越权负例。
6. 配置缓存：读取、保存、审计、缓存失效。
7. Dashboard 对账：API 与 SQL 双轨指标一致。

## 每个领域最低测试保护要求

用户域需 admin/group/self；配置域需缓存与审计；商品域需展示和转链映射；达人域需认领/地址/标签；寄样域需状态机；订单域需同步幂等；业绩域需公式和冲正；分析模块需 API/SQL 对账。

## Targeted / Full / Frontend / real-pre / E2E

A 类只读任务只需 git diff --check 和误改检查。B 类跑 targeted tests。C/D 类后端重构至少跑 targeted tests，核心域追加 backend full tests 或 E2E。前端任务跑 typecheck、Vitest、必要页面 smoke。修改 Java/Vue/SQL/Docker 后才需要重启 real-pre；docs-only 计划任务不重启。订单、业绩、寄样、看板链路变更必须做 SQL 只读对账。

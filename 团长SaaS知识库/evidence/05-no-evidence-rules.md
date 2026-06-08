---
kb_id: evidence/05-no-evidence-rules
title: 无证据处理规则
domain: evidence
category: evidence-no-evidence
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - governance/04-domain-status.md
  - harness/reports/evidence-*.md
related_reports: []
forbidden_misread:
  - 缺证据不写 PASS
  - 缺证据不写 PARTIAL PASS
---

# 无证据处理规则

## 1. 用途

明确"无证据"时的输出规范：阶段性结论、不写 PASS、不写"业务闭环"。

## 2. 结论模板

```
当前结论：PENDING / BLOCKED_BY_*
关键证据：缺失
阻塞详情：<...>
解封条件：<...>
下次复测：<...>
```

## 3. 阶段记录

- 不写 PASS
- 不写 PARTIAL PASS
- 不写"业务闭环通过"
- 不写"渠道归因闭环通过"（除非有 pick_source 样本）
- 不写"结算轨完成"（除非 anti-join + 双轨金额 + 冲正均通过）

## 4. 必做

- 显式记录缺什么证据
- 写明下一步动作（拉数据 / 拿 Token / 部署脚本）
- 把阶段性结论写入 evidence / reports

## 5. 复测入口

- real-pre P0 预检：npm run e2e:real-pre:p0:preflight
- 测试 P0 基线：npm run e2e:v1-p0
- 后端回归：cd backend && mvn test

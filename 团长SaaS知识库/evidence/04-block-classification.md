---
kb_id: evidence/04-block-classification
title: BLOCK 分类
domain: evidence
category: evidence-block-classification
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - governance/04-domain-status.md
  - docs/09-测试验收总览.md
related_reports: []
forbidden_misread:
  - BLOCKED_BY_SAMPLE 不得升级 PASS
  - BLOCKED_BY_EXTERNAL 不得升级 PASS
---

# BLOCK 分类

## 1. 用途

为 V1 验收中的"阻塞"做明确分类，避免误判 PASS。

## 2. BLOCK 类型

| 类型 | 含义 | 升级条件 |
| --- | --- | --- |
| BLOCKED_BY_SAMPLE | 缺真实 pick_source / 真实订单 | 样本就位 |
| BLOCKED_BY_EXTERNAL | 上游 / 凭据 / Token 缺失 | 上游就位 |
| FAILED | 业务逻辑 / 数据不一致 | 修复 + 重测 |
| RISK_ACCEPTED_BY_USER | 用户书面接受风险 | 真实闭环后转 PASS |
| PARTIAL | 部分通过，部分不通过 | 拆分子任务 |

## 3. 升级路径

```
PENDING → BLOCKED_BY_SAMPLE → READY（样本就位）
PENDING → BLOCKED_BY_EXTERNAL → READY（上游就位）
FAILED → RISK_ACCEPTED_BY_USER → PASS（需三环）
```

## 4. 禁止

- 禁止把 BLOCKED_BY_SAMPLE 写 PASS
- 禁止把 BLOCKED_BY_EXTERNAL 写 PASS
- 禁止在缺数据时写 PARTIAL PASS

## 5. 证据要求

每条 BLOCK 必须：
- 记录阻塞详情
- 关联证据（脚本 / SQL / 日志）
- 写明预期解封条件

---
title: Agent 控制面页面元数据规范
type: procedure
status: active
created_at: 2026-06-27
updated_at: 2026-06-27
source_level: none
sources: []
raw_evidence: []
related:
  - "[[KB_PROTOCOL]]"
  - "[[PATH_RULES]]"
tags:
  - agent-governance
  - schema
maintainers:
  - codex
confidence: 1.0
---

# Agent 控制面页面元数据规范

## 适用范围

本规范适用于新建或本次修改过的正式知识页。历史页面暂不强制全量整改。

严格 schema 主要适用于 `知识库/` 下的正式知识页面。以下目录可按自身职责放宽字段要求，但仍建议保留 frontmatter：

- `知识库/_meta/`
- `知识库/_review/`
- `知识库/sources/`
- `知识库/90-来源与映射/`

## 推荐 frontmatter

```yaml
---
title: ""
type: concept | entity | source | synthesis | map | procedure | index | review | note
status: draft | active | review | deprecated | archived
created_at: 2026-06-27
updated_at: 2026-06-27
source_level: none | weak | normal | strong
sources:
  - ""
raw_evidence:
  - ""
related:
  - ""
tags:
  - ""
maintainers:
  - agent
confidence: 0.0
---
```

## 过渡期兼容

旧页面常用 `created` 与 `updated`。过渡期内，新建页面推荐使用 `created_at` 与 `updated_at`；修改旧页面时可以保留原字段。

校验脚本应同时接受：

- `updated_at`
- `updated`

## 字段说明

- `title`：页面标题。
- `type`：页面类型。
- `status`：生命周期状态。
- `created_at` / `created`：创建日期。
- `updated_at` / `updated`：最后维护日期。
- `source_level`：来源强度，内部规范可使用 `none`。
- `sources`：来源页、来源映射页或外部来源。
- `raw_evidence`：可回溯的 raw 文件路径。
- `related`：相关 wiki 链接。
- `tags`：检索标签。
- `maintainers`：维护者或 agent 名称。
- `confidence`：可信度，范围 0 到 1。

## 来源要求

正式知识页必须满足以下至少一项：

- 有 `sources` 字段。
- 有 `raw_evidence` 字段。
- 明确写出 `source_level: none`，表示该页是内部规范、索引或无外部来源的维护说明。

不得伪造来源链接。raw 文件缺失时，应写入待核查或报告，而不是补一个不存在的链接。

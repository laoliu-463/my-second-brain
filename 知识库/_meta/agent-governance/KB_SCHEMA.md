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
  - "raw/sources/..."
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
- `sources`：机器可读来源提示，可填写 raw 路径、来源映射页或外部来源；它不能替代正文中的 `## 原文链接`。
- `raw_evidence`：可回溯的 raw 文件路径，优先指向 `raw/sources/...` 下的真实原文附件。
- `related`：相关 wiki 链接。
- `tags`：检索标签。
- `maintainers`：维护者或 agent 名称。
- `confidence`：可信度，范围 0 到 1。

## 来源要求

正式知识页必须优先满足以下要求：

- 页面正文有 `## 原文链接` 区块。
- `## 原文链接` 区块中至少有一个 Obsidian Wiki 链接直接指向真实存在的 `raw/sources/...` 原始文件。
- raw 原文通过 Obsidian backlinks / graph / 脚本索引能反查引用它的知识页。

以下页面可以豁免 raw 原文直链：

- 明确写出 `source_level: none` 的内部规范、索引、流程或无外部来源维护说明。
- 暂无 raw 文件但已在 `_review/`、维护报告或页面中明确标记“原文缺失待核查”的过渡页。

`sources` 与 `raw_evidence` 字段仍可保留，用于脚本检索、批量审计和外部来源映射，但不是来源完整性的唯一判据。

不得伪造来源链接。raw 文件缺失时，应写入待核查或报告，而不是补一个不存在的链接。

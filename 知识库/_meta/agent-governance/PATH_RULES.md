---
title: Agent 控制面路径规则
type: procedure
status: active
created_at: 2026-06-27
updated_at: 2026-06-27
source_level: none
sources: []
raw_evidence: []
related:
  - "[[KB_PROTOCOL]]"
  - "[[KB_SCHEMA]]"
tags:
  - agent-governance
  - path-rules
maintainers:
  - codex
confidence: 1.0
---

# Agent 控制面路径规则

## 总原则

本知识库按证据、正式知识、来源映射、审计报告分层维护。Agent 不应把临时材料、原始证据和正式知识混在同一层。

## `00-收集箱/` 与 `00-收件箱/`

用途：资料入口、草稿和待归位文本。

Agent 可以：

- 读取和整理。
- 将原始材料保留到 `raw/`。
- 为后续处理生成待复核说明。

Agent 不应：

- 把入口材料直接当作最终知识。
- 删除未处理材料，除非用户明确要求。
- 在未建立来源链路时迁入正式知识层。

## `raw/`

用途：原始证据层。

Agent 可以：

- 新增原始资料。
- 新增来源说明或校验信息。
- 计算 hash 并建立 source mapping。

Agent 禁止：

- 改写已有原始资料正文。
- 为了优化表达修改 raw 内容。
- 删除或重命名 raw 内容，除非用户明确要求并已记录影响。

## `知识库/`

用途：正式 wiki 页面与知识图谱节点。

Agent 可以：

- 新增或修改正式知识页。
- 维护 `sources/`、`90-来源与映射/`、`concepts/`、`entities/`、`maps/`、`syntheses/`。
- 建立交叉引用和来源追踪。

Agent 必须：

- 新建或修改正式页时保留 frontmatter。
- 事实性内容保留来源链路。
- 重要新页接入 `index.md` 或局部索引页。
- 涉及 `知识库/` 的成批改动必须追加 `log.md`。

## `知识库/_review/`

用途：来源不足、分类不确定、内容冲突或待人工判断的问题页。

以下情况优先写入 `_review/`：

- 来源不足。
- 与已有知识冲突。
- 涉及敏感信息。
- 无法确认分类。
- 大规模重构前的草案。

## `知识库/_meta/`

用途：治理规范、迁移清单、内容清单和维护元数据。

Agent 可以维护本目录下的治理文档，但不得把普通知识正文放入 `_meta/`。

## `.obsidian/`

用途：Obsidian 本地配置。

Agent 默认不得修改 `.obsidian/`。需要修改时必须由用户明确提出，并说明影响范围与回滚方式。

## `tools/` 与 `tests/`

用途：本地维护脚本和验证用例。

修改 `tools/` 后应运行对应语法检查或单元测试。PowerShell 脚本至少应通过实际命令冒烟；Python 脚本至少应通过 `py_compile` 或相关 unittest。

## 编号目录冲突

当前存在两个 `05-*` 目录：

- `知识库/05-认知与成长/`
- `知识库/05-智能体与Agent体系/`

Agent 不得自动重命名这两个目录。

新增 Agent、记忆层、AI 工具、MCP、Claude/Codex/Cursor 相关知识时，使用 `知识库/05-智能体与Agent体系/`。

新增认知成长、学习方法、个人成长相关知识时，使用 `知识库/05-认知与成长/`。

目录重命名必须由用户明确批准。

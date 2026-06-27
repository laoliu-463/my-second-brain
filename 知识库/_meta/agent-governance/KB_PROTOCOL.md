---
title: Agent 控制面维护协议
type: procedure
status: active
created_at: 2026-06-27
updated_at: 2026-06-27
source_level: none
sources: []
raw_evidence: []
related:
  - "[[PATH_RULES]]"
  - "[[KB_SCHEMA]]"
tags:
  - agent-governance
  - knowledge-ops
maintainers:
  - codex
confidence: 1.0
---
# Agent 控制面维护协议

## 定位

本协议定义所有 Agent 维护本知识库时的最小流程。根目录 `AGENTS.md` 是主入口；本目录下的治理文档负责把规则拆成可执行、可校验的维护协议。

## 接管前检查

任何维护任务开始前，先读取：

1. `AGENTS.md`
2. `index.md`
3. `log.md` 最近 20 条
4. 本目录下的 `PATH_RULES.md` 与 `KB_SCHEMA.md`

如果任务只读查询，可只读取前三项；如果任务会改文件，必须读取全部四项。

## Ingest 流程

用于处理 `00-收集箱/` 或 `00-收件箱/` 中的新材料。

1. 判断材料是否已有对应 raw 原文、正式页或辅助来源映射。
2. 保留原始材料到 `raw/`，不得改写已有 raw 文件正文。
3. 需要生成正式知识页时，按 `KB_SCHEMA.md` 添加 frontmatter，并在正文设置 `## 原文链接` 区块，直接链接到真实存在的 `raw/sources/...` 原文附件。
4. 只有当一份来源影响多个页面、需要保留外部 URL/hash/批量映射或审计关系时，才更新 `知识库/sources/` 或 `知识库/90-来源与映射/`。
5. 不得用新建 source 元数据页替代知识页到 raw 原文的直接可点击链接。
6. 更新相关索引页或 `index.md`。
7. 追加 `log.md`，记录改动范围、原因、影响文件、待复查项。

## Promote 流程

用于把来源材料提升为正式 wiki 页面。

1. 先搜索现有页面，优先更新已有页，避免重复页。
2. 新建正式页必须包含 frontmatter。
3. 事实性内容必须优先通过页面内 `## 原文链接` 回溯到 `raw/sources/...` 原文附件。
4. 分类不确定、来源不足或存在冲突时，先写入 `知识库/_review/`。
5. 重要新页必须能从 `index.md` 或局部索引页到达。
6. 多对多来源关系、外部 canonical URL、hash 或批量审计信息可补充到 `知识库/sources/` 或 `90-来源与映射/`，但不能替代第 3 步。
7. 追加 `log.md`。

## Review 流程

用于检查本次改动是否满足知识库治理要求。

1. 检查 `raw/` 是否被改写、删除或重命名。
2. 检查正式知识页是否有 frontmatter。
3. 检查正式知识页是否存在 `## 原文链接` 区块，并且其中的 `raw/sources/...` Wiki 链接能命中真实 raw 文件；`source_level: none` 的内部规范、索引和无外部来源页除外。
4. 检查新增重要页面是否可导航。
5. 检查 `log.md` 是否记录本次改动。
6. 运行 `tools/kb_validate.ps1 -ChangedOnly`。

## Audit 流程

用于全库或专题级健康检查。

1. 明确审计范围。
2. 运行现有维护脚本或 `tools/kb_validate.ps1`。
3. 生成报告到 `06-报告证据/`。
4. 只记录问题，不在无依据时大规模自动修复。
5. 追加 `log.md`。

## 完成标准

维护任务完成前必须满足：

- 本次改动范围清楚。
- `raw/` 既有证据未被改写。
- 新建或修改的正式页符合 schema。
- 必要来源链路存在，且正式知识页到 raw 原文附件的直接链接可点击、可反查。
- `index.md` 或局部索引已接住重要新页。
- `log.md` 已追加记录。
- 校验脚本已执行或明确说明无法执行的原因。

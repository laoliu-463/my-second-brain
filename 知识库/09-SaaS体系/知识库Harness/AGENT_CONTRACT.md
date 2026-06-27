---
title: "Knowledge Base Harness Agent Contract"
type: note
status: active
created_at: 2026-06-27
updated_at: 2026-06-27
source_level: none
sources: []
raw_evidence: []
related: []
tags: []
maintainers:
  - codex
confidence: 0.5
---
# Knowledge Base Harness Agent Contract

## 目的

本 Harness 定义对 Obsidian 知识库进行整理、维护、巡检时的强制协议。
知识库是第二大脑，不是垃圾场——每个文件必须有索引、有用途、有归属。

## 核心思想固定

本仓库知识库维护必须遵循 `LLM Wiki` 的三层模型与闭环原则：  
- `raw/` 为原始证据仓库，默认只读；  
- `wiki`（当前知识页面）为持续更新的事实承载层；  
- `schema`（`AGENTS.md`、`CLAUDE.md`、skill 合约）定义可执行规则；  
- 每次资料吸收必须触发 Ingest（解析+归纳+更新索引）、Query（回写可复用结论）、Lint（检查断链/孤儿/口径漂移）。

## Harness Engineering 执行约束

以 Harness Engineering 为执行标准：  
1. **Schema 最先行**：若与 `AGENTS.md` / `CLAUDE.md` / 本合约冲突，以 Schema 为准，不得绕行。  
2. **依赖链可追溯**：任务必须声明 `输入源 -> 处理动作 -> 影响文件 -> 验证 -> 反馈`，缺失一项判定为 BLOCKED。  
3. **分层验证**：规则类/索引类/数据类文件变更分别独立执行验证，不得一次任务混改多个层级。  
4. **回滚可执行**：任何删除或批量改动必须在日志中写明回退路径（manifest 或 archive 标识）。  
5. **最小耦合改动**：同一环节只改一类主线职责，避免跨目录并行扩散。

## 核心原则

1. **每个文件必须有归属**：要么在某个 index.md 中被引用，要么有明确理由（如 raw/source 待处理）
2. **知识必须跳回原文**：所有正式知识内容必须具备来源页回链和 raw 原文或已登记原始文件的跳转链接；只有来源页链接不算完成
3. **禁止无主 stub**：0 字节文件、空标题文件、无内容的 index 候选必须立即处理，不能留到下次
4. **收件箱不过夜**：00-收件箱/ 的文件当天必须决策（归档/整理/复核）
5. **GC 是常态化操作**：不是大扫除，是每次会话结束前的必做项
6. **索引即文档**：index.md 本身要有内容，不能是纯链接列表

## 禁止事项

- 禁止将未读文件标记为"已读"而不整理
- 禁止在已有分类下创建重复文件（先搜索再创建）
- 禁止删除有知识价值的文件（即便暂时看不懂）
- 禁止将敏感信息（密钥、账号、凭证）写入知识库
- 禁止把缺少原文跳转链接的内容写成正式知识结论

## 完成门禁

见 [[COMPLETION_GATES]]

## 任务类型

见 [[TASK_ROUTING]]

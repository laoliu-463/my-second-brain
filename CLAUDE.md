# CLAUDE.md

本文件与 `AGENTS.md` 保持同一套知识库维护规范，供 Claude / Hermes / Codex 等代理共享。

> 若两者冲突，以 `AGENTS.md` 为准，并应尽快同步修正本文件。
> 若 `知识库/04-方法论与工具/Hermes/AGENTS.md` 存在更细分规则，以其为同级补充，冲突时仍以 `AGENTS.md` 为准。

## 使用方式

任何接管本知识库的代理，在开始维护前应依次阅读：

1. `AGENTS.md`
2. `index.md`
3. `log.md`

然后根据任务类型进入：

- ingest：先看 `00-收集箱/`、`00-收件箱/`
- query：先看 `index.md` 和相关索引页
- lint：先检查断链、孤立页、frontmatter、页数统计和索引口径

若是 Hermes Agent 首次接管或长时间未维护后重新接管，建议再补一轮：

4. 阅读 `log.md` 最近 10-20 条记录
5. 扫描 `00-收集箱/`、`00-收件箱/`、`知识库/90-来源与映射/`
6. 先判断当前优先专题和待整理入口，再开始正式修改

## 维护原则

- `raw/` 原始资源不可直接修改
- 正式知识沉淀进入 `知识库/`
- 正式知识页的来源完整性优先以页面内 `## 原文链接` 区块为准，链接必须直接指向真实存在的 `raw/sources/...` 原文附件
- `知识库/sources/` 与 `知识库/90-来源与映射/` 只作为辅助索引或批量映射，不替代知识页到 raw 原文的可点击直链
- 任何结构性修改都要同步更新 `index.md` 和 `log.md`
- 来源入口处理完成后，应回填 `status / updated / outputs`
- Hermes Agent 应作为“长期维护代理”工作，而不是只做临时回答

## Claude Code 控制面

Claude Code 在本仓库中应额外遵守项目级控制面：

- 治理文档：`知识库/_meta/agent-governance/KB_PROTOCOL.md`
- 路径边界：`知识库/_meta/agent-governance/PATH_RULES.md`
- 页面 schema：`知识库/_meta/agent-governance/KB_SCHEMA.md`
- 运行时门禁：`.claude/hooks/`
- 通用校验：`tools/kb_validate.ps1 -ChangedOnly`

若 Claude Code 的 hook 或校验脚本与聊天上下文冲突，以脚本阻断结果为准；需要放行时必须由用户明确说明原因。

## 页面最低结构

```markdown
---
title: 页面标题
tags: [标签1, 标签2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [来源1, 来源2]
---

# 页面标题

## 概述

## 原文链接

- [[raw/sources/...|原文附件]]

## 详细内容

## 相关概念
```

## 工作约束

- 不制造无意义测试文件
- 不遗留临时分析产物在根目录
- 不让正式页面脱离索引和日志
- 不在未核对引用关系前删除正式页面
- 规范升级、批量补链、系统性清理后必须更新 `log.md`

## 本地检索工具

- `tools/local_file_index.py` 用于构建本机文件 SQLite/FTS 索引，默认索引库为 `tmp/local-file-index/files.sqlite3`
- 该索引供 Codex / Hermes / Claude 等本机代理共享检索
- 不得自动上传全盘原文到 EverOS；上传前必须由用户确认摘要或文件片段
- 全盘扫描前必须先使用 `--dry-run` 核对范围，并保留默认敏感文件排除规则

## 自动记忆

- `tools/memory_capture.py` 是跨 Agent 统一记忆捕获入口
- Codex 使用官方 lifecycle hooks，从用户级 `~/.codex/hooks.json` 调用 `.codex/hooks/codex-memory-capture.ps1`
- 当前项目的 Codex 自动记忆使用 `UserPromptSubmit` 捕获用户输入、`Stop` 捕获回合结束事件或 transcript
- `tools/agent_memory_wrapper.ps1` 可包装 Codex/Hermes/其他 CLI Agent，退出时自动捕获 transcript 并写入脱敏摘要
- Claude Code Stop hook 应 best-effort 调用该脚本，保存本地 transcript 并向 EverOS Cloud 写入脱敏摘要
- 云端只保存脱敏摘要、关键决策、任务轨迹和认知讨论摘要；完整原文只保存在 `tmp/agent-memory-transcripts/`
- 认知、政治、经济、地缘、博弈、社会趋势等讨论属于必须写入摘要的内容
- Cloud 写入失败不能阻断正常工程工作，但必须保留本地 transcript 和失败状态

## 参考

完整规范见：[[AGENTS]]
模式说明见：[[agent]]

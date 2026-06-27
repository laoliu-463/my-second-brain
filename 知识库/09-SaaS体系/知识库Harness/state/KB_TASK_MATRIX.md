---
title: "Knowledge Base Task Matrix"
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
# Knowledge Base Task Matrix

## 任务卡索引

| 任务 ID | 描述 | 优先级 | 状态 |
|---|---|---|---|
| KB-GC-STUBS | 删除 3 个 0 字节文件 | P0 | 已执行 |
| KB-GC-INBOX | 处理 5 个收件箱/收集箱文件 | P0 | 已执行 |
| KB-GC-ORPHANS-211 | 211 个孤立文件归类 | P1 | 待执行 |
| KB-GC-DUP | 合并/删除 4 对重复文件 | P2 | 待执行 |
| KB-GC-RAW-58 | 58 个 raw/sources 整理 | P1 | 待执行 |
| KB-ORG-ROOT | 移动 9 个 vault 根目录文件 | P2 | 待执行 |
| KB-AUDIT-FULL | 全面 LINT 巡检 | P1 | 已执行 |

## 执行顺序

KB-GC-STUBS → KB-GC-INBOX → KB-AUDIT-FULL → KB-GC-ORPHANS-211 → KB-GC-RAW-58 → KB-GC-DUP → KB-ORG-ROOT

## 下次优先任务

1. KB-GC-ORPHANS-211：收件箱旧清单已降到可复用状态后，继续推进更广泛孤立文件归类。
2. KB-GC-RAW-58：raw/sources 批量归档。
3. KB-GC-DUP：重复内容对齐与去重。

## 延期任务

（暂无）

---
title: "Skill: kb-session-exit"
type: procedure
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
# Skill: kb-session-exit

## 触发条件

每次会话结束前必须执行。

## 步骤

1. 确认本会话修改的文件已记录
2. 确认 0 字节文件已删除
3. 确认收件箱文件已处理或标注
4. 更新 `state/KB_STATUS.md` 当前状态
5. 更新 `state/KB_TASK_MATRIX.md` 下次任务

## 输出模板

```
## 本次会话摘要

- 新建文件：N
- 移动文件：N  
- 删除文件：N
- 更新的 index：N

## 下次优先任务

1. [KB-GC-ORPHANS] 孤立文件归类（剩余 N 个）
2. [KB-GC-RAW] raw/sources/ 整理（剩余 N 个）
3. [KB-GC-DUP] 重复文件合并（N 对）
```

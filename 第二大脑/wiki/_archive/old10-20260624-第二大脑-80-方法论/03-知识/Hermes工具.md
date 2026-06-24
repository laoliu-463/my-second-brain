---
id: kb-method-03-知识-Hermes工具
type: concept
title: 'Hermes工具'
original_title: 'Hermes工具'
aliases: []
status: active
source_id: ''
created: 2026-06-24
updated: 2026-06-24
---

# Hermes工具.md

> Hermes Agent 工具集。源：`知识库/04-方法论与工具/Hermes/` 6 md。

## 1. 核心命令

```bash
hermes config set ...
hermes tools
hermes setup
hermes curator
```

## 2. 关键能力

- 跨平台文件操作
- 浏览器交互
- delegate_task 多 Agent 编排
- Skills 加载 / 卸载
- 记忆持久化

## 3. 常用工具

- terminal / file / search_files
- write_file / patch / read_file
- brain_search / brain_lint
- delegate_task / cronjob

## 4. 第二大脑脚本

- line_guard.py：目录结构校验
- brain_lint.py：索引覆盖
- brain_search.py：跨实例搜索

## 5. 关联

- [[../第二大脑/07-脚本/line_guard.py]]

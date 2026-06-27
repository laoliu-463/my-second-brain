---
source_id: src-20260626-everos-llms-full
original_title: EverOS — Full Reference
title: EverOS 官方 API 参考
aliases:
  - EverOS llms-full
  - EverOS Cloud API Reference
source_type: official-doc
author: EverMind AI
published:
captured: 2026-06-26
canonical_url: https://docs.evermind.ai/llms-full.txt
raw_path: raw/sources/src-20260626-everos-llms-full/llms-full.txt
raw_sha256: 6DC7046698A4605109E87D55467CAA5AA07182DE0173340CCC6597CA406FA3A3
topics:
  - EverOS
  - AI Agent Memory
  - Cloud SDK
tags:
  - source
---

# EverOS 官方 API 参考

## 原文跳转

- [官方文档](https://docs.evermind.ai/llms-full.txt)
- [本地 raw 副本](../../raw/sources/src-20260626-everos-llms-full/llms-full.txt)

## 一句话摘要

该官方参考说明 EverOS 的记忆生命周期、Cloud v1 API、Python SDK、检索方法、群组记忆、agent memory、多模态上传、OSS 部署差异和安全边界。

## 对本项目的影响

- 本项目采用 Cloud SDK：`everos-cloud==0.4.1`。
- API Key 只通过 `EVEROS_API_KEY` 注入，不写入仓库。
- 项目工具入口为 `tools/everos_memory.py`。
- 正式知识库仍以本地 Markdown、来源页和 raw 副本为事实源，EverOS 只做跨会话记忆辅助。

## 证据地图

| 证据位置 | 内容 | 影响页面 |
|---|---|---|
| `llms-full.txt` API Reference | v1 memories add/search/get/flush、filters、error handling | [[知识库/05-智能体与Agent体系/EverOS 记忆层接入方案|EverOS 记忆层接入方案]] |
| `llms-full.txt` Python SDK | `pip install everos-cloud`、`from everos_cloud import EverOS`、同步/异步客户端 | [[知识库/05-智能体与Agent体系/EverOS 记忆层接入方案|EverOS 记忆层接入方案]] |
| `llms-full.txt` Retrieval Methods | `hybrid` 默认推荐，`agentic` 仅用于复杂查询并需要 fallback | [[知识库/05-智能体与Agent体系/EverOS 记忆层接入方案|EverOS 记忆层接入方案]] |
| `llms-full.txt` Open Source Deployment | Cloud 与 OSS API schema 不同，路径和字段不可混用 | [[知识库/05-智能体与Agent体系/EverOS 记忆层接入方案|EverOS 记忆层接入方案]] |

## 待验证项

- 持续维护时确认当前账号 quota 和 dashboard 中的 memory space 是否符合长期需求。
- 后续若要自动写入每次维护轨迹，需要定义哪些内容允许进入 EverOS，哪些内容必须脱敏。

## 影响的知识页

- [[知识库/05-智能体与Agent体系/EverOS 记忆层接入方案|EverOS 记忆层接入方案]]

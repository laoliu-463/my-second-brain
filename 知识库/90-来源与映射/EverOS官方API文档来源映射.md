---
title: EverOS官方API文档来源映射
tags: [EverOS, 来源映射, AI-Agent]
created: 2026-06-26
updated: 2026-06-26
source_id: src-20260626-everos-llms-full
raw_path: raw/sources/src-20260626-everos-llms-full/llms-full.txt
raw_sha256: 6DC7046698A4605109E87D55467CAA5AA07182DE0173340CCC6597CA406FA3A3
canonical_url: https://docs.evermind.ai/llms-full.txt
sources:
  - raw/sources/src-20260626-everos-llms-full/llms-full.txt
  - 知识库/sources/src-20260626-everos-llms-full.md
---

# EverOS官方API文档来源映射

## 来源

| 字段 | 值 |
|---|---|
| source_id | `src-20260626-everos-llms-full` |
| canonical_url | `https://docs.evermind.ai/llms-full.txt` |
| raw_path | `raw/sources/src-20260626-everos-llms-full/llms-full.txt` |
| raw_sha256 | `6DC7046698A4605109E87D55467CAA5AA07182DE0173340CCC6597CA406FA3A3` |
| source_type | 官方 API 参考 |

## 映射关系

| 来源片段 | 本地沉淀 | 说明 |
|---|---|---|
| Core Concepts / Memory Types | [[知识库/05-智能体与Agent体系/EverOS 记忆层接入方案|EverOS 记忆层接入方案]] | 明确 EverOS 作为 agent memory layer 的定位 |
| API Reference (v1) | `tools/everos_memory.py` | 对应 add/search/get/flush 命令 |
| Python SDK | `tools/requirements-everos.txt`、`tools/everos_memory.py` | 使用 `everos-cloud` 和 `everos_cloud.EverOS` |
| Retrieval Methods | [[知识库/05-智能体与Agent体系/EverOS 记忆层接入方案|EverOS 记忆层接入方案]] | 采用 `hybrid` 作为默认检索方式 |
| Open Source Deployment | [[知识库/05-智能体与Agent体系/EverOS 记忆层接入方案|EverOS 记忆层接入方案]] | 记录 Cloud/OSS schema 不可混用 |

## 风险说明

- API Key 不进入本来源映射页。
- 若未来 EverOS Cloud SDK 升级，需要重新核对 SDK 签名和官方文档。
- 若引入自动写入任务，需要补充脱敏规则和失败重试记录。


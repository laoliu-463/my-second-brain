---
title: EverOS本地长期记忆服务来源映射
tags: [EverOS, 来源映射, 本地记忆服务]
created: 2026-06-26
updated: 2026-06-27
source_id: src-20260626-local-everos-oss-memory-service
raw_path: raw/sources/src-20260626-local-everos-oss-memory-service/original.md
raw_sha256: 5407F81FBCE96603C1CE8EFB83C5B5432BAFBDA799AC5CEAF7675CAC61C9266D
canonical_url:
sources:
  - raw/sources/src-20260626-local-everos-oss-memory-service/original.md
  - 知识库/sources/src-20260626-local-everos-oss-memory-service.md
---
# EverOS本地长期记忆服务来源映射

## 来源

| 字段 | 值 |
|---|---|
| source_id | `src-20260626-local-everos-oss-memory-service` |
| raw_path | `raw/sources/src-20260626-local-everos-oss-memory-service/original.md` |
| raw_sha256 | `5407F81FBCE96603C1CE8EFB83C5B5432BAFBDA799AC5CEAF7675CAC61C9266D` |
| source_type | 本地粘贴文本 + 官方 GitHub 文档核验 |

## 映射关系

| 来源片段 | 本地沉淀 | 说明 |
|---|---|---|
| 写入/抽取/检索/注入上下文闭环 | [[知识库/05-智能体与Agent体系/EverOS 本地长期记忆服务方案|EverOS 本地长期记忆服务方案]] | 定义本地长期记忆运行链路 |
| `/api/v1/memory/add` / `flush` / `search` | `tools/everos_local_memory.py` | 新增 OSS 本地 HTTP 桥接脚本 |
| app_id/project_id 分区 | [[知识库/05-智能体与Agent体系/EverOS 本地长期记忆服务方案|EverOS 本地长期记忆服务方案]] | 采用 `second-brain` / `my-second-brain` |
| Markdown + SQLite + LanceDB | [[知识库/05-智能体与Agent体系/EverOS 本地长期记忆服务方案|EverOS 本地长期记忆服务方案]] | 明确本地 source of truth 和索引分层 |
| 默认无鉴权 | `.gitignore` 与安全边界说明 | 记录不得直接暴露到公网/局域网 |

## 待复查项

- 当前本机 `everos 0.4.0` 包不提供 CLI/server，需确认真正的 OSS server 安装路径。
- 安装 server 后执行 `health -> add -> flush -> search` 端到端冒烟。


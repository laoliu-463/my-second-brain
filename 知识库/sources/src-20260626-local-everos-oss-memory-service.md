---
source_id: src-20260626-local-everos-oss-memory-service
original_title: EverOS 当成本地长期记忆服务配合使用
title: EverOS 本地长期记忆服务方案来源
aliases:
  - EverOS 本地长期记忆
  - EverOS OSS 本地服务
source_type: local-pasted-text
author: 本地粘贴文本
published:
captured: 2026-06-26
canonical_url:
raw_path: raw/sources/src-20260626-local-everos-oss-memory-service/original.md
raw_sha256: 5407F81FBCE96603C1CE8EFB83C5B5432BAFBDA799AC5CEAF7675CAC61C9266D
topics:
  - EverOS
  - 本地长期记忆
  - AI Agent
  - 第二大脑
tags:
  - source
---

# EverOS 本地长期记忆服务方案来源

## 原文跳转

- [本地 raw 副本](../../raw/sources/src-20260626-local-everos-oss-memory-service/original.md)

## 一句话摘要

该来源主张把 EverOS OSS 作为本地长期记忆服务：Agent 负责产生对话、任务轨迹和工具调用，EverOS 负责抽取长期记忆、写入 Markdown，并通过 SQLite + LanceDB 支撑检索。

## 核心观点

- 核心闭环是写入、抽取、检索、注入上下文。
- 本地 EverOS OSS 服务使用 `/api/v1/memory/add`、`/api/v1/memory/flush`、`/api/v1/memory/search`。
- `app_id` 和 `project_id` 用于隔离不同应用/项目记忆空间。
- Markdown 是可读、可编辑、可版本化的长期记忆事实源。
- 如果暴露到非 loopback 网络，需要自建网关或认证层。

## 官方文档核验

本次维护已联网核对以下官方 GitHub 文档：

- https://github.com/EverMind-AI/EverOS/blob/main/README.zh-CN.md
- https://github.com/EverMind-AI/EverOS/blob/main/QUICKSTART.md
- https://github.com/EverMind-AI/EverOS/blob/main/docs/api.md
- https://github.com/EverMind-AI/EverOS/blob/main/docs/how-memory-works.md

核验结论：

- 官方文档确认 OSS 本地服务 API 路径为 `/api/v1/memory/*`。
- 官方文档确认默认绑定 `127.0.0.1:8000`，并且服务无内置鉴权。
- 官方文档确认 Markdown 是 source of truth，SQLite 和 LanceDB 是可重建索引。
- 官方文档确认 `/flush` 写入 Markdown 后，检索索引可能存在异步延迟。

## 影响的知识页

- [[知识库/05-智能体与Agent体系/EverOS 本地长期记忆服务方案|EverOS 本地长期记忆服务方案]]


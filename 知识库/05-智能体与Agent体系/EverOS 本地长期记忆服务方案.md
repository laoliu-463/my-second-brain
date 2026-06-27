---
title: EverOS 本地长期记忆服务方案
tags: [EverOS, 本地优先, AI-Agent, Memory, 第二大脑]
created: 2026-06-26
updated: 2026-06-26
source_id: src-20260626-local-everos-oss-memory-service
raw_path: raw/sources/src-20260626-local-everos-oss-memory-service/original.md
raw_sha256: 5407F81FBCE96603C1CE8EFB83C5B5432BAFBDA799AC5CEAF7675CAC61C9266D
canonical_url:
sources:
  - raw/sources/src-20260626-local-everos-oss-memory-service/original.md
  - 知识库/sources/src-20260626-local-everos-oss-memory-service.md
  - https://github.com/EverMind-AI/EverOS/blob/main/README.zh-CN.md
  - https://github.com/EverMind-AI/EverOS/blob/main/QUICKSTART.md
  - https://github.com/EverMind-AI/EverOS/blob/main/docs/api.md
  - https://github.com/EverMind-AI/EverOS/blob/main/docs/how-memory-works.md
---

# EverOS 本地长期记忆服务方案

## 定位

本方案记录 EverOS OSS 本地服务路线：由 Codex、Claude、Hermes 或自建 Agent 产生对话、任务轨迹和工具调用记录，EverOS 本地服务负责抽取长期记忆，并以 Markdown 作为 source of truth，同时维护 SQLite 与 LanceDB 派生索引。

它和当前已接入的 EverOS Cloud 是两套接口：

| 维度 | EverOS Cloud | EverOS OSS 本地服务 |
|---|---|---|
| API 入口 | `https://api.evermind.ai/api/v1/memories/*` | `http://127.0.0.1:8000/api/v1/memory/*` |
| 本项目脚本 | `tools/everos_memory.py` | `tools/everos_local_memory.py` |
| 鉴权 | `EVEROS_API_KEY` Bearer Key | 默认无内置鉴权，依赖 loopback 或外部网关 |
| 数据位置 | EverMind Cloud | 默认 `~/.everos/` |
| 原文事实源 | Cloud 服务 | 本地 Markdown |
| 使用边界 | 跨会话云记忆 | 本地长期记忆服务、可用 Obsidian/Git 查看 |

## 推荐闭环

```text
对话/任务轨迹
  -> /api/v1/memory/add
  -> /api/v1/memory/flush
  -> Markdown + SQLite + LanceDB
  -> /api/v1/memory/search
  -> 注入下一轮 Agent prompt
```

项目落地时建议：

- `app_id = second-brain`
- `project_id = my-second-brain`
- `user_id = my-second-brain-owner`
- `agent_id = codex` / `claude-code` / `hermes`

这样可以把用户长期记忆和 Agent 轨迹隔离，同时避免不同项目串库。

## 本地桥接脚本

本次新增：

```powershell
python tools/everos_local_memory.py --help
```

健康检查：

```powershell
python tools/everos_local_memory.py health --soft
```

确认当前端口确实是 EverOS OSS 记忆 API：

```powershell
python tools/everos_local_memory.py health --require-memory-api
```

写入一条用户记忆：

```powershell
python tools/everos_local_memory.py add --content "我正在搭建第二大脑系统。"
```

写入一条 Agent 轨迹：

```powershell
python tools/everos_local_memory.py add --role assistant --agent-id codex --content "完成了本地文件索引工具验证。"
```

会话结束后强制抽取：

```powershell
python tools/everos_local_memory.py flush
```

检索用户记忆：

```powershell
python tools/everos_local_memory.py search "我在搭建什么系统" --include-profile
```

检索 Agent 记忆：

```powershell
python tools/everos_local_memory.py search "本地文件索引怎么验证" --agent --agent-id codex
```

## 当前环境证据

- 本机 Python 3.12 环境中已存在 `everos 0.4.0` 包。
- `where everos` 未找到 CLI。
- `python -m everos --help` 返回 `No module named everos.__main__`。
- `http://127.0.0.1:8000/health` 当前可访问，但 `/openapi.json` 标题为 `Smart Campus Voice Demo Backend`，且没有 `/api/v1/memory/*` 路由。
- `tools/everos_local_memory.py add` 对当前 8000 服务调用 `/api/v1/memory/add` 返回 404，说明当前端口不是 EverOS OSS memory API。
- 因此当前环境尚不能直接按官方 OSS README 执行 `everos init` / `everos server start`，也不能完成本地 EverOS 端到端写入。
- 本项目已提供 HTTP 桥接脚本，但真实端到端写入需要先安装或取得带 CLI/server 的 EverOS OSS 运行时，并完成模型 API Key 配置，且避免与现有 8000 服务端口冲突。

## 安全边界

- EverOS OSS 官方 API 文档说明默认绑定 `127.0.0.1`，且无内置鉴权；不要直接暴露到局域网或公网。
- `everos.toml`、`ome.toml`、`.everos/`、`tmp/everos-local/` 已加入 `.gitignore`，避免密钥和本地记忆误提交。
- 本地服务与全电脑文件索引仍需分层：`tools/local_file_index.py` 找文件，EverOS 只写入用户确认后的对话、摘要和任务轨迹。
- `/flush` 写入 Markdown 后，索引存在异步延迟；搜索应允许 retry/backoff。

## 待完成

- 安装并验证真正的 EverOS OSS CLI/server 版本。
- 若 8000 端口被其他 FastAPI 服务占用，需改用 EverOS 的 `EVEROS_API__PORT` 或启动参数指定其他端口，并设置 `EVEROS_LOCAL_BASE_URL`。
- 确认本地模型 provider：OpenRouter/DeepInfra、DashScope/百炼，或其他 OpenAI-compatible 服务。
- 启动 `127.0.0.1:8000` 后执行 `health -> add -> flush -> search` 端到端冒烟。
- 为 Codex/Hermes/Claude 增加会话结束时自动调用 `add/flush` 的薄封装。

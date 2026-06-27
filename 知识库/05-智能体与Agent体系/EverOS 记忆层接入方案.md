---
title: EverOS 记忆层接入方案
tags: [EverOS, AI-Agent, Memory, 知识库工具]
created: 2026-06-26
updated: 2026-06-27
source_level: none
source_id: src-20260626-everos-llms-full
raw_path: raw/sources/src-20260626-everos-llms-full/llms-full.txt
raw_sha256: 6DC7046698A4605109E87D55467CAA5AA07182DE0173340CCC6597CA406FA3A3
canonical_url: https://docs.evermind.ai/llms-full.txt
sources:
  - raw/sources/src-20260626-everos-llms-full/llms-full.txt
  - 知识库/sources/src-20260626-everos-llms-full.md
---
# EverOS 记忆层接入方案

## 定位

EverOS 在本知识库中只作为 AI Agent 的外部记忆层，用来保存跨会话维护上下文、任务轨迹、用户偏好和可检索的工作片段。

它不替代本仓库的事实源：

- `raw/` 仍保存原始资料。
- `知识库/` 仍保存正式 wiki 页面。
- `知识库/sources/` 和 `知识库/90-来源与映射/` 仍负责来源追踪。
- EverOS 只保存对话、任务和维护过程中的记忆摘要，不能作为删除、改名、重排正式页面的唯一依据。

## 接入文件

本次接入新增：

- `tools/requirements-everos.txt`：固定当前已验证 SDK 版本 `everos-cloud==0.4.1`。
- `tools/everos_memory.py`：项目级 EverOS Cloud 命令行工具。
- `.gitignore`：忽略 `.env` 和 `.env.*`，避免 API Key 误入版本库。

## 环境变量

官方文档要求使用 Bearer API Key，并明确不应将 key 提交到版本库。本项目只从环境变量读取密钥。

Windows PowerShell 当前会话：

```powershell
$env:EVEROS_API_KEY = "<your-everos-api-key>"
```

macOS / Linux shell：

```bash
export EVEROS_API_KEY="<your-everos-api-key>"
```

可选 scope：

```powershell
$env:EVEROS_USER_ID = "my-second-brain-owner"
$env:EVEROS_SESSION_ID = "my-second-brain"
```

## 常用命令

安装依赖：

```powershell
python -m pip install -r tools/requirements-everos.txt
```

本地自检：

```powershell
python tools/everos_memory.py self-test
```

写入一条维护记忆：

```powershell
python tools/everos_memory.py add --content "完成一次知识库维护：更新了来源页、索引和日志。"
```

写入文件片段：

```powershell
python tools/everos_memory.py add-file log.md --max-chars 12000
```

触发抽取：

```powershell
python tools/everos_memory.py flush
```

检索记忆：

```powershell
python tools/everos_memory.py search "最近一次知识库维护改了什么" --method hybrid --top-k 5
```

查看结构化记忆：

```powershell
python tools/everos_memory.py get --memory-type profile
```

## API 口径

根据官方 `llms-full.txt`：

- Cloud SDK 包名为 `everos-cloud`，Python import 为 `everos_cloud`。
- Cloud API base URL 为 `https://api.evermind.ai`。
- v1 个人记忆写入接口是 `POST /api/v1/memories`。
- 检索接口是 `POST /api/v1/memories/search`。
- 获取结构化记忆接口是 `POST /api/v1/memories/get`。
- flush 接口用于触发边界检测和记忆抽取。
- 搜索默认推荐 `method="hybrid"`，聊天上下文通常 `top_k=5`，研究分析可用 `top_k=10`。
- Cloud 与 OSS API schema 不同，Cloud 使用 `/api/v1/memories/`，OSS 使用 `/api/v1/memory/`，不能混用。

## Cloud 与 OSS 本地服务

本页主要记录 EverOS Cloud 接入。若目标是让记忆全部留在本机，应使用 EverOS OSS 本地服务路线，API 路径是 `/api/v1/memory/add`、`/api/v1/memory/flush`、`/api/v1/memory/search`，并通过 `tools/everos_local_memory.py` 桥接。

详见：[[知识库/05-智能体与Agent体系/EverOS 本地长期记忆服务方案|EverOS 本地长期记忆服务方案]]。

## 边界与风险

- 不把 `EVEROS_API_KEY` 写入 Markdown、脚本、日志或 `.env` 跟踪文件。
- 不把 EverOS 搜索结果当成最终事实；涉及知识库结构修改时仍要回到本地文件、索引和来源页验证。
- 不用 EverOS 替代 `log.md`，每次成批改动仍必须追加 `log.md`。
- 不把个人隐私、第三方密钥、未脱敏客户数据写入记忆。
- `agentic` 检索成本和延迟更高，只在 `hybrid` 不足时使用，并应保留 fallback。

## 与本地全电脑检索的分工

全电脑文件检索由 `tools/local_file_index.py` 负责，索引库保存在 `tmp/local-file-index/files.sqlite3`，供 Codex、Hermes、Claude 等本机代理读取。EverOS 不直接承载全盘原文，只保存用户确认后的维护记忆、摘要和任务轨迹。

详见：[[知识库/04-方法论与工具/实用工具/本地全电脑文件检索方案|本地全电脑文件检索方案]]。

## 当前验证状态

- 已安装并验证 `everos-cloud 0.4.1` 可导入。
- 已通过本地 `self-test`，确认 SDK、默认 `user_id` 和 `session_id` 正常。
- 已用临时进程环境变量完成 Cloud 冒烟：`self-test --live` 可认证，`add --sync` 返回 `Messages accepted`，`flush` 返回 `extracted`，`search --method hybrid` 可检索到测试 episode。
- 未将 API Key 写入仓库文件；当前接入仍要求使用者在自己的 shell 中显式设置 `EVEROS_API_KEY`。

## 最小验收清单

- `python tools/everos_memory.py self-test` 返回 `everos_cloud_installed: true`。
- 设置 `EVEROS_API_KEY` 后，`self-test --live` 能返回一次 live search 结果。（已验证）
- `add --content ...` 返回 EverOS 接收状态。（已验证）
- `flush` 返回 `extracted` 或 `no_extraction`。（已验证）
- `search` 能按 `user_id` 检索到相关记忆。（已验证）
- `git diff` 或文件检查确认没有 API Key 被写入仓库文件。

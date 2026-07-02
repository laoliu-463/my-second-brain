---
title: Raven Agent Harness 使用记录
type: procedure
status: active
created_at: 2026-07-02
updated_at: 2026-07-02
source_level: strong
sources:
  - raw/sources/EverMind-Raven/README.zh-CN.md
  - raw/sources/EverMind-Raven/pyproject.toml
  - raw/sources/EverMind-Raven/install.ps1
raw_evidence:
  - raw/sources/EverMind-Raven/README.zh-CN.md
  - raw/sources/EverMind-Raven/pyproject.toml
  - raw/sources/EverMind-Raven/install.ps1
related:
  - "[[EverOS 记忆层接入方案]]"
  - "[[EverOS 本地长期记忆服务方案]]"
tags:
  - Raven
  - EverMind
  - AI-Agent
  - Agent-Harness
maintainers:
  - codex
confidence: 0.86
---
# Raven Agent Harness 使用记录

## 定位

Raven 是 EverMind-AI/Raven 仓库提供的终端原生 Agent Harness，构建在 EverOS 之上，覆盖 CLI、TUI、provider、channels、sessions、skills、memory、sentinel 和 gateway 等能力。

当前上游 README 标注项目仍处于 pre-alpha，API 和行为可能继续变化。本页只记录 2026-07-02 本机验证结果，不把未验证能力当作已落地事实。

## 原文链接

- [[raw/sources/EverMind-Raven/README.zh-CN.md|Raven 中文 README 快照]]
- [[raw/sources/EverMind-Raven/pyproject.toml|Raven pyproject 依赖与命令入口快照]]
- [[raw/sources/EverMind-Raven/install.ps1|Raven Windows 安装脚本快照]]

## 本机接入结果

- 上游仓库：`https://github.com/EverMind-AI/Raven`
- 本机源码目录：`D:\Docs\Books\my second brain\tmp\Raven`
- 本次源码提交：`d7d14798888b1001e4dda221901e8e02d8de98d5`
- Raven 版本：`0.1.2`
- Python 要求：`>=3.12`
- TUI Node 要求：`>=22`
- 本机 Node：`v24.12.0`，满足 TUI 要求。
- 安装方式：已通过 `uv tool install --force -e "D:\Docs\Books\my second brain\tmp\Raven"` 安装为用户级 `raven` 命令。

## 已验证命令

```powershell
raven --version
raven status
raven provider list
raven plugins
raven channels list
raven skill list
raven sessions list
raven sentinel status
raven cron list
raven tui --check
```

验证结果：

- `raven --version` 返回 `Raven v0.1.2`。
- `raven status` 能识别 `C:\Users\caojianing\.raven\workspace`，但 `config.json` 尚不存在。
- `raven provider list` 可列出 OpenAI、OpenRouter、Anthropic、DeepSeek、Gemini、MiniMax、Ollama、OpenAI Codex OAuth、GitHub Copilot OAuth 等 provider，当前均为 `not set`。
- `raven plugins` 显示内置 `everos-memory` 已激活，active memory backend 为 `everos`。
- `raven channels list` 可列出 Telegram、Slack、Discord、WhatsApp、Matrix、Feishu、WeCom、Mochat、QQ、DingTalk、Email、WeChat 等通道。
- `raven tui --check` 返回 0，非交互终端下输出 `raven-tui: no TTY`。

## TUI 构建记录

源码安装后，`ui-tui/dist/entry.js` 默认不存在。已在 `ui-tui` 目录执行：

```powershell
npm ci
npm run build
```

结果：

- `npm ci` 成功安装 438 个包，`npm audit` 报 1 个 low severity 漏洞，未自动修复，避免修改锁文件。
- `npm run build` 成功生成 `ui-tui/dist/entry.js`。
- `npm run type-check` 通过。
- `npm run lint:rpc` 失败，原因是 `src/rpc/generated.ts` 与 `rpc-schema/openrpc.json` 生成结果不同步；这是上游源码一致性问题，不阻塞基础 CLI/TUI 使用。

## 当前阻塞项

真实 agent 对话还未完成，因为 provider 尚未配置。

已执行：

```powershell
raven agent -m "hello"
```

返回：

```text
Error: No API key configured.
Set one in ~/.raven/config.json under providers section
```

因此当前只能认定：

- Raven 已完成本机安装。
- CLI、TUI smoke、插件、通道、session、skill、sentinel、cron 等只读命令可运行。
- 真实 LLM agent 调用尚未验证。

## 后续使用入口

交互式配置：

```powershell
raven onboard
```

配置完成后诊断：

```powershell
raven doctor
raven provider list
raven provider test <provider-name>
```

一次性任务：

```powershell
raven agent -m "用一句话说明当前目录"
```

进入 TUI：

```powershell
raven
```

## 阶段性结论

截至 2026-07-02，Raven 在本机 Windows PowerShell 环境中已能安装并运行基础 CLI/TUI。当前不能下结论说 Raven 已可执行真实 AI 任务，因为 provider 凭证或 OAuth 登录尚未配置；下一步必须先完成 `raven onboard` 或 `raven provider set ...`，再用 `raven doctor` 和 `raven agent -m ...` 固化真实调用证据。

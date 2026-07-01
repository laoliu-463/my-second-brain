---
title: XianyuAutoAgent MiniMax部署与启动SOP
tags: [XianyuAutoAgent, MiniMax, 闲鱼客服, AI-Agent, 部署]
created: 2026-07-01
updated: 2026-07-01
source_level: mixed
source_id: src-20260701-xianyuautoagent-minimax-deploy
raw_path: raw/sources/src-20260701-xianyuautoagent-minimax-deploy/original.md
canonical_url: https://github.com/shaxiu/XianyuAutoAgent
sources:
  - raw/sources/src-20260701-xianyuautoagent-minimax-deploy/original.md
  - https://github.com/shaxiu/XianyuAutoAgent
  - https://platform.minimax.io/docs/token-plan/intro
  - https://platform.minimax.io/docs/api-reference/text-openai-api
---
# XianyuAutoAgent MiniMax部署与启动SOP

## 定位

本页记录 `shaxiu/XianyuAutoAgent` 在本机使用 MiniMax Token Plan 与闲鱼网页端 Cookie 部署、启动、验证和故障恢复的标准流程。

本页不保存任何 `API_KEY`、Subscription Key、Cookie 或账号凭证。敏感值只允许存在于本地项目 `.env` 文件。

## 当前本机事实

- 项目路径: `D:\Docs\Books\my second brain\tmp\external\XianyuAutoAgent`
- 虚拟环境: `D:\Docs\Books\my second brain\tmp\external\XianyuAutoAgent\.venv`
- 配置文件: `D:\Docs\Books\my second brain\tmp\external\XianyuAutoAgent\.env`
- 启动脚本: `tools/start_xianyu_autoagent.ps1`
- 已验证模型: `MiniMax-M3`
- 已验证 Base URL: `https://api.minimaxi.com/v1`
- 本机证据: 2026-07-01 已完成 token 获取、WebSocket 注册、心跳响应，并由用户确认自动回复成功。

## 标准启动

在知识库根目录执行:

```powershell
powershell -ExecutionPolicy Bypass -File tools/start_xianyu_autoagent.ps1
```

强制重启:

```powershell
powershell -ExecutionPolicy Bypass -File tools/start_xianyu_autoagent.ps1 -Restart
```

脚本会执行以下检查:

- 项目目录不存在时自动克隆 `https://github.com/shaxiu/XianyuAutoAgent.git`
- 创建或复用 Python 虚拟环境
- 安装或补齐 `requirements.txt` 依赖
- 保证 `.env` 中 `MODEL_BASE_URL=https://api.minimaxi.com/v1`
- 保证 `.env` 中 `MODEL_NAME=MiniMax-M3`
- 检查 `API_KEY` 与 `COOKIES_STR` 是否非空，但不输出敏感值
- 调用 MiniMax `/v1/models` 做脱敏连通性检查
- 确保 `XianyuAgent.py` 已过滤 `<think>...</think>`
- 后台启动 `main.py`
- 将日志写入 `tmp/external/XianyuAutoAgent/logs/`

## 首次配置

如果 `.env` 未配置完整，先打开:

```powershell
notepad "D:\Docs\Books\my second brain\tmp\external\XianyuAutoAgent\.env"
```

必要字段:

```env
API_KEY=你的 MiniMax Token Plan Subscription Key
COOKIES_STR=你的闲鱼网页端 Cookie
MODEL_BASE_URL=https://api.minimaxi.com/v1
MODEL_NAME=MiniMax-M3
```

Cookie 获取路径:

- 打开 `https://www.goofish.com`
- 登录闲鱼账号
- 按 `F12`
- 进入 `Network` / `网络`
- 筛选 `Fetch/XHR`
- 刷新页面或打开消息页面
- 点任意请求
- 在 `Request Headers` 中复制 `Cookie:` 后面的完整值
- 只把 Cookie 值填入 `COOKIES_STR`，不要复制 `Cookie:` 这几个字

## 验证清单

启动后按顺序验证:

- 进程存在: `main.py` 对应 Python 进程仍在运行
- 日志无异常退出
- 日志出现 `.env` 加载、提示词加载、SQLite 初始化
- 日志出现闲鱼 token 获取成功
- 日志出现 WebSocket 注册完成
- 日志出现心跳响应
- 用另一个闲鱼账号给商品发消息
- 确认买家端收到自动回复
- 回复内容不包含 `<think>`、`</think>` 或模型推理过程

## 常用命令

查看机器人进程:

```powershell
Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^python(\.exe)?$' -and $_.CommandLine -like '*main.py*' }
```

停止机器人:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.Name -match '^python(\.exe)?$' -and $_.CommandLine -like '*main.py*' } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

查看最新日志:

```powershell
Get-ChildItem "D:\Docs\Books\my second brain\tmp\external\XianyuAutoAgent\logs" -File |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 6 Name, Length, LastWriteTime
```

## 故障排查

### 不自动回复

先确认:

- Python 进程是否还在
- 当前日志是否持续更新
- WebSocket 心跳是否正常
- 是否处于人工接管模式
- 买家消息是否是系统消息或被判定为无需回复

### Cookie 失效

现象:

- 闲鱼 token 获取失败
- WebSocket 重连失败
- 手机或网页端提示重新登录

处理:

- 重新登录闲鱼网页版
- 重新从 Network 请求头复制 Cookie
- 更新 `.env` 的 `COOKIES_STR`
- 执行 `tools/start_xianyu_autoagent.ps1 -Restart`

### MiniMax 401

现象:

- 模型调用返回 `invalid api key`
- `/v1/models` 返回 401

处理:

- 确认 `.env` 中 `API_KEY` 是 Token Plan Subscription Key
- 确认 Token Plan seat 或 Credits 可用
- 本机优先使用 `https://api.minimaxi.com/v1`
- 不要把 pay-as-you-go API Key 与 Token Plan Subscription Key 混用

### 推理内容外发风险

MiniMax M 系列可能返回 `<think>...</think>`。本机已在 `_safe_filter` 中删除该区块。若未来重新克隆项目，必须确认该过滤仍存在，或通过 `tools/start_xianyu_autoagent.ps1` 自动补齐。

## 手机登录影响

手机端正常登录通常不会立刻中断机器人。但以下动作可能导致网页 Cookie 失效:

- 改密码
- 退出所有设备
- 频繁切换账号
- 异常网络环境登录
- 触发风控验证

机器人突然不回复时，优先重新复制网页端 Cookie，再重启。

## 原文链接

- [[raw/sources/src-20260701-xianyuautoagent-minimax-deploy/original.md|XianyuAutoAgent MiniMax Token Plan 本机部署证据快照]]

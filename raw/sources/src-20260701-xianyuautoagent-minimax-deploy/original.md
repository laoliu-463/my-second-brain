---
title: XianyuAutoAgent MiniMax Token Plan 本机部署证据快照
created: 2026-07-01
source_type: local_deployment_evidence
canonical_url: https://github.com/shaxiu/XianyuAutoAgent
redaction: secrets_redacted
---
# XianyuAutoAgent MiniMax Token Plan 本机部署证据快照

## 来源

- GitHub 项目: https://github.com/shaxiu/XianyuAutoAgent
- MiniMax Token Plan: https://platform.minimax.io/docs/token-plan/intro
- MiniMax OpenAI SDK: https://platform.minimax.io/docs/api-reference/text-openai-api

## 本机部署事实

- 部署日期: 2026-07-01
- 本机项目路径: `D:\Docs\Books\my second brain\tmp\external\XianyuAutoAgent`
- Python 虚拟环境: `D:\Docs\Books\my second brain\tmp\external\XianyuAutoAgent\.venv`
- 依赖安装来源: `requirements.txt`
- 配置文件: `.env`
- 敏感配置: `API_KEY` 与 `COOKIES_STR` 已在本地 `.env` 填写，但不得写入知识库、日志、脚本或聊天记录。

## MiniMax 接入证据

- `.env` 中 `MODEL_NAME=MiniMax-M3`
- 官方文档给出的 OpenAI 兼容 URL 是 `https://api.minimax.io/v1`
- 本机 Token Plan Key 实测:
  - `https://api.minimax.io/v1/models` 返回 401
  - `https://api.minimaxi.com/v1/models` 返回 200
- 因此本机部署使用 `MODEL_BASE_URL=https://api.minimaxi.com/v1`
- 模型调用 `chat.completions.create` 实测通过。
- MiniMax 返回内容可能包含 `<think>...</think>`，已在本地 `XianyuAgent.py` 的 `_safe_filter` 中增加过滤，避免推理内容发给闲鱼买家。

## 闲鱼连接证据

- `.env` 中 `COOKIES_STR` 脱敏长度检查通过，长度约 936，形态包含 `=`。
- 启动日志显示 `.env` 加载成功。
- 启动日志显示提示词文件加载成功。
- 启动日志显示 SQLite 对话库初始化成功: `data/chat_history.db`
- 启动日志显示闲鱼 token 获取成功。
- 启动日志显示 WebSocket 注册完成。
- 启动日志显示心跳包持续收到响应。
- 用户在 2026-07-01 确认: 已成功自动回复。

## 运行边界

- 本部署依赖网页端 Cookie，手机端正常登录通常不必然中断，但重新登录、改密码、退出所有设备或触发风控可能导致 Cookie 失效。
- Cookie 失效后，优先重新复制网页端 Cookie，更新 `.env` 后重启。
- Token Plan 额度耗尽或 seat 不可用时，MiniMax 可能返回 401、rate limit 或 insufficient balance。
- 当前知识库只记录部署证据、命令和验证结果，不保存任何密钥或 Cookie。

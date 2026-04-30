---
title: Hermes QQ机器人部署指南
tags: [Hermes, QQ机器人, 部署, DevOps]
created: 2026-04-25
updated: 2026-04-25
sources: [Hermes Agent配置, 实际操作记录]
---

# Hermes QQ机器人部署指南

## 概述

使用 Hermes Agent 的内置 QQ Bot 平台，通过 WebSocket 方式连接 QQ 官方机器人网关，实现消息收发。

## 环境信息

- **系统**：WSL (Windows Subsystem for Linux)
- **Gateway 进程管理器**：Hermes CLI
- **Python 版本**：CPython 3.11.15
- **连接方式**：WebSocket（wss://api.sgroup.qq.com/websocket）
- **认证方式**：App ID + Client Secret → Access Token

## 配置文件位置

```
~/.hermes/
├── config.yaml          # 平台配置（app_id, client_secret 等）
├── gateway.pid          # 当前 Gateway PID
├── pairing/
│   ├── qqbot-pending.json   # 待审批用户
│   └── qqbot-approved.json  # 已授权用户
└── logs/
    ├── agent.log        # 主日志（包含 QQ Bot 日志）
    ├── errors.log       # 错误日志
    └── gateway.log      # Gateway 启动日志
```

## 核心配置（config.yaml）

```yaml
qqbot:
  enabled: true
  extra:
    app_id: '1903862650'
    client_secret: aOD3tkbTLE71wrnjgdbZYXXYZbdgjnrw
    markdown_support: true
```

## 常见启动错误及解决

### 1. Gateway 已运行（PID 冲突）

```
❌ Gateway already running (PID 5736).
   Use 'hermes gateway restart' to replace it,
   or 'hermes gateway stop' to kill it first.
   Or use 'hermes gateway run --replace' to auto-replace.
```

**解决**：使用 `--replace` 参数，或先 `kill` 旧进程

### 2. App ID 或 Secret 无效

```
RuntimeError: QQ Bot token response missing access_token:
  {'code': 100016, 'message': 'invalid appid or secret'}
```

**解决**：检查 `config.yaml` 中的 `app_id` 和 `client_secret` 是否正确

### 3. Session 超时（4009）

```
WARNING [QQBot] WebSocket closed: code=4009 reason=Session timed out
```

**解决**：自动重连机制会处理，若持续出现需检查网络

### 4. Gateway URL 获取失败（500 错误）

```
WARNING [QQBot] Reconnect failed: Failed to get QQ Bot gateway URL:
  Server error '500 Internal Server Error'
```

**解决**：QQ 服务器临时问题，等待重试

## 启停命令

### 启动

```bash
cd /home/caojianing
hermes gateway run --replace
```

### 停止

```bash
hermes gateway stop
# 或手动 kill
kill $(cat ~/.hermes/gateway.pid | python3 -c "import sys,json; print(json.load(sys.stdin)['pid'])")
```

### 重启

```bash
hermes gateway restart
```

## 日志查看

```bash
# 查看 QQ Bot 最新日志
grep -i "qqbot\|QQBot" ~/.hermes/logs/agent.log | tail -20

# 查看 Gateway 启动日志
tail -20 ~/.hermes/logs/gateway.log

# 查看错误日志
tail -30 ~/.hermes/logs/errors.log
```

## 部署检查步骤

1. **确认进程运行**
   ```bash
   ls -la /proc/$(cat ~/.hermes/gateway.pid | python3 -c "import sys,json; print(json.load(sys.stdin)['pid'])")/exe
   ```

2. **确认 QQ Bot 连接**（日志中查找）
   ```
   INFO [QQBot] Connected
   INFO [QQBot] Ready, session_id=xxx
   INFO gateway.run: ✓ qqbot connected
   ```

3. **确认网络连接**
   ```bash
   ss -tnp | grep $(cat ~/.hermes/gateway.pid | python3 -c "import sys,json; print(json.load(sys.stdin)['pid'])")
   ```

## 相关概念

- [[agent]] - LLM Wiki 模式说明

## 操作记录

| 日期 | 操作 | 结果 |
|------|------|------|
| 2026-04-19 | 首次配置部署 | 成功连接，后因 I/O 错误断开 |
| 2026-04-25 11:52 | 首次启动 Gateway | Token 刷新成功，QQ Bot Connected |
| 2026-04-25 12:57 | Session 超时断开 | 自动重连失败 |
| 2026-04-25 15:38 | 重启 Gateway | QQ Bot Ready ✓ |

---
kb_id: tools/05-powershell-qa
title: PowerShell 验收脚本
domain: tools
category: qa
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/验收/
  - harness/scripts/
related_reports: []
forbidden_misread:
  - 不得在 PowerShell 脚本中硬编码 token / password
  - 不得用 mock 数据写"real-pre 验收"输出
---

# PowerShell 验收脚本

## 1. 主源

- `docs/验收/*.ps1`
- `harness/scripts/`

## 2. 常用脚本

| 脚本 | 用途 |
| --- | --- |
| `real-pre-preflight.ps1` | real-pre 预检 |
| `p0-evidence-bundle.ps1` | P0 证据打包 |
| `domain-status-snapshot.ps1` | DOMAIN_STATUS 快照 |
| `session-exit-report.ps1` | 退出报告生成 |

## 3. 调用方式

```powershell
# 预检
pwsh -File docs/验收/real-pre-preflight.ps1

# 证据打包
pwsh -File harness/scripts/p0-evidence-bundle.ps1 -TaskId HARNESS-KB-001
```

## 4. 已知坑

- 路径分隔符 Windows `\` 与 bash `/` 必须用环境兼容写法
- `$env:VAR` 读取敏感变量，输出必须脱敏
- 错误码非 0 必须登记

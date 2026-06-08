---
kb_id: evidence/05-screenshots
title: 截图与可视化证据
domain: evidence
category: evidence-screenshots
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/evidence/screenshots/
  - frontend/tests/e2e/screenshots/
related_reports: []
forbidden_misread:
  - 截图时间戳必须保留
  - 不得用 mock 数据截图当成 real-pre
---

# 截图与可视化证据

## 1. 用途

保存界面渲染、看板、E2E 流程、容器状态的截图证据。

## 2. 截图分类

| 类型 | 路径 | 来源 |
| --- | --- | --- |
| 看板 | harness/evidence/screenshots/dashboard/*.png | 人工 / Playwright |
| E2E | frontend/tests/e2e/screenshots/*.png | Playwright |
| 容器 | harness/evidence/screenshots/containers/*.png | 人工 |
| 接口 | harness/evidence/screenshots/api/*.png | Postman / curl 终端 |

## 3. 验收口径

- 截图必须含时间戳（系统托盘 / 水印 / 元数据）
- 与 last_verified_at 一致
- 截图说明文件：同目录同名 .md

## 4. 治理

- 截图内容如有客户数据 / 真实订单号需脱敏
- 截图大小 ≤ 5MB
- 禁止用 mock 数据截图当成 real-pre 闭环证据

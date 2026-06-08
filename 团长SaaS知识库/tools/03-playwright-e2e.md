---
kb_id: tools/03-playwright-e2e
title: Playwright E2E 工具链
domain: tools
category: e2e
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - package.json
  - e2e/playwright.config.ts
related_reports: []
forbidden_misread:
  - 不得把 `--headed` 用于 CI
  - 不得把 mock 数据的 E2E 结果当成 real-pre 证据
---

# Playwright E2E 工具链

## 1. 主源

- `package.json` 顶层 scripts
- `e2e/playwright.config.ts`

## 2. 关键命令

```bash
# V1-P0 mock 基线
npm run e2e:v1-p0

# real-pre 预检
npm run e2e:real-pre:p0:preflight

# real-pre 全量
npm run e2e:real-pre:p0

# 调试（仅本机）
npx playwright test --headed --debug
```

## 3. 输出物

- HTML 报告：`e2e/playwright-report/`
- Trace：`e2e/test-results/`
- 截图：嵌入 HTML 报告

## 4. 已知坑

- `real-pre` 测试要绑定 127.0.0.1
- 缺真实样本时，测试结果不构成 PASS
- `mock` 与 `real-pre` 的 fixtures 不可混用

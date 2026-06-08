---
kb_id: tools/02-frontend-npm
title: 前端 npm 工具链
domain: tools
category: frontend
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - frontend/package.json
  - frontend/vite.config.ts
  - frontend/tsconfig.json
related_reports: []
forbidden_misread:
  - 不得擅自升级 Vite / Vue 3 / Naive UI
  - 不得把 `npm install` 改为全局
---

# 前端 npm 工具链

## 1. 主源

- `frontend/package.json`（Vue 3 + Vite + Pinia + Naive UI + TypeScript）

## 2. 关键依赖

| 依赖 | 版本 | 用途 |
| --- | --- | --- |
| vue | 3.4+ | 框架 |
| vite | 5.x | 构建 |
| typescript | 5.x | 类型 |
| pinia | 2.x | 状态 |
| naive-ui | 2.38+ | 组件库 |
| vue-router | 4.x | 路由 |
| @vueuse/core | 10.x | 工具集 |

## 3. 常用命令

```bash
# 安装
npm install

# 开发
npm run dev

# 构建
npm run build

# 类型检查
npm run type-check

# 单测（Vitest）
npm run test:unit

# 覆盖率
npm run test:unit -- --coverage
```

## 4. 已知坑

- Vite 5 在 Node 18 上需要 `--openssl-legacy-provider`
- Naive UI 的全局 provider 必须在 `App.vue` 包裹
- Pinia devtools 仅在 dev 模式生效

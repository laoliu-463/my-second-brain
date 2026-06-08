---
kb_id: environment/02-test-mock
title: test/mock 环境
domain: environment
category: env-test
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docker-compose.yml
  - backend/src/main/resources/application-test.yml
  - frontend/vitest.config.ts
related_reports: []
forbidden_misread:
  - 不得把 mock 数据当作 real-pre 真实闭环
  - 不得用 mock 样本驱动 "PASS" 验收
---

# test/mock 环境

## 1. 适用场景

- 单测基线 `npm run e2e:v1-p0`
- 集成测试
- CI 回归

## 2. 启动方式

```bash
# 容器全栈
docker compose up -d

# 单元测试
cd backend && mvn test
cd frontend && npm run test:unit
```

## 3. mock 边界

- 所有外部 API 调用走 `MockXxxClient`
- 订单表 / 业绩表可能为空（mock fixture）
- 不得用空表写"已通过"

## 4. 与 real-pre 的差异

| 维度 | test/mock | real-pre |
| --- | --- | --- |
| 抖音开放平台 | mock | 真实 |
| Token | fake | 真实 |
| 数据持久 | 可选 | 必须 |
| E2E 入口 | e2e:v1-p0 | e2e:real-pre:p0 |

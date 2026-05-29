---
title: ADR-006 real-pre作为上线前联调环境
tags: [ADR, 架构决策, real-pre, 测试环境, 抖音团长]
created: 2026-05-29
updated: 2026-05-29
sources:
  - D:/Projects/SAAS/docs/决策/ADR-006-real-pre作为上线前联调环境.md
---

# ADR-006 real-pre作为上线前联调环境

## 状态

**已采纳**

## 背景

- test/mock 能证明本地业务闭环，但不能证明第三方真实接口可用
- real-pre 用于上线前真实 Token、真实接口、真实数据路径联调

## 决策

- real-pre 是上线前联调环境
- real-pre 必须关闭 mock：`APP_TEST_ENABLED=false`、`DOUYIN_TEST_ENABLED=false`
- real-pre 的 PASS 必须有真实接口响应、系统入库和日志证据
- 缺 Token、权限包、真实样本或限流导致失败时，标记 BLOCKED 并保留证据

## 影响

- real-pre 不能用 test/mock 数据冒充通过
- 验收报告必须区分 PASS、PASS_NEEDS_CLEANUP、BLOCKED、PENDING、FAIL
- profile 名称存在旧口径差异时，以实际 `.env.real-pre`、compose 和启动日志为准

## 验证方式

- 运行 `npm run e2e:real-pre:p0:preflight`
- 运行 `npm run e2e:real-pre:p0` 或记录阻塞原因
- 证据登记到验收证据索引

## 相关概念

- [[DDD实战-团长SaaS系统/48-部署运行总览|部署运行总览]]
- [[DDD实战-团长SaaS系统/47-测试验收总览|测试验收总览]]
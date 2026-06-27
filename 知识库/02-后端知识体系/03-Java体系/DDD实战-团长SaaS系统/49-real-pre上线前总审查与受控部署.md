---
title: real-pre上线前总审查与受控部署
tags: [DDD, SaaS, real-pre, 部署, 验收, release, 抖音团长]
created: 2026-05-29
updated: 2026-06-27
source_level: none
sources:
  - D:/Projects/SAAS/docs/release/README.md
  - D:/Projects/SAAS/docs/release/real-pre上线总审查报告-20260528-171543.md
  - D:/Projects/SAAS/docs/10-部署运行总览.md
  - D:/Projects/SAAS/docker-compose.real-pre.yml
  - D:/Projects/SAAS/.env.real-pre.example
---
# real-pre上线前总审查与受控部署

## 概述

2026-05-28 的 release 审查结论是：当前项目达到 **real-pre 受控部署** 条件，但没有达到“正式生产全量上线”或“real-pre P0 全量 PASS”。这个页面用于固定审查口径，避免把 `PASS`、`PENDING`、`BLOCKED` 混写成一个笼统的“已上线”结论。

## 审查目标

| 项目 | 口径 |
| --- | --- |
| 审查时间 | 2026-05-28 17:15:43，Asia/Shanghai |
| 审查目标 | real-pre 受控部署、真实接口联调准备、P0 门禁可验证 |
| 明确不是 | 正式生产全量上线 |
| 审查 commit | `63d7bab58699ffd8f97818333c96ac7753b36743` |
| 审查分支 | `feature/auth-system` |

## 已达到的门禁

| 门禁 | 报告记录结果 | 说明 |
| --- | --- | --- |
| 后端测试 | PASS | release 报告记录 `Tests run: 1617, Failures: 0, Errors: 0, Skipped: 0` |
| 后端打包 | PASS | 生成 `backend/target/colonel-saas.jar`，插件 warning 不阻塞 |
| 前端依赖安装 | PASS | `npm ci` 成功，0 vulnerabilities |
| 前端测试 | PASS | 55 个测试文件，219 个测试通过 |
| 前端构建 | PASS | 构建成功，存在 Vite chunk size warning |
| 前端依赖审计 | PASS | 0 vulnerabilities |
| Compose 静态检查 | PASS | `docker compose --env-file .env.real-pre.example -f docker-compose.real-pre.yml config` 可解析 |
| PostgreSQL / Redis 公网暴露 | PASS | Compose 未发布公网 `5432` / `6379` |
| healthcheck / volume | PASS | 四个服务有 healthcheck，PostgreSQL / Redis 使用命名卷 |

以上是 release 报告中的历史审查记录；本次知识库整理没有重新运行这些命令。

## 未达到或受阻项

| 项目 | 状态 | 原因 |
| --- | --- | --- |
| 真实上游调用 | BLOCKED | `BLOCKED_BY_SECRET_NOT_CONFIGURED` |
| OAuth 真实授权跳转验证 | BLOCKED | 需要服务器域名、SSL、真实百应应用和回调白名单 |
| token / 权限 / 白名单 / 角色不足日志样本 | PENDING | 本地缺少真实凭据与第三方错误样本 |
| real-pre P0 全链路 PASS | 未达到 | 真实订单样本、归因、寄样和业绩证据仍需补齐 |
| 正式生产全量上线 | 未达到 | real-pre 只是受控部署与真实样本采集入口 |

## real-pre 不变量

| 配置 / 规则 | 口径 |
| --- | --- |
| `APP_TEST_ENABLED=false` | real-pre 关闭应用层 mock |
| `DOUYIN_TEST_ENABLED=false` | real-pre 关闭抖店 mock |
| `DOUYIN_REAL_UPSTREAM_MODE=live` | 切到真实上游 |
| `DOUYIN_REAL_PROMOTION_WRITE_ENABLED=false` | 真实推广写入默认关闭 |
| `ALLOW_REAL_PROMOTION_WRITE=false` | 双开关控制，人工批准窗口才允许开启 |
| `.env.real-pre` | 不得提交，不得写入真实 Token、数据库密码、Redis 密码、JWT_SECRET、CLIENT_SECRET |
| PostgreSQL / Redis | 不应公网开放 |

## 受控部署后的验证路径

1. 执行 real-pre preflight：`npm run e2e:real-pre:p0:preflight`
2. 执行 real-pre P0：`npm run e2e:real-pre:p0`
3. 执行角色权限回归：`npm run e2e:real-pre:roles`
4. 归档 Compose 状态、服务日志、`runtime/qa/out/**`、`playwright-report/**`、`test-results/playwright/**`
5. 对真实订单、归因、寄样、业绩闭环补 API / SQL / 日志证据

## 结论边界

- 可以说：项目具备 real-pre 受控部署入口，具备继续真实样本采集和联调的工程条件。
- 不能说：项目已经正式生产上线。
- 不能说：real-pre P0 已全量通过，除非真实 Token、真实上游响应、真实订单样本、归因、寄样和业绩证据全部补齐。
- `PENDING` / `BLOCKED` 必须保留原状态，不能为了总结好看改写成 `PASS`。

## 相关概念

- [[DDD实战-团长SaaS系统/48-部署运行总览]]
- [[DDD实战-团长SaaS系统/47-测试验收总览]]
- [[DDD实战-团长SaaS系统/31-测试验收与QA图谱脉络]]
- [[抖店团长SaaS-技术体系/07-部署运行|部署运行]]
- [[知识库/90-来源与映射/抖音团长SaaS当前项目来源映射|抖音团长SaaS当前项目来源映射]]

---
title: 抖音授权与Token
tags: [DDS, SaaS, 抖音, OAuth, Token, 鉴权, 抖店团长]
created: 2026-05-29
updated: 2026-05-29
sources:
  - D:/Projects/SAAS/docs/对接/抖音授权与Token.md
---

# 抖音授权与Token

## 概述

支撑 real-pre 环境获取、刷新和校验抖音/抖店访问 Token，为活动商品、转链、订单、物流、达人等接口提供统一鉴权输入。

## 核心事实

- Token 由后端 Gateway/SDK 管理，前端不得直接持有第三方密钥
- real-pre 必须关闭 mock：`APP_TEST_ENABLED=false`、`DOUYIN_TEST_ENABLED=false`
- Token 获取失败时必须记录请求时间、环境、错误码和响应摘要
- V1 不要求完整多租户 Token 池，但必须能支撑当前联调账号

## API/配置

| 项 | 证据 |
| --- | --- |
| 授权码换 Token | real-pre 请求/响应、后端日志 |
| Token 刷新 | 后端日志、配置或 Token 状态 |
| 权限包校验 | 第三方错误码、接口响应 |
| Token 过期处理 | 错误日志、重试或刷新记录 |

## 验收证据

- `npm run e2e:real-pre:p0:preflight` 能证明 real-pre 环境和 Token 基础配置
- Token 相关证据写入验收证据索引
- 缺权限或授权码过期时标记 BLOCKED，不写成业务通过

## 明确不做

- 不在前端或文档中暴露真实 secret
- 不用 mock Token 冒充 real-pre

## 相关概念

- [[DDD实战-团长SaaS系统/45-第三方对接总览|第三方对接总览]]
- [[DDD实战-团长SaaS系统/48-部署运行总览|部署运行总览]]
---
title: 抖音授权与Token
tags: [抖店团长, 抖音, OAuth, Token, 技术]
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

## API/配置

| 项 | 证据 |
| --- | --- |
| 授权码换 Token | real-pre 请求/响应、后端日志 |
| Token 刷新 | 后端日志、配置或 Token 状态 |
| 权限包校验 | 第三方错误码、接口响应 |

## 相关概念

- [[抖店团长SaaS-技术体系/index|技术体系索引]]
- [[抖店团长SaaS-技术体系/07-部署运行|部署运行]]
- [[抖店团长SaaS-技术体系/08-ADR/ADR-006|ADR-006 real-pre上线前联调]]
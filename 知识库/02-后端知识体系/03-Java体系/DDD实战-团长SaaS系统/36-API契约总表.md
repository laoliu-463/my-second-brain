---
title: API 契约总表
tags: [DDD, SaaS, API契约, REST, 抖音团长]
created: 2026-05-29
updated: 2026-05-29
sources:
  - D:/Projects/SAAS/docs/05-API契约总表.md
---

# API 契约总表

## 概述

前端只调用内部 API，不直接调用抖音/抖店开放接口。后端通过 Gateway/SDK 封装第三方接口、鉴权、参数转换、签名、错误码适配和响应标准化。

## 内部 API 总表

| 领域 | API 分组/典型路径 | 用途 | 验收证据 |
| --- | --- | --- | --- |
| 认证 | `/api/auth/login`、`/api/auth/me`、`/api/auth/logout` | 登录、当前用户、退出 | E2E 登录、Network 响应 |
| 用户 | `/api/users/**`、`/api/roles/**`、`/api/menus/**` | 用户、角色、菜单、数据范围 | 权限测试、API 响应 |
| 配置 | `/api/configs/**`、`/api/commission-rules/**`、`/api/rule-center/**` | 配置、佣金规则、规则中心 | 配置变更日志、规则 API |
| 商品 | `/api/products/**`、`/api/colonel/products/**` | 商品库、活动商品、筛选、转链 | 商品表、转链记录 |
| 活动 | `/api/activities/**`、`/api/colonel/activities/**` | 活动商品同步、活动查询 | 同步日志、API 响应 |
| 达人 | `/api/talents/**`、`/api/colonel/talents/**` | 达人资料、标签、地址、跟进 | 达人表、操作日志 |
| 寄样 | `/api/samples/**`、`/api/sample-applications/**` | 寄样申请、审批、发货、状态 | 寄样状态日志、E2E |
| 订单 | `/api/orders/**`、`/api/order-sync/**` | 订单同步、订单事实、退款事实 | 订单表、同步日志 |
| 业绩 | `/api/performance/**`、`/api/commission/**` | 归属、提成、冲正、汇总 | 业绩明细、汇总 API |
| 分析 | `/api/dashboard/**`、`/api/analytics/**`、`/api/reports/**` | dashboard、只读汇总、导出 | 看板 API、导出文件 |
| 运维 | `/api/operations/**`、`/actuator/**` | 操作日志、健康检查 | 健康检查、操作审计 |
| 抖音授权 | `/api/douyin/auth/**`、`/api/douyin/token/**` | 授权、Token、刷新 | real-pre Token 证据 |
| 抖音物流 | `/api/douyin/logistics/**` | 物流接口适配 | real-pre 响应或阻塞证据 |
| 主数据 | `/api/master-data/**`、`/api/current-user/**` | 前端下拉、当前用户上下文 | Network 响应 |

## 第三方 API 入口

| 对接项 | 文档入口 | 关键事实 |
| --- | --- | --- |
| 抖音授权与 Token | [[DDD实战-团长SaaS系统/44b-抖音授权与Token|抖音授权与Token]] | 授权码、Token 获取、刷新、过期处理 |
| 活动商品同步 | [[DDD实战-团长SaaS系统/44c-活动商品同步|活动商品同步]] | 活动商品、商品库同步 |
| 转链与归因 | [[DDD实战-团长SaaS系统/44a-转链与pick_source归因|转链与pick_source归因]] | `buyin.instPickSourceConvert`、`pick_source_mapping` |
| 订单同步 | [[DDD实战-团长SaaS系统/44d-订单同步|订单同步]] | 抖店订单、退款、归因输入 |
| 物流接口 | [[DDD实战-团长SaaS系统/44e-物流接口|物流接口]] | 发货、物流查询、阻塞证据 |
| 达人信息获取 | [[DDD实战-团长SaaS系统/44f-达人信息获取|达人信息获取]] | 达人资料、权限包限制 |

## 明确不做

- 不让前端直接调用第三方开放接口
- 不把旧 OpenAPI 缓存当作最终事实；字段级契约需由代码、OpenAPI 或真实响应证明

## 相关概念

- [[DDD实战-团长SaaS系统/28-后端代码结构索引|后端代码结构索引]]
- [[DDD实战-团长SaaS系统/29-前端代码结构索引|前端代码结构索引]]
- [[DDD实战-团长SaaS系统/30-前后端映射对照|前后端映射对照]]
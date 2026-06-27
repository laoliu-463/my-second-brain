---
title: API契约
tags: [抖店团长, API, REST, 技术]
created: 2026-05-29
updated: 2026-06-27
source_level: none
sources:
  - D:/Projects/SAAS/docs/05-API契约总表.md
---
# API契约

## 概述

前端只调用内部 API，不直接调用抖音/抖店开放接口。后端通过 Gateway/SDK 封装第三方接口。

## 内部 API 总表

| 领域 | API 路径 | 用途 |
| --- | --- | --- |
| 认证 | `/api/auth/login`、`/api/auth/me`、`/api/auth/logout` | 登录、当前用户、退出 |
| 用户 | `/api/users/**`、`/api/roles/**`、`/api/menus/**` | 用户、角色、菜单、数据范围 |
| 配置 | `/api/configs/**`、`/api/commission-rules/**`、`/api/rule-center/**` | 配置、佣金规则、规则中心 |
| 商品 | `/api/products/**`、`/api/colonel/products/**` | 商品库、活动商品、筛选、转链 |
| 活动 | `/api/activities/**`、`/api/colonel/activities/**` | 活动商品同步、活动查询 |
| 达人 | `/api/talents/**`、`/api/colonel/talents/**` | 达人资料、标签、地址、跟进 |
| 寄样 | `/api/samples/**`、`/api/sample-applications/**` | 寄样申请、审批、发货、状态 |
| 订单 | `/api/orders/**`、`/api/order-sync/**` | 订单同步、订单事实、退款 |
| 业绩 | `/api/performance/**`、`/api/commission/**` | 归属、提成、冲正、汇总 |
| 分析 | `/api/dashboard/**`、`/api/analytics/**`、`/api/reports/**` | dashboard、只读汇总、导出 |
| 抖音对接 | `/api/douyin/auth/**`、`/api/douyin/token/**` | 授权、Token、刷新 |
| 抖音对接 | `/api/douyin/logistics/**` | 物流接口适配 |

## 第三方 API 入口

| 对接项 | 详情入口 |
| --- | --- |
| 抖音授权与 Token | [[抖店团长SaaS-技术体系/05-抖音授权与Token]] |
| 活动商品同步 | [[抖店团长SaaS-技术体系/05-活动商品同步]] |
| 转链与归因 | [[抖店团长SaaS-技术体系/05-转链与pick_source归因]] |
| 订单同步 | [[抖店团长SaaS-技术体系/05-订单同步]] |
| 物流接口 | [[抖店团长SaaS-技术体系/05-物流接口]] |
| 达人信息获取 | [[抖店团长SaaS-技术体系/05-达人信息获取]] |

## 相关概念

- [[抖店团长SaaS-技术体系/index|技术体系索引]]
- [[抖店团长SaaS-技术体系/02-前后端映射|前后端映射]]
---
title: 转链与pick_source归因
tags: [DDD, SaaS, 抖店, 转链, pick_source, 归因, 抖音团长]
created: 2026-05-29
updated: 2026-05-29
sources:
  - D:/Projects/SAAS/docs/对接/转链与pick_source归因.md
---

# 转链与pick_source归因

## 概述

商品域调用抖音转链接口，生成可推广链接并落 `pick_source_mapping`。`pick_source_mapping` 是订单归因链路的事实输入。

## 核心事实

- 转链能力属于商品域
- 订单域消费 `pick_source` 等输入，但不做最终提成
- 业绩域根据映射、订单事实和配置计算最终归属
- real-pre 真实转链写操作受双开关控制：
  - `DOUYIN_REAL_PROMOTION_WRITE_ENABLED`（后端 `douyin.real.promotion-write-enabled`）
  - `ALLOW_REAL_PROMOTION_WRITE`（后端 `douyin.real.allow-promotion-write`）
  - 默认均为 `false`，商品库复制简介需携带推广链接时必须在人工批准窗口同时开启

## 数据流

1. 用户在内部商品页面触发转链
2. 后端 Gateway 调用转链接口（如 `buyin.instPickSourceConvert`）
3. 商品域保存第三方响应摘要和 `pick_source_mapping`
4. 订单同步时订单域保存 `pick_source` 等归因输入
5. 业绩域完成最终归属和提成计算

## 验收证据

- 转链接口请求/响应摘要
- `pick_source_mapping` SQL/API 记录
- 至少一笔订单能从 `pick_source` 追溯到映射和业绩明细
- 后端日志需留存 `promotion_convert_result=success|failed`，包含 `product_id`、`channel_id`、`pick_source` 和调用结果

## 明确不做

- 不在商品域计算提成
- 不在订单域应用独家覆盖

## 相关概念

- [[DDD实战-团长SaaS系统/41-订单归因链路|订单归因链路]]
- [[DDD实战-团长SaaS系统/34c-商品域合同|商品域]]
- [[DDD实战-团长SaaS系统/34f-订单域合同|订单域]]
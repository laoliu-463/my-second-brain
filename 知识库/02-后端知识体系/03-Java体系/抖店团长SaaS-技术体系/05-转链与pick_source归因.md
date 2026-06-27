---
title: 转链与pick_source归因
tags: [抖店团长, 转链, pick_source, 归因, 技术]
created: 2026-05-29
updated: 2026-06-27
source_level: none
sources:
  - D:/Projects/SAAS/docs/对接/转链与pick_source归因.md
---
# 转链与pick_source归因

## 概述

商品域调用抖音转链接口，生成可推广链接并落 `pick_source_mapping`。`pick_source_mapping` 是订单归因链路的事实输入。

## 核心事实

- 转链能力属于商品域
- 订单域消费 `pick_source` 等输入，但不做最终提成
- real-pre 真实转链写操作受双开关控制：
  - `DOUYIN_REAL_PROMOTION_WRITE_ENABLED`（后端 `douyin.real.promotion-write-enabled`）
  - `ALLOW_REAL_PROMOTION_WRITE`（后端 `douyin.real.allow-promotion-write`）
  - 默认均为 `false`

## 数据流

1. 用户触发转链 → Gateway 调用 `buyin.instPickSourceConvert`
2. 商品域保存 `pick_source_mapping`
3. 订单同步时订单域保存 `pick_source` 等归因输入
4. 业绩域完成最终归属和提成计算

## 相关概念

- [[抖店团长SaaS-技术体系/index|技术体系索引]]
- [[抖店团长SaaS-业务体系/03-订单归因链路|订单归因链路]]
- [[抖店团长SaaS-业务体系/04-七领域合同/商品域|商品域]]
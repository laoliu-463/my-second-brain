---
source_id: src-20260430-akkkk-douyin-comments-cleaned
original_title: creator_comments_cleaned.csv
title: Akkkk 抖音评论数据集
aliases:
  - creator_comments_cleaned.csv
source_type: dataset
author: 本地采集
published:
captured: 2026-04-30
canonical_url:
original_path: creator_comments_cleaned.csv
topics:
  - Akkkk
  - 评论数据
tags:
  - source
  - dataset
---

# Akkkk 抖音评论数据集

## 原文跳转

- [[creator_comments_cleaned.csv|原文]]

## 一句话摘要
该 CSV 是 Akkkk 评论样本数据集，包含评论 ID、视频 ID、评论内容、点赞数、评论层级和部分用户标识字段。

## 数据用途

- 支撑评论区画像、受众关切、主题共鸣和内容反馈分析。
- 只适合聚合分析，不应在知识页复制个人标识。

## 证据地图

| 证据位置 | 内容 | 影响页面 |
|---|---|---|
| CSV 表头 | `comment_id`、`aweme_id`、`content`、`like_count` | [[知识库/90-来源与映射/Akkkk抖音数据集来源映射|Akkkk抖音数据集来源映射]] |
| 全量记录 | 评论样本 | [[知识库/06-内容创作与传播/Akkkk内容研究/抖音创作者Akkkk评论区画像|抖音创作者Akkkk评论区画像]] |
| `aweme_id` | 与内容表关联 | [[知识库/06-内容创作与传播/Akkkk内容研究/index|Akkkk内容研究]] |

## 个人批注

- 评论数据含个人标识和头像链接，正式知识页只保留主题和聚合画像。
- 不创建评论用户实体页。

## 待验证项

- 是否迁入 `raw/sources/` 需先处理脚本路径和敏感字段治理。

## 影响的知识页

- [[知识库/90-来源与映射/Akkkk抖音数据集来源映射]]
- [[知识库/06-内容创作与传播/Akkkk内容研究/抖音创作者Akkkk评论区画像]]



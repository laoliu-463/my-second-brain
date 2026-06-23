---
source_id: src-20260430-akkkk-douyin-contents-cleaned
original_title: creator_contents_cleaned.csv
title: Akkkk 抖音内容数据集
aliases:
  - creator_contents_cleaned.csv
source_type: dataset
author: 本地采集
published:
captured: 2026-04-30
canonical_url:
original_path: creator_contents_cleaned.csv
topics:
  - Akkkk
  - 内容数据
tags:
  - source
  - dataset
---

# Akkkk 抖音内容数据集

## 一句话摘要

该 CSV 是 Akkkk 抖音内容样本数据集，包含视频 ID、发布时间、标题/文案、互动指标、链接和下载相关字段。

## 数据用途

- 支撑 Akkkk 内容运营观察、高互动样本、主题索引和视频原文归档。
- 字段可用于按时间、互动指标和文本是否为空进行分析。

## 证据地图

| 证据位置 | 内容 | 影响页面 |
|---|---|---|
| CSV 表头 | `aweme_id`、发布时间、互动指标、链接字段 | [[知识库/90-来源与映射/Akkkk抖音数据集来源映射|Akkkk抖音数据集来源映射]] |
| 全量记录 | 393 条内容样本 | [[知识库/06-内容创作与传播/Akkkk内容研究/index|Akkkk内容研究]] |
| `is_text_empty` | 无文案视频识别 | [[知识库/06-内容创作与传播/Akkkk缺失视频补抓与转写索引|Akkkk缺失视频补抓与转写索引]] |

## 个人批注

- CSV 含 `user_id`、`sec_uid`、头像链接等个人标识字段。知识页只做聚合分析，不复制个人标识。
- 现有工具仍读取根路径 `creator_contents_cleaned.csv`，本批次不移动该文件。

## 待验证项

- 是否需要把根目录 CSV 改为 `raw/sources/` 下的唯一位置，需要先同步更新脚本和全部 sources 引用。

## 影响的知识页

- [[知识库/90-来源与映射/Akkkk抖音数据集来源映射]]
- [[知识库/06-内容创作与传播/Akkkk内容研究/index]]


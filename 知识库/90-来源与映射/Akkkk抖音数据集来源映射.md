---
title: Akkkk抖音数据集来源映射
tags: [来源映射, 数据集, 抖音, 内容创作]
created: 2026-04-30
updated: 2026-04-30
sources: [00-收集箱/未命名.md, creator_contents_cleaned.csv, creator_comments_cleaned.csv]
---

# Akkkk抖音数据集来源映射

## 概述

本页记录 `00-收集箱/未命名.md` 引用的两个 CSV 数据集如何映射到知识库页面。

## 来源文件

| 来源 | 说明 | 处理状态 |
|------|------|----------|
| `00-收集箱/未命名.md` | 收集箱入口，引用两个 CSV 文件 | 已整理 |
| `creator_contents_cleaned.csv` | Akkkk 内容数据，393 条 | 已提取统计、主题和高互动样本 |
| `creator_comments_cleaned.csv` | 评论样本，1732 条 | 已提取受众画像和评论主题 |

## 字段映射

### 内容表

| 字段 | 用途 |
|------|------|
| `aweme_id` | 内容唯一标识，与评论表关联 |
| `create_datetime` / `create_date` | 发布时间 |
| `nickname` | 创作者昵称 |
| `title` / `desc` / `content_text` | 标题、描述和文本内容 |
| `liked_count` / `collected_count` / `comment_count` / `share_count` | 互动指标 |
| `engagement_total` | 总互动指标 |
| `aweme_url` | 抖音页面链接 |
| `is_text_empty` | 是否缺少文本 |

### 评论表

| 字段 | 用途 |
|------|------|
| `comment_id` | 评论唯一标识 |
| `aweme_id` | 关联内容 |
| `create_datetime` / `create_date` | 评论时间 |
| `content` | 评论正文 |
| `like_count` | 评论点赞 |
| `ip_location` | 评论 IP 属地字段 |
| `is_top_level` | 是否顶层评论 |

## 已生成页面

- [[知识库/06-内容创作与传播/抖音创作者Akkkk内容运营观察|抖音创作者Akkkk内容运营观察]]
- [[知识库/06-内容创作与传播/抖音创作者Akkkk高互动样本|抖音创作者Akkkk高互动样本]]
- [[知识库/06-内容创作与传播/抖音创作者Akkkk评论区画像|抖音创作者Akkkk评论区画像]]
- [[Akkkk视频原文归档索引|Akkkk视频原文归档索引]]
- [[知识库/06-内容创作与传播/Akkkk缺失视频补抓与转写索引|Akkkk缺失视频补抓与转写索引]]

## 整理原则

- 不复制评论区用户 ID、头像、签名等个人标识字段。
- 评论内容只做聚合分析，必要时只引用主题，不建立用户个人页面。
- 无文本视频只标记为“无文本”，不凭互动量虚构内容主题。
- 对 `aweme_type` 等未解释字段保持谨慎，不做过度解释。

## 待补工作

- 对高收藏无文本视频做 ASR/OCR，补充内容主题。
- 建立逐条内容主题标签表。
- 将评论情绪分为求助、共鸣、质疑、复述、行动反馈等类型。
- 校对 `raw/sources/Akkkk缺失视频转写/` 中的 ASR 草稿，并将确认后的内容回填到逐条 `视频内容原文（ASR/OCR）`。
- 对 4 条 `request is not allowed` 视频重新导出有效下载链接或使用登录态人工补抓。

## 相关概念

- [[知识库/06-内容创作与传播/抖音创作者Akkkk内容运营观察|抖音创作者Akkkk内容运营观察]]
- [[知识库/06-内容创作与传播/抖音创作者Akkkk高互动样本|抖音创作者Akkkk高互动样本]]
- [[知识库/06-内容创作与传播/抖音创作者Akkkk评论区画像|抖音创作者Akkkk评论区画像]]
- [[Akkkk视频原文归档索引|Akkkk视频原文归档索引]]
- [[知识库/06-内容创作与传播/Akkkk缺失视频补抓与转写索引|Akkkk缺失视频补抓与转写索引]]


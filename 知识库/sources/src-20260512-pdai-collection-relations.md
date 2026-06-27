---
source_id: src-20260512-pdai-collection-relations
original_title: Collection 类关系图
title: Java 集合框架关系图来源
updated_at: 2026-06-27
aliases:
  - Collection 类关系图
  - Java Collection 类关系图
source_type: web-article
author: pdai
published: 2026-05-12
captured: 2026-06-23
canonical_url: https://pdai.tech/md/java/collection/java-collection-all.html
original_path: raw/sources/src-20260512-pdai-collection-relations/original.md
topics:
  - Java
  - 集合框架
tags:
  - source
---
# Java 集合框架关系图来源

## 原文跳转

- [[raw/sources/src-20260512-pdai-collection-relations/original.md|原文]]

## 一句话摘要
该来源按 Collection 和 Map 两个入口梳理 Java 容器体系，适合支撑 Java 集合概念页中的结构速查和实现选择。

## 作者核心观点

- Java 容器主要分为 `Collection` 与 `Map` 两条体系。
- 不同实现的选择取决于访问方式、顺序需求、排序需求和并发需求。
- `Hashtable`、`Vector` 属于历史线程安全容器，现代并发场景通常另选 `ConcurrentHashMap` 等方案。

## 证据地图

| 证据位置 | 内容 | 影响页面 |
|---|---|---|
| `original.md` 知识体系结构 | Collection 与 Map 的总体关系 | [[Collection类关系图]] |
| `original.md` Collection | List、Set、Queue 的主要实现 | [[Collection类关系图]] |
| `original.md` Map | TreeMap、HashMap、Hashtable、LinkedHashMap | [[Collection类关系图]] |

## 个人批注

- 该来源适合作为面试和复习的结构图证据，不宜直接替代 JDK 官方文档。

## 待验证项

- `published` 当前沿用历史收件箱创建日期，需人工确认网页真实发布日期。
- `raw` 原文与 `00-收件箱` 文件哈希不同，差异可能来自历史 frontmatter 处理。

## 影响的知识页

- [[Collection类关系图]]
- [[知识库/90-来源与映射/Collection类关系图来源映射]]



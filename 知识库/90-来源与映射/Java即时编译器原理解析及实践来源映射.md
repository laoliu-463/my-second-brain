---
title: Java即时编译器原理解析及实践来源映射
created: 2026-06-23
updated: 2026-06-27
tags:
  - 来源映射
  - JVM
  - JIT
sources:
  - raw/sources/src-20201022-meituan-jit-practice/original.md
  - 知识库/sources/src-20201022-meituan-jit-practice.md
---
# Java即时编译器原理解析及实践来源映射

## 概述

本页追踪《Java即时编译器原理解析及实践》与知识页的映射关系。  
原文全文保存在 `raw/sources/src-20201022-meituan-jit-practice/original.md`，不再作为最终知识页直接展示。

## 页面映射

| 正式页面 | 对应来源 | 作用 |
| --- | --- | --- |
| [[知识库/sources/src-20201022-meituan-jit-practice|Java JIT 编译器原理与实践]] | `raw/sources/src-20201022-meituan-jit-practice/original.md` | 主来源页：元数据、证据地图、影响页面 |
| [[知识库/02-后端知识体系/03-Java体系/Java即时编译器原理解析及实践|Java即时编译器原理解析及实践（旧兼容页）]] | 同上 | 旧来源入口，后续可迁移为重定向 |
| [[知识库/02-后端知识体系/02-计算机基础/JIT编译器详解|JIT编译器详解]] | 同上 | 知识层结论：分层编译、热点、IR、优化与调优口径 |
| [[raw/sources/src-20201022-meituan-jit-practice/original.md|Java即时编译器原文]] | `raw/sources/src-20201022-meituan-jit-practice/original.md` | 原始抓取稿已迁入 raw，收件箱副本已清理 |

## 说明

- 已确认：该主题的知识结论不在来源页重复；主知识页为 `JIT编译器详解`。  
- 主来源页为 `知识库/sources/src-20201022-meituan-jit-practice.md`，旧 Java 体系下来源页仅保留兼容。
- 若后续补充 JIT 与 AOT、OSR、分层阈值的新实证，应直接在知识页追加，并在本映射页补齐证据范围。

---
title: "Collection 类关系图"
created: 2026-05-17
updated: 2026-06-27
source_level: none
sources:
  - raw/sources/src-20260512-pdai-collection-relations/original.md
tags:
  - Java
  - 集合
  - JCF
---
# Collection 类关系图

> 这是一份知识页，不保留原文全文。原始材料保持在 `raw/` 下不变。

## 概述

Java 集合框架的核心是两个入口：`Collection` 与 `Map`。  
`Collection` 处理对象集合，`Map` 处理键值映射。两者都通过不同实现覆盖“有序性、去重、顺序和并发”需求。

## 结构速查

### Collection 族

| 场景 | 可选实现 | 典型特征 |
|---|---|---|
| 随机读多 | `ArrayList` | 查询快，插入/删除有数组搬移成本 |
| 频繁头尾操作 | `LinkedList` | 中间插入/删除更友好，可承担队列/双端队列角色 |
| 需要保序去重 | `LinkedHashSet` | `HashSet` + 插入顺序 |
| 需要排序视图 | `TreeSet` | 红黑树实现，支持范围查询 |

### Map 族

| 场景 | 可选实现 | 典型特征 |
|---|---|---|
| 通用映射 | `HashMap` | 默认选择，快速读写 |
| 保持顺序 | `LinkedHashMap` | 维护插入序/访问序 |
| 键排序查询 | `TreeMap` | 支持有序区间和范围检索 |
| 高并发共享 | `ConcurrentHashMap` | 并发读写下更稳定的主流选择 |

## 结论

- 优先基于访问特征选取容器，再按是否需要顺序、是否高并发决定具体实现。  
- `Hashtable`、`Vector` 属于历史并发模型，现代场景一般优先 `ConcurrentHashMap`、`ArrayList` + 外部同步策略。

## 相关知识与来源

- [[知识库/90-来源与映射/Collection类关系图来源映射|Collection 类关系图来源映射]]
- `raw/sources/src-20260512-pdai-collection-relations/original.md`


---
title: 迁移计划
created: 2026-06-23
updated: 2026-06-23
tags:
  - migration-plan
---

# 迁移计划

## 本批次目标

1. 把已入库原文从知识页中剥离为证据层。
2. 用 `original_title`、`title`、`source_id` 区分作者标题、显示标题和机器标识。
3. 用 `sources/`、`concepts/`、`entities/`、`syntheses/`、`maps/`、`_meta/`、`_review/` 表达页面类型。
4. 把多篇或多来源内容沉淀到概念页、实体页和综合页。

## 已执行

| 动作 | 文件 | 可逆方式 |
|---|---|---|
| 复制原文到 raw | `Skills 教程`、`DDD提示词`、`SAAS 全项目业务流程图` | 哈希一致，可删除新副本回退；未覆盖源文件 |
| 建立来源页 | `知识库/sources/*.md` | 删除新增来源页并恢复索引即可 |
| 建立知识页类型目录 | `concepts/`、`entities/`、`syntheses/`、`maps/` | 新增目录，无破坏性迁移 |
| 转移根目录碎片 | `C++.md` -> `知识库/_review/cpp-learning-fragment.md` | 作为复核项保留；移动时哈希一致，后续补丁改变工作区文件哈希口径 |
| 大图谱页瘦身 | `SAAS全项目业务流程图.md` | 原文已在 raw 保全，旧页变为兼容入口 |

## 暂缓项

| 文件 | 暂缓原因 | 下一步 |
|---|---|---|
| `creator_contents_cleaned.csv` | 工具脚本依赖根路径，且含个人标识字段 | 先改脚本和引用，再决定是否迁入 raw |
| `creator_comments_cleaned.csv` | 含评论用户标识字段，搬迁需同步敏感字段治理 | 先确认数据治理规则 |
| `00-收集箱/未命名 2.md` | 与已归档图谱重复但 frontmatter 不同 | 人工确认是否保留为采集入口或改为重定向 |
| `Hermes_Agent_研究报告.pptx` | 未抽取文本，无法判断类型 | 需要文档抽取后再建来源页 |
| `Hermes_Lecture_精简版.pptx` | 未抽取文本，无法判断类型 | 需要文档抽取后再建来源页 |

## 回滚条件

- raw 复制哈希不一致：停止引用新 raw 路径，保留原路径。
- 新来源页 source_id 冲突：保留原有页面，新页面改名或合并。
- 断链增加：恢复旧索引或补兼容入口。
- 人工确认 CSV 可迁移前，不移动根目录 CSV。
- `_review/cpp-learning-fragment.md` 不能作为不可变原文证据使用，只作为待整理碎片。

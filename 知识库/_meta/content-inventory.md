---
title: 内容清单
created: 2026-06-23
updated: 2026-06-23
tags:
  - inventory
  - migration
---

# 内容清单

## 扫描摘要

- 扫描根目录：`D:\Docs\Books\my second brain`
- 扫描范围：除 `.git/`、`.obsidian/` 外的全库文件
- 扫描文件数：1569
- Git 状态：`main...origin/main`，写入前未见未提交改动
- 本批次上限：20 个来源

## 类型分布

| 扩展名 | 数量 |
|---|---:|
| `.md` | 1263 |
| `.pdf` | 144 |
| `.json` | 48 |
| `.mp4` | 46 |
| `.py` | 36 |
| `.ppt` | 9 |
| `.txt` | 6 |
| `.csv` | 5 |
| `.docx` | 5 |
| `.pptx` | 3 |
| `.doc` | 1 |
| `.zip` | 1 |

## 本批次详细清单

| 原始路径 | 当前标题 | 文件类型 | 完整原文 | 批注/AI总结 | 原始链接/作者/日期 | 建议 source_id | 重复候选 | 建议合并页 | 目标路径 | 风险和待确认 |
|---|---|---|---|---|---|---|---|---|---|---|
| `00-收件箱/Skills 教程  菜鸟教程.md` | Skills 教程 | raw-source | 是 | 含本地 frontmatter | `https://www.runoob.com/skills/skills-tutorial.html` / 菜鸟教程 / 采集 2026-06-17 | `src-20260617-runoob-skills-tutorial` | `第二大脑-90-收件箱/03-知识/Skills教程.md` | [[知识库/concepts/Agent Skills]] | `raw/sources/src-20260617-runoob-skills-tutorial/original.md`；[[知识库/sources/src-20260617-runoob-skills-tutorial]] | 网页发布日期缺失 |
| `00-收集箱/DDD提示词.md` | DDD提示词（原始） | mixed | 是 | 是，提示词包含执行规则 | 本地来源 / 本地知识库 / 采集 2026-06-23 | `src-20260623-local-ddd-refactor-prompts` | `第二大脑-90-收件箱/03-知识/DDD提示词.md` | [[知识库/syntheses/SAAS DDD渐进式重构任务链]] | `raw/sources/src-20260623-local-ddd-refactor-prompts/original.md`；[[知识库/sources/src-20260623-local-ddd-refactor-prompts]] | 任务状态需与当前 SAAS 项目进度核对 |
| `知识库/06-内容创作与传播/Akkkk内容研究/SAAS全项目业务流程图.md` | SAAS 业务流程图 | raw-source | 是 | 否，工具生成 | code-review-graph / 生成 2026-05-24 | `src-20260524-code-review-graph-saas-flow` | `00-收集箱/未命名 2.md` | [[知识库/syntheses/SAAS代码图谱业务流程图]] | `raw/sources/src-20260524-code-review-graph-saas-flow/original.md`；[[知识库/sources/src-20260524-code-review-graph-saas-flow]] | 旧 wiki 页过大，已改为兼容入口 |
| `00-收集箱/未命名 2.md` | SAAS 全项目业务流程图 | mixed | 是 | 含状态 frontmatter | code-review-graph / 生成 2026-05-24 | `src-20260524-code-review-graph-saas-flow` | `知识库/06-内容创作与传播/Akkkk内容研究/SAAS全项目业务流程图.md` | [[知识库/syntheses/SAAS代码图谱业务流程图]] | 暂不移动；写入复核清单 | 与已归档图谱重复但 frontmatter 不同 |
| `00-收件箱/Java即时编译器原理解析及实践.md` | Java即时编译器原理解析及实践 | raw-source | 是 | 含本地 frontmatter | 美团技术博客 / 作者待确认 / 2020-10-22 | `src-20201022-meituan-jit-practice` | `raw/sources/src-20201022-meituan-jit-practice/original.md` | [[JIT编译器详解]] | [[知识库/sources/src-20201022-meituan-jit-practice]] | raw 与收件箱哈希不同，不自动覆盖 |
| `00-收件箱/Collection 类关系图.md` | Collection 类关系图 | raw-source | 是 | 含本地 frontmatter | pdai / 日期待确认 | `src-20260512-pdai-collection-relations` | `raw/sources/src-20260512-pdai-collection-relations/original.md` | [[Collection类关系图]] | [[知识库/sources/src-20260512-pdai-collection-relations]] | raw 与收件箱哈希不同，不自动覆盖 |
| `C++.md` | C++ 零散笔记 | source-note | 否 | 个人学习摘录 | 无 | 无 | 无 | 不创建概念页 | `知识库/_review/cpp-learning-fragment.md` | 信息碎片化；移动时哈希一致，后续补丁导致文件哈希口径异常，已列入复核 |
| `creator_contents_cleaned.csv` | Akkkk 抖音内容数据集 | raw-source | 是 | 否 | 本地采集 / 2026-04-30 | `src-20260430-akkkk-douyin-contents-cleaned` | 多个 Akkkk 页面引用 | [[知识库/06-内容创作与传播/Akkkk内容研究/index]] | [[知识库/sources/src-20260430-akkkk-douyin-contents-cleaned]] | 含个人标识字段；脚本依赖根路径，暂不移动 |
| `creator_comments_cleaned.csv` | Akkkk 抖音评论数据集 | raw-source | 是 | 否 | 本地采集 / 2026-04-30 | `src-20260430-akkkk-douyin-comments-cleaned` | 多个 Akkkk 页面引用 | [[知识库/06-内容创作与传播/Akkkk内容研究/抖音创作者Akkkk评论区画像]] | [[知识库/sources/src-20260430-akkkk-douyin-comments-cleaned]] | 含个人标识字段；暂不移动 |
| `Hermes_Agent_研究报告.pptx` | Hermes Agent 研究报告 | unknown | 未确认 | 未确认 | 本地文件 / 2026-04-25 | 待定 | Hermes 相关页面可能引用 | 待复核 | 暂不移动 | 未抽取文本，需人工决定是否作为来源 |
| `Hermes_Lecture_精简版.pptx` | Hermes Lecture 精简版 | unknown | 未确认 | 未确认 | 本地文件 / 2026-04-25 | 待定 | Hermes 相关页面可能引用 | 待复核 | 暂不移动 | 未抽取文本，需人工决定是否作为来源 |

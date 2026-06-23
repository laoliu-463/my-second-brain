---
title: 待复核项
created: 2026-06-23
updated: 2026-06-23
tags:
  - review
---

# 待复核项

## 需要人工决定

| 项 | 证据 | 风险 | 建议动作 |
|---|---|---|---|
| JIT raw 与收件箱哈希不同 | `raw/sources/src-20201022-meituan-jit-practice/original.md` vs `00-收件箱/Java即时编译器原理解析及实践.md` | 不清楚差异是否仅为 frontmatter | 人工 diff 后决定是否保留双版本 |
| Collection raw 与收件箱哈希不同 | `raw/sources/src-20260512-pdai-collection-relations/original.md` vs `00-收件箱/Collection 类关系图.md` | 不清楚差异是否仅为 frontmatter | 人工 diff 后决定是否保留双版本 |
| `00-收集箱/未命名 2.md` | 与 SAAS 图谱来源高度重复 | 自动删除会破坏采集入口追踪 | 改为重定向前需用户确认 |
| Akkkk CSV 根路径 | `tools/download_missing_akkkk_videos.py` 依赖 `creator_contents_cleaned.csv` | 直接移动会破坏脚本 | 先改脚本，再迁移 raw |
| CSV 个人标识字段 | `user_id`、`sec_uid`、头像链接等 | 正式知识页不应复制个人标识 | 建立数据脱敏规则 |
| Hermes PPTX | 根目录两个 PPTX | 未抽取文本，无法分类 | 后续用文档工具抽取后再建来源页 |
| `知识库/02-后端知识体系/03-Java体系/Java即时编译器原理解析及实践.md` | 旧来源页仍在主题目录 | 目录类型与页面类型不一致 | 当前保留兼容，后续可迁到 `sources/` 后留重定向 |
| `_review/cpp-learning-fragment.md` | 由根目录 `C++.md` 移入 | 移动时哈希一致，补丁重写后工作区 SHA256 不再等于移动时记录 | 仅作为待整理碎片，不作为原文证据层 |
| `brain_search.py 来源页` | 验证返回 NO_MATCH | 新增 `知识库/sources` 可能不在第二大脑脚本搜索范围 | 后续扩展搜索脚本或使用全库搜索 |

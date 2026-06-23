---
title: 沉淀日志
created: 2026-06-23
updated: 2026-06-23
tags:
  - distillation-log
---

# 沉淀日志

## [2026-06-23] reorganize | 来源页与知识页分层

- 扫描全库 1569 个文件，优先处理收件箱、根目录散落文件、超大原文页和重复候选。
- 新增 `知识库/sources/` 主来源页，区分 `source_id`、`original_title` 和显示标题。
- 为 Agent Skills、SAAS DDD 重构任务链、SAAS code-review-graph 图谱建立概念/综合页。
- 为菜鸟教程、美团技术博客、pdai、code-review-graph 建立实体页。
- 将 `SAAS全项目业务流程图` 超长工具输出复制到 raw 后，把旧 wiki 页改为兼容入口。
- 将根目录 `C++.md` 移入 `_review`；移动时哈希一致，但后续补丁改变工作区文件哈希口径，已列为复核项。

## 验证记录

| 检查 | 结果 | 说明 |
|---|---|---|
| raw 复制哈希 | PASS | Skills、DDD 提示词、SAAS 图谱复制到 raw 后哈希一致 |
| 主来源页 source_id | PASS | `知识库/sources/src-*.md` 共 7 个，未发现重复 source_id |
| 0 字节文件 | PASS | 全库未发现 0 字节文件 |
| `line_guard.py` | PASS | 11 个第二大脑实例结构约束通过 |
| `brain_lint.py` | PASS | 11 个第二大脑实例索引 LINT 通过 |
| `brain_search.py 来源页` | LIMITATION | 返回 NO_MATCH，疑似脚本不覆盖 `知识库/sources` 新目录 |

## 2026-06-23 全量文章内容整理

- 扫描文件：1652；Markdown：1290；raw 来源组：227。
- 新建来源页：222；已有来源页：5。
- 刷新：`content-inventory.md`、`migration-plan.md`、`sources/index.md`、`content-distillation-map.md`、`unresolved-items.md`。
- 安全边界：未删除文件，未覆盖 raw 原文，未批量移动历史知识页。
- 分类分布：concept=400；entity=20；mixed=2；question=1；raw-source=67；source-note=19；synthesis=277；unknown=504

## 2026-06-23 全量文章内容整理

- 扫描文件：1875；Markdown：1513；raw 来源组：227。
- 新建来源页：0；已有来源页：227。
- 刷新：`content-inventory.md`、`migration-plan.md`、`sources/index.md`、`content-distillation-map.md`、`unresolved-items.md`。
- 安全边界：未删除文件，未覆盖 raw 原文，未批量移动历史知识页。
- 分类分布：concept=401；entity=20；mixed=2；question=1；raw-source=67；source-note=241；synthesis=277；unknown=504
- 验证补充：轻量断链检查扫描 1513 个 Markdown，发现 2050 个无法自动解析的链接候选，已写入复核清单；未做批量改链。

## 2026-06-23 原文跳转链接硬约束

- 更新 `kb-organize`、`AGENT_CONTRACT`、`COMPLETION_GATES`：正式知识内容必须同时具备来源页回链和原文跳转链接。
- 更新 `tools/kb_full_distill.py`：后续生成来源页时写入可点击原文链接，并保留路径、大小和哈希。
- 批量补齐 `知识库/sources/src-*.md` 的 `## 原文跳转` 小节，覆盖 229 个来源页。
- 验证结果：229 个来源页均存在原文跳转小节；其中 2 个 CSV 来源仍指向根目录原始文件，因脚本依赖暂未迁入 raw。

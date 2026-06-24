---
id: kb-raw-06-报告-source-link-repair-report
type: evidence
title: '来源链接修复报告'
original_title: '来源链接修复报告'
aliases: []
status: active
source_id: ''
created: 2026-06-24
updated: 2026-06-24
---

# 来源链接修复报告

## 扫描结果

- 扫描时间：2026-06-24 01:13:05 +0800
- 知识库根目录：`D:\Docs\Books\my second brain`
- RAW_DIR：`raw/`
- 当前实例未使用 `wiki/sources`、`wiki/concepts`、`wiki/entities`、`wiki/syntheses`、`wiki/questions` 目录结构；按现有实例规范使用 `第二大脑-95-原始资料/03-知识` 与 `01-状态/资料来源.md`。
- 来源页候选数量：30
- 原始文件数量：319
- 知识库 Markdown 页面数量：547
- canonical_url 数量：0

## 修复结果

- 新增全量原始文件索引：[[raw-原始文件索引|raw 原始文件索引]]
- 新增本地原文文件链接数：319
- 新增/规范化来源目录与示例文件链接数：13
- 修复错误路径数：0（本轮未发现已存在链接需要改写为另一路径；新增链接均来自真实文件系统扫描）
- 新增知识页到来源索引链接数：4
- 新增来源页到知识页链接数：0（当前没有可证据化的逐条知识页反向绑定；未按标题猜测）
- 补充原始网页链接数：0（现有 raw 文件未提供可验证 canonical_url，未伪造网页链接）

## 哈希与原文保护

- 已为 319 个 raw 文件计算 SHA-256，并写入 [[raw-原始文件索引|raw 原始文件索引]]。
- 本轮未写入、移动、重命名或删除 `raw/` 下任何文件。
- raw 文件哈希基线已固化；后续复查可用该索引逐项比对。

## 异常

| 页面路径 | source_id | 当前 raw_path | 推测目标 | 无法修复原因 | 推荐处理方式 |
|---|---|---|---|---|---|
| `第二大脑-95-原始资料/03-知识/Akkkk视频转写.md` | 未建立独立 source_id | `raw/sources/Akkkk缺失视频转写/` | [[raw-原始文件索引|raw 原始文件索引]] 中对应目录文件 | 多文件目录来源，缺少逐文件 canonical_url 与明确知识页引用边界 | 如需逐条引用，按视频/转写文件建立来源页或在知识页显式声明 source_id |
| `第二大脑-95-原始资料/03-知识/抖音团长SaaS设计.md` | 未建立独立 source_id | `raw/sources/抖音团长SaaS设计文档/` | [[raw-原始文件索引|raw 原始文件索引]] 中对应目录文件 | 多文件目录来源，缺少逐文件 canonical_url 与明确知识页引用边界 | 如需逐条引用，按设计文档建立来源页或在知识页显式声明 source_id |
| `第二大脑-95-原始资料/03-知识/raw-资料来源.md` | 未建立独立 source_id | `raw/sources/` | [[raw-原始文件索引|raw 原始文件索引]] | 该页是来源登记页，不是单一来源页 | 保留为来源目录入口；逐文件来源以 raw 索引为准 |
| 全库知识页 | 无法可靠批量确定 | 多处未声明 | 不自动推断 | 仅靠标题、作者或目录名无法证明某条知识陈述来自哪个 raw 文件 | 在知识页补 `source_id` 或显式来源页链接后再做双向反链 |
| `第二大脑-95-原始资料` | 不适用 | 不适用 | 不适用 | 当前实例不存在标准 wiki 子目录：wiki/sources, wiki/concepts, wiki/entities, wiki/syntheses, wiki/questions | 不强行创建新目录；沿用现有实例规范 |
| 全库 source_id 扫描 | `created: 2026-06-23` | 不适用 | 不适用 | source_id 出现 4 次 | 人工确认是否为同一来源复用或重复定义 |

## 验证清单

- 每个新增本地原始文件链接均由文件系统扫描生成。
- 相对路径从 `第二大脑-95-原始资料/03-知识/raw-原始文件索引.md` 出发生成，使用 `/` 分隔，并使用 Markdown 角括号包裹。
- 未记录 canonical_url 的条目没有生成虚假网页链接。
- 不依赖文件标题批量猜测知识页来源；无法确认项进入本报告异常表。

## 抽样验证项

- `.md`：[raw/sources/Akkkk缺失视频转写/2024-06-07_7377747575333604646.md](<../../raw/sources/Akkkk缺失视频转写/2024-06-07_7377747575333604646.md>), SHA-256 `a24da2786b715a04127eddbc790f8c642bdb47b5ab542c1f4ddc40af59053e3b`
- `.pdf`：[raw/sources/CSS揭秘.pdf](<../../raw/sources/CSS揭秘.pdf>), SHA-256 `595323e8fa4e46bfbaf012a627bb818ca9e0a7d7e0da0de7f699ea4f1f25a8d6`
- `.mp4`：[raw/assets/Akkkk缺失视频/2024-06-07_7377747575333604646.mp4](<../../raw/assets/Akkkk缺失视频/2024-06-07_7377747575333604646.mp4>), SHA-256 `e976969639e656d6d412fc6bb5fde5935ebc074026d236696c7621813cf332e8`

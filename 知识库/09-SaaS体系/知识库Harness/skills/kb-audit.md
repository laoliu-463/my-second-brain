# Skill: kb-audit

## 触发条件

用户说"巡检知识库"、"LINT"、"审计"、"harness 知识库"时使用。

## 步骤

### 1. 建立 all_wiki 映射

扫描 vault 下所有 .md 文件，构建 `文件名(去md) → 相对路径` 的映射。

### 2. 扫描所有 index.md 的链接

用正则 `\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]` 提取所有 wiki link，汇总为 indexed_keys。

### 3. 计算孤立文件

`orphans = all_keys - indexed_keys - {'index'}`

### 4. 扫描 broken links

对每个文件内容中的 wiki link，检查目标是否在 all_wiki 中。

### 5. 识别 stub

文件大小 < 200 字节。

### 6. 识别 zero-byte 文件

文件大小 == 0。

### 7. 识别重复标题

提取每个文件 `# 标题`，找同标题不同路径。

### 8. 输出报告

```
Total: N files
Indexed: N (M%)
Orphans: N
  - 分类/文件名1.md (原因)
  - 分类/文件名2.md (原因)
Broken links: N
Stubs: N
Zero-byte: N
Duplicates: N
```

## 证据要求

- 孤立文件完整清单（路径）
- stub 文件内容片段（前3行）
- 重复标题文件对

## 路由

发现孤立 → KB-ORG 系列任务
发现 zero-byte → KB-GC-STUBS
发现 duplicate → KB-GC-DUP

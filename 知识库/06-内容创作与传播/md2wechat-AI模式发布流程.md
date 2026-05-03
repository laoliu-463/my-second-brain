---
title: md2wechat AI 模式发布流程
tags: [公众号, md2wechat, AI模式, 发布流程]
created: 2026-05-03
updated: 2026-05-03
sources: [md2wechat-skill 项目文档, 2026-05-03 实测验证]
---

# md2wechat AI 模式发布流程

## 概述

AI 模式是 md2wechat 的本地生成路径：不依赖 md2wechat.cn API Key，直接由 LLM 生成 HTML，再调用微信接口创建草稿。适合没有 API Key 但想用精美排版的用户。

**前提条件：**
- 微信公众号已认证（用于获取 appid/secret）
- WSL 出口 IP 已加入微信公众号后台白名单
- 封面图（可本地生成或使用已有素材）

## 完整发布流程（5 步）

### Step 1：准备文章 Markdown

frontmatter 必须包含 title、author、digest：

```markdown
---
title: 文章标题
author: 作者名
digest: 摘要（限128字）
---

# H1 标题（不要和 title 完全重复）

正文内容...
```

### Step 2：检查 metadata

```bash
export PATH="/home/caojianing/.hermes/node/bin:$PATH"
md2wechat inspect article.md
```

关注输出中的 `convert_ready` 和 `draft_ready`，以及 `TITLE_BODY_MISMATCH` 等 INFO 提示。

### Step 3：AI 模式生成 HTML

```bash
md2wechat convert article.md --mode ai --theme autumn-warm \
  --output /tmp/article_output.html --json
```

输出示例：
```json
{
  "success": true,
  "code": "CONVERT_AI_REQUEST_READY",
  "status": "action_required",
  "data": {
    "prompt_file": "/tmp/article_output.prompt.txt",
    "requested_output_file": "/tmp/article_output.html"
  }
}
```

**AI 模式返回 `action_required`，表示需要 LLM 执行 prompt 生成 HTML。**

### Step 4：LLM 执行 prompt 生成 HTML

将 `prompt_file` 内容发给 LLM，LLM 生成 HTML 写入 `requested_output_file`。

推荐使用 subagent 并发执行：
```bash
# LLM 执行 prompt，结果写入 /tmp/article_output.html
```

验证生成结果：
```bash
ls -la /tmp/article_output.html
wc -c /tmp/article_output.html  # 通常 5-20KB 为正常
```

### Step 5：创建微信草稿

**方案 A：有封面图 → 用 test-draft**

```bash
md2wechat test-draft /tmp/article_output.html cover.png --json
```

成功返回：
```json
{
  "success": true,
  "code": "TEST_DRAFT_CREATED",
  "data": {
    "media_id": "LZfQeDRIVZbX1DOPkTjB3nEhb..."
  }
}
```

**方案 B：无封面图或想复用素材 → 用 create_draft + JSON**

构造 JSON 后执行：
```bash
md2wechat create_draft draft.json --json
```

## 封面图方案

### 方案 1：本地生成（需 Volcengine API Key）

```bash
md2wechat generate_cover \
  --title "文章标题" \
  --summary "文章摘要" \
  --style autumn-warm \
  --json
```

**当前限制：** 需要配置文件中 `api.image_key` 为真实 Volcengine Key（当前为占位符）。

### 方案 2：用 ffmpeg 生成纯色封面

```bash
ffmpeg -f lavfi -i "color=0xfef4e7:s=900x383:d=1" \
  -frames:v 1 /tmp/cover.png -y
```

适用于测试，最小可用（900×383 即可）。

### 方案 3：复用已有素材

在微信公众号后台 → 内容与互动 → 素材管理 中找到已有图片的 media_id，使用 `--cover-media-id` 参数。

## 关键路径和文件

| 用途 | 路径 |
|------|------|
| md2wechat CLI | `/home/caojianing/.hermes/node/bin/md2wechat` |
| WSL 配置文件 | `~/.config/md2wechat/config.yaml` |
| 项目路径 | `/mnt/d/Projects/OpenSource/md2wechat-skill/` |
| 测试文章 | `/mnt/d/Projects/OpenSource/md2wechat-skill/test_article.md` |
| 生成的 HTML 示例 | `/tmp/ai_output.html` |

## 配置文件关键字段

```yaml
wechat:
    appid: wx0a4204f0dfa437ca
    secret: 980b9b8e6c187fc6ae3...
api:
    md2wechat_key: your_md2wechat_api_key  # AI 模式不需要！
    md2wechat_base_url: https://www.md2wechat.cn
```

**AI 模式只需要 wechat.appid + wechat.secret，不需要 md2wechat_key。**

## 常见错误排查

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `errcode=40164: invalid ip` | WSL 出口 IP 不在白名单 | 微信公众号后台 → 基本配置 → IP白名单，加入出口 IP |
| `Invalid API Key format` | md2wechat_key 是占位符 | AI 模式不需要此字段，确认配置文件中 `mode` 或 `--mode ai` |
| `IMAGE_GENERATE_FAILED: Volcengine API Key` | 封面图生成失败 | 手动准备封面图，或配置真实 Volcengine Key |
| `TEST_DRAFT_COVER_FAILED` | 封面上传失败 | 检查 IP 白名单 + 封面图尺寸（最小 900×383） |

## 验证时间线（2026-05-03 实测）

| 时间 | 事件 |
|------|------|
| 配置 IP 白名单 42.84.233.154 | 微信公众号后台添加 |
| 验证 access_token 获取 | 成功返回 token |
| test-draft 草稿创建 v1 | 成功，含 `<style>@import` 字体（兼容性存疑） |
| HTML 排版优化 | 去除外部依赖，修复 CDN 字体问题 |
| test-draft 草稿创建 v2 | 成功，无外部资源依赖 |

## HTML 排版优化记录

### 问题：内置 autumn-warm 主题的 CDN 字体问题

内置 `autumn-warm` 主题 prompt 第 97 行写"字体通过CDN链接"，与"禁止 `<style>` 标签"矛盾。子代理生成的 HTML 包含：
```html
<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');</style>
```
微信公众号编辑器会过滤 `<style>` 标签和外部链接，导致字体回退到系统默认。

### 解决方案：使用 --custom-prompt 传入优化版提示词

**Step 3 改为：**
```bash
# 使用优化后的 prompt（已修复 CDN 字体问题）
md2wechat convert article.md --mode ai \
  --custom-prompt "$(cat /tmp/optimized_prompt.txt)" \
  --output /tmp/article.html --json
```

**优化 prompt 关键改动：**
- 绝对禁止 `<style>`、`<head>`、`<link>` 标签
- 绝对禁止任何外部 CDN 链接、@import
- 字体只通过 `font-family` 内联在每个元素上
- HTML 从 `<body>` 内的 `<div>` 开始
- 使用纯 CSS 系统字体栈（无外部依赖）

**优化 prompt 文件路径：** `/tmp/optimized_prompt.txt`

**极简主义 v3（合并版）prompt 文件：** `/tmp/optimized_prompt_minimal_v3.txt`（v1蓝色+v2参数）

### 验证命令
```bash
# 检查是否有外部资源引用
grep -E '<style|<head|<link|@import' /tmp/article.html
# 应无输出

## 相关概念

- [[内容创作导航中心]] — 各内容平台的入口和工具总览
- [[Hermes 使用指南]] — 发布工具的使用方法

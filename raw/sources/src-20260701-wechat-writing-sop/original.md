---
title: 公众号写作与发布SOP本地证据快照
created: 2026-07-01
source_type: local_knowledge_synthesis
redaction: secrets_redacted
---
# 公众号写作与发布SOP本地证据快照

## 本地知识库来源

- `知识库/06-内容创作与传播/内容创作导航中心.md`
  - 记录公众号发布核心工具 `md2wechat`
  - 记录 API 模式命令: `inspect` -> `preview` -> `convert --draft --cover`
  - 记录 AI 模式命令: `inspect` -> `convert --mode ai` -> LLM 生成 HTML -> `test-draft`
  - 记录 AI 公众号文章项目路径: `D:\Projects\OpenSource\AI微信公众号`
- `知识库/06-内容创作与传播/prompts/md2wechat-AI模式发布流程.md`
  - 记录 Markdown frontmatter 要求: `title`、`author`、`digest`
  - 记录 AI 模式 5 步发布流程
  - 记录微信公众号编辑器会过滤 `<style>`、外部链接、`@import` 等兼容性风险
  - 记录优化 prompt 要求: 禁止 `<style>`、`<head>`、`<link>`、外部 CDN 与 `@import`
  - 记录封面图方案与微信草稿创建方式
- `知识库/06-内容创作与传播/prompts/ai主题-prompt-深度认知干货菁英风v4终极版.txt`
  - 记录深度认知/干货菁英风排版 prompt
  - 适合作为认知类、方法论类、观点型长文排版风格
- `知识库/06-内容创作与传播/prompts/ai主题-prompt-极简主义v3合并版.txt`
  - 记录极简主义公众号排版 prompt
  - 适合克制、干净、信息密度较高的公众号长文

## 本地项目来源

- `D:\Projects\OpenSource\AI微信公众号\harness-engineering\README.md`
  - 定位: Harness Engineering 学习指南
  - 结构: concepts、thinking、practice、feedback、works、prompts、references
  - 输出路径: 作品、翻译、学习笔记、独立思考
- `D:\Projects\OpenSource\AI微信公众号\harness-engineering\AGENTS.md`
  - 记录学习档案的分阶段结构: 概念理解、独立思考、动手实践、反馈记录、作品输出
- `D:\Projects\OpenSource\md2wechat-skill\README.md`
  - 定位: 用 Markdown 写公众号文章，转为微信公众号格式
  - 记录安装、能力发现、主题列表、prompt 列表、AI 模式与 API 模式边界
- `D:\Projects\OpenSource\md2wechat-skill\docs\WRITING_FAQ.md`
  - 记录写作功能: 观点/片段/大纲/标题扩展为完整文章
  - 记录 `md2wechat write --style dan-koe -o article.md`
  - 记录生成后需要人工修改，AI 文章是起点，不是终点
  - 记录封面提示词、封面尺寸建议和转换到微信格式流程

## 整合后的 SOP 口径

- 默认公众号类型: AI/工程技术长文，兼容认知方法论类文章。
- AI 职责: 帮助扩展初稿、润色、提炼标题摘要、生成封面 prompt、生成排版 HTML。
- 用户职责: 决定选题、观点、事实边界、是否发布、是否代表本人立场。
- 证据优先: 技术类文章必须保留来源、链接、事实核查和发布前复核。
- 发布前必须验证: metadata、移动端预览、外部资源过滤、封面、草稿箱、敏感信息、版权和事实风险。
- 不保存敏感信息: 微信公众号 appid/secret、API Key、Cookie、access token 不写入知识库。

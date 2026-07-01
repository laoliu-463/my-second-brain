---
title: 公众号写作与发布SOP
tags: [公众号, 内容创作, md2wechat, 写作流程, 发布SOP]
created: 2026-07-01
updated: 2026-07-01
source_level: mixed
source_id: src-20260701-wechat-writing-sop
raw_path: raw/sources/src-20260701-wechat-writing-sop/original.md
canonical_url:
sources:
  - raw/sources/src-20260701-wechat-writing-sop/original.md
  - 知识库/06-内容创作与传播/内容创作导航中心.md
  - 知识库/06-内容创作与传播/prompts/md2wechat-AI模式发布流程.md
  - D:/Projects/OpenSource/AI微信公众号/harness-engineering/README.md
  - D:/Projects/OpenSource/md2wechat-skill/docs/WRITING_FAQ.md
---
# 公众号写作与发布SOP

## 定位

本 SOP 用于把一个想法稳定推进为微信公众号草稿或正式发布文章。

默认内容类型是 AI/工程技术长文，兼容认知方法论、个人学习复盘、工具介绍和观点型文章。

核心原则:

- 用户决定选题、观点、事实边界和是否发布。
- AI 只负责辅助扩展、整理、润色、排版和风险提示。
- 技术文章必须有证据链，不能把 AI 生成内容直接当事实。
- 发布前必须经过人工预览、事实检查和平台兼容性检查。

## 总流程

```text
选题入池
  -> 写作前拷问
  -> 资料与证据收集
  -> 大纲与主张确认
  -> 初稿生成或人工起稿
  -> 事实校验与结构改稿
  -> md2wechat metadata 检查
  -> HTML/排版生成
  -> 微信草稿创建
  -> 手机预览与发布前审查
  -> 发布
  -> 数据复盘与沉淀
```

## Step 0：选题入池

选题必须先写成一张选题卡，不要直接开始生成全文。

选题卡模板:

```markdown
---
title:
type: 技术解读 / 翻译改写 / 工具教程 / 认知方法论 / 复盘
status: 待写作
target_reader:
core_claim:
counter_intuition:
evidence:
publish_channel: 微信公众号
---

## 一句话选题

## 为什么现在值得写

## 读者读完能带走什么

## 不能写或需要谨慎写的边界
```

选题通过条件:

- 有明确目标读者。
- 有一句可争辩的核心主张。
- 至少有 2 条来源或经验事实支撑。
- 能说清读者读完后的行动或认知变化。
- 不依赖未经核实的 AI 事实。

## Step 1：写作前拷问

写作前按顺序回答。答不清的问题，先补资料，不进入初稿。

| 问题 | 推荐答案口径 |
|---|---|
| 这篇文章给谁看？ | 写给正在学习 AI 工程化、工具链、智能体实践的人，而不是泛泛写给所有人 |
| 文章解决什么具体问题？ | 解决一个可描述的理解、操作或决策问题 |
| 核心主张是什么？ | 一句话能复述，不超过 30 字 |
| 反常识点是什么？ | 不是堆信息，而是指出一个常见误区或更有效路径 |
| 证据在哪里？ | 原文链接、本地项目、实测命令、截图、日志或数据 |
| 哪些内容不能让 AI 编？ | 事实数据、项目结论、法律/财务/医疗判断、个人经历 |
| 读者读完下一步做什么？ | 能执行一条命令、复用一个模板、改变一个判断或收藏一张清单 |
| 发布失败的风险是什么？ | 事实错误、外链失效、排版异常、封面不合规、标题夸大、敏感信息泄露 |

## Step 2：资料与证据收集

不同文章类型的最低证据要求:

| 类型 | 必备证据 |
|---|---|
| 技术解读 | 官方文档、源码或 README、版本号、实测命令 |
| 翻译改写 | 原文链接、作者、发布日期、术语表、删改说明 |
| 工具教程 | 安装命令、配置路径、成功日志、失败处理 |
| 认知方法论 | 具体场景、案例、反例、可执行动作 |
| 复盘 | 时间线、决策点、结果、失败证据、后续动作 |

资料记录格式:

```markdown
## 证据

- 来源:
- 路径/链接:
- 关键事实:
- 可信度:
- 是否需要二次验证:
```

禁止事项:

- 不引用无法回溯的“网上说法”。
- 不把 AI 总结当成一手来源。
- 不在文章中放 API Key、Cookie、token、私密配置。
- 不把未验证的命令写成“可直接运行”。

## Step 3：确定文章结构

推荐结构:

```text
标题
摘要 digest
开头钩子
问题场景
核心主张
证据与案例
方法或步骤
常见误区
行动清单
结尾观点
```

技术类文章可以使用:

```text
问题是什么
为什么常规做法不够
关键概念
本地实测
最小可复现路径
推荐做法
风险与边界
验证清单
```

认知方法论类文章可以使用:

```text
一个具体现象
常见解释
更底层的解释
案例
可执行方法
反例和边界
总结金句
```

## Step 4：生成或撰写初稿

如果只用已有观点扩展文章，可以使用 md2wechat 写作功能:

```powershell
md2wechat write --style dan-koe -o article.md
```

如果已有片段需要润色:

```powershell
md2wechat write --style dan-koe --input-type fragment article.md -o article.rewrite.md
```

如果已有大纲:

```powershell
md2wechat write --style dan-koe --input-type outline outline.md -o article.md
```

初稿要求:

- 保留 Markdown 格式。
- 明确标出事实、观点、推论。
- 对外部事实加来源占位。
- 不直接进入排版。
- 不使用夸张标题替代真实主张。

## Step 5：人工改稿

改稿顺序:

1. 先改主张: 文章到底想让读者相信什么。
2. 再改结构: 每一节是否服务于主张。
3. 再补证据: 技术事实、命令、截图、日志、链接。
4. 再改语言: 删除空话、套话、重复句。
5. 最后改标题、摘要、金句和结尾。

人工改稿检查:

- 开头 300 字是否讲清问题。
- 每个小标题下是否有实质信息。
- 是否存在“看起来很对但没有证据”的段落。
- 是否存在 AI 味过重的泛化表达。
- 是否有具体动作或判断标准。

## Step 6：md2wechat metadata

公众号发布稿必须有 frontmatter:

```markdown
---
title: 文章标题
author: 作者名
digest: 128字以内摘要
---

# 正文标题
```

注意:

- `title` 是后台标题。
- `digest` 会影响分享卡片摘要。
- 正文 H1 不要和 `title` 完全重复。
- 摘要要写“读者为什么要点开”，不是复述标题。

检查:

```powershell
md2wechat inspect article.md
```

通过标准:

- `convert_ready=true`
- `draft_ready=true`
- 没有 metadata 缺失
- 只有可接受的 INFO，不存在阻断性 ERROR

## Step 7：排版与 HTML 生成

### API 模式

适合已经配置 `md2wechat.cn` API Key 的环境:

```powershell
md2wechat preview article.md
md2wechat convert article.md --draft --cover cover.jpg
```

### AI 模式

适合本地生成 HTML:

```powershell
md2wechat convert article.md --mode ai --theme autumn-warm `
  --output article.html --json
```

命令返回 `prompt_file` 后，由 LLM 执行 prompt，把 HTML 写入 `requested_output_file`。

生成后检查:

```powershell
Select-String -Path article.html -Pattern '<style|<head|<link|@import'
```

通过标准:

- 无 `<style>`
- 无 `<head>`
- 无 `<link>`
- 无 `@import`
- 无外部 CDN 字体
- 主要样式使用内联样式

## Step 8：封面

封面优先使用 16:9:

```text
推荐尺寸: 2560x1440
最低测试尺寸: 900x383
```

封面生成路径:

```powershell
md2wechat write --style dan-koe --cover-only > cover_prompt.txt
```

封面验收:

- 标题在手机端能看清。
- 不使用过度营销化文字。
- 不遮挡主体。
- 与文章主张一致。
- 不包含敏感信息、品牌误导或侵权素材。

## Step 9：创建微信草稿

有封面图:

```powershell
md2wechat test-draft article.html cover.png --json
```

复用素材库图片:

```powershell
md2wechat create_draft draft.json --json
```

成功标志:

- 返回草稿创建成功。
- 返回 `media_id` 或草稿相关信息。
- 微信公众号后台草稿箱可见。

## Step 10：发布前审查

发布前必须手机预览。

审查清单:

- 标题没有夸大承诺。
- 摘要不误导。
- 首屏能看清主题。
- 段落间距正常。
- 图片不变形。
- 代码块可读。
- 链接可点击。
- 没有 `<style>` 被过滤导致的排版崩坏。
- 没有外部字体依赖。
- 没有 API Key、Cookie、token、个人隐私。
- 技术命令已注明环境前提。
- 结论与证据一致。

未通过时回到对应步骤，不允许靠“应该没问题”发布。

## Step 11：发布

发布前最后确认:

- 账号正确。
- 标题、封面、摘要正确。
- 文章分类、合集、原创声明按实际情况选择。
- 引用来源和转载边界已处理。
- 如果是翻译或改写，保留原文链接和说明。

发布后记录:

```markdown
## 发布记录

- 标题:
- 发布平台: 微信公众号
- 发布时间:
- 草稿来源:
- 封面来源:
- 主要来源:
- 发布链接:
- 待观察指标:
```

## Step 12：复盘

建议 24 小时、72 小时、7 天各记录一次。

复盘指标:

- 阅读量
- 完读率
- 分享
- 收藏
- 关注转化
- 留言质量
- 读者问题
- 哪个标题/开头/观点有效
- 哪些地方造成误解

复盘模板:

```markdown
## 复盘

### 数据

### 有效点

### 问题

### 下一篇可延展选题

### SOP 需要更新的地方
```

## 文件命名

建议:

```text
YYYY-MM-DD-文章短标题.md
YYYY-MM-DD-文章短标题.html
YYYY-MM-DD-文章短标题-cover.png
YYYY-MM-DD-文章短标题-review.md
```

技术长文建议放在对应项目 `works/` 或 `drafts/`，不要只存在聊天记录里。

## 常见故障

| 现象 | 可能原因 | 处理 |
|---|---|---|
| `inspect` 不通过 | 缺 title、author、digest | 补 frontmatter |
| 草稿创建失败 | 微信配置、IP 白名单、封面问题 | 查 `md2wechat-AI模式发布流程` 的错误表 |
| 排版在微信里变样 | 使用了 `<style>`、外链字体、`@import` | 改为纯内联样式 |
| 文章像 AI 生成 | 缺个人判断、案例和取舍 | 回到 Step 1 和 Step 5 |
| 技术事实被质疑 | 来源不足或命令未验证 | 补官方来源和本地验证记录 |
| 封面上传失败 | 尺寸、格式或素材问题 | 用 16:9 PNG/JPG 重新生成 |

## 完成定义

一篇公众号文章只有同时满足以下条件，才算完成:

- 选题卡完整。
- 核心主张明确。
- 事实证据可回溯。
- Markdown metadata 通过检查。
- HTML 兼容微信编辑器。
- 草稿箱创建成功。
- 手机预览通过。
- 发布前人工确认。
- 发布后记录链接和复盘项。

## 相关页面

- [[内容创作导航中心]]
- [[md2wechat-AI模式发布流程]]

## 原文链接

- [[raw/sources/src-20260701-wechat-writing-sop/original.md|公众号写作与发布SOP本地证据快照]]

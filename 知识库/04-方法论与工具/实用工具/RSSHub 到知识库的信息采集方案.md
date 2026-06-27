---
title: RSSHub 到知识库的信息采集方案
tags: [RSSHub, 知识库, RAG, 信息采集, 自动化]
created: 2026-06-26
updated: 2026-06-27
source_level: none
source_id: src-20260626-local-rsshub-knowledge-ingest-a8843ce1
raw_path: raw/sources/src-20260626-local-rsshub-knowledge-ingest-a8843ce1/original.md
raw_sha256: A8843CE1180DDA6FFA3C773726EEAB9EA0B5E0AAEEDEB94C54DB74138C956DF8
canonical_url:
sources:
  - raw/sources/src-20260626-local-rsshub-knowledge-ingest-a8843ce1/original.md
  - 知识库/sources/src-20260626-local-rsshub-knowledge-ingest-a8843ce1.md
---
# RSSHub 到知识库的信息采集方案

## 定位

RSSHub 更适合作为信息采集层，而不是知识库存储层。推荐链路是：

```text
RSSHub 路由/订阅源
  -> 定时拉取 RSS/Atom
  -> 清洗、去重、补全文
  -> 写入知识库或向量库
  -> AI 检索问答、每日摘要、专题追踪
```

在这个分层里，RSSHub 负责把 Telegram、GitHub、B 站、知乎、媒体站点等来源转成 RSS/Atom；知识库负责长期存储、结构化沉淀、索引和问答。

## 推荐落地顺序

1. 先用公共 RSSHub 实例验证 3-5 个订阅源是否有价值。
2. 确认价值后自部署 RSSHub，保证稳定性、访问控制、缓存和私有订阅可控。
3. 给订阅源加 `filter`、`filterout`、`limit`、`filter_time`、`mode=fulltext` 等参数，在入库前先降噪。
4. 用定时脚本拉取 RSSHub 输出，做去重、正文抽取和字段规范化。
5. 按“标题、来源、链接、发布时间、抓取时间、正文、标签”写入知识库。
6. 由知识库应用或向量库提供 RAG 问答、每日摘要和专题追踪。

## 自部署要点

原文建议长期配合知识库时优先自部署 RSSHub，原因是公共实例不适合承载私密订阅、登录态 Cookie、访问密钥和高稳定性需求。

最小部署形态：

```bash
wget https://raw.githubusercontent.com/DIYgod/RSSHub/master/docker-compose.yml
docker compose up -d
```

常见配置关注点：

| 配置项 | 作用 |
|---|---|
| `NODE_ENV=production` | 生产模式 |
| `CACHE_TYPE=redis` | 使用 Redis 缓存 |
| `CACHE_EXPIRE=600` | 控制缓存过期时间 |
| `ACCESS_KEY` | 访问控制，避免公开滥用 |
| 代理配置 | 支撑需要特殊网络访问的源 |
| 第三方平台凭证 | 支撑 GitHub、YouTube、Telegram、Twitter/X 等受限路由 |

> 证据边界：这些配置来自本次附件原文整理，部署前需要按 RSSHub 官方文档二次核验最新参数和镜像要求。

## 订阅源设计

RSSHub URL 通常由实例域名和路由参数组成：

```text
https://你的-rsshub-实例域名/路由/参数
```

对知识库更有用的通用参数：

| 参数 | 用途 |
|---|---|
| `limit=20` | 限制每次拉取条数 |
| `filter=AI|大模型|RAG` | 仅保留关键词相关内容 |
| `filterout=广告|抽奖` | 排除低价值内容 |
| `filter_time=86400` | 只取最近 24 小时内容 |
| `mode=fulltext` | 尝试提取全文 |

示例订阅源：

```text
https://你的-rsshub实例/github/release/langgenius/dify?limit=10
https://你的-rsshub实例/bilibili/user/video/用户ID?filter=AI|大模型&limit=20
https://你的-rsshub实例/telegram/channel/频道名?filter_time=86400
```

## 入库方式对比

| 方式 | 适合场景 | 边界 |
|---|---|---|
| Dify 工作流实时读取 | “今天有什么新内容”这类即时问答 | 不等于长期知识沉淀 |
| 定时写入 Dify Knowledge | 需要 RAG 检索、文档管理、自动索引 | 需要处理 API Key、数据集 ID、异步索引状态 |
| 写入本地 Markdown 知识库 | Obsidian、Logseq、Quartz、MkDocs、AnythingLLM 本地目录 | 需要自己维护去重、文件命名、frontmatter 和索引 |

本知识库更匹配第三种：RSSHub 只做采集入口，脚本将条目保存为 Markdown，再由 Obsidian/本地检索/向量库消费。

## Markdown 入库格式

建议每条 RSS 条目保存为一个可追踪 Markdown 文档：

```markdown
---
source: RSSHub
feed: GitHub Releases
url: https://example.com/article
published: 2026-06-26
captured: 2026-06-26
tags:
  - rss
  - ai
  - 自动入库
---

# 标题

正文内容……
```

对当前仓库，应进一步补齐：

- `source_id`
- `raw_path`
- `raw_sha256`
- `canonical_url`
- 影响的知识页
- 待验证项

## 知识库分层

不要把所有 RSS 条目放进一个库。建议按用途分层：

| 分库 | 内容范围 |
|---|---|
| RSS-AI动态库 | AI 新闻、论文、产品更新 |
| RSS-技术发布库 | GitHub Release、框架更新、开源项目 |
| RSS-商业情报库 | 竞品博客、行业媒体、公司公告 |
| RSS-个人关注库 | 公众号、博客、社交平台 |

后续可支持的问题：

- 最近 7 天 Dify、LangChain、OpenAI 有什么重要更新？
- 今天 AI Agent 相关内容按产品、论文、融资如何分类？
- 关注的 GitHub 项目最近有哪些破坏性变更？

## 风险与边界

- 不要把 RSSHub 抓取频率设得过高；普通信息源可按 30 分钟到 2 小时，同步价值高的快讯源再缩短到 5 到 15 分钟。
- 需要登录态、Cookie、Token 的源应使用自部署实例，不应放在不可信公共实例。
- 入库侧必须去重，否则 RSS 条目更新会反复写入重复文档。
- RSSHub 的全文提取不等于稳定高质量正文，入库前应保留原文链接和抓取时间。
- Dify/FastGPT/AnythingLLM 这类平台的 API 参数可能变化，自动写入前必须用最小样本验证。

## 验证清单

- RSSHub 实例首页可访问。
- 目标订阅源返回合法 RSS/Atom。
- `filter`、`filterout`、`limit`、`filter_time` 参数符合预期。
- 同一条目重复运行不会二次入库。
- Markdown 文件包含标题、原文链接、来源、发布时间、抓取时间和正文。
- source_id、raw_path、raw_sha256 可回溯。
- 知识库或向量库能检索到新条目。
- 问答结果能引用到原文链接或来源页。
- 失败日志能区分拉取失败、解析失败、入库失败和索引失败。

## 相关页面

- [[agent-llm-wiki模式]]
- [[知识库/sources/src-20260626-local-rsshub-knowledge-ingest-a8843ce1|RSSHub 到知识库的信息采集方案（来源页）]]

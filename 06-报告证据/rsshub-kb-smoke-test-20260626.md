# RSSHub 与知识库配合使用冒烟验证

## 执行信息

- 执行时间：2026-06-26 12:37:40 +08:00
- 知识库根目录：`D:\Docs\Books\my second brain`
- RSSHub 测试容器：`rsshub-kb-test`
- 本地访问地址：`http://127.0.0.1:1200`
- 测试产物目录：`tmp/rsshub-kb-smoke-20260626-123740`

## 验证目标

验证 RSSHub 是否能作为信息采集层，与当前 Obsidian/LLM Wiki 知识库的存储规范配合：

```text
RSSHub 路由
  -> RSS/XML
  -> 解析 item
  -> 生成带 frontmatter 的 Markdown
  -> 保留 source_id/raw_path/raw_sha256
```

## 启动证据

启动命令：

```powershell
docker run -d --name rsshub-kb-test -p 127.0.0.1:1200:1200 -e NODE_ENV=production diygod/rsshub
```

容器状态：

```text
rsshub-kb-test   diygod/rsshub   127.0.0.1:1200->1200/tcp   Up
```

容器日志关键行：

```text
RSSHub is running on port 1200
Local: http://localhost:1200
```

首页访问结果：

```text
GET http://127.0.0.1:1200/ -> 200
```

## 路由验证

| 路由 | 结果 | 证据 |
|---|---|---|
| `https://rsshub.app/github/release/DIYgod/RSSHub?limit=1` | 失败 | 公共实例返回 Cloudflare challenge，不适合直接作为自动化依赖 |
| `http://127.0.0.1:1200/github/release/DIYgod/RSSHub?limit=1` | 失败 | 503，RSSHub 报 `NotFoundError` |
| `http://127.0.0.1:1200/github/trending/daily/any?limit=1` | 失败 | 503 |
| `http://127.0.0.1:1200/github/issue/DIYgod/RSSHub?limit=1` | 通过 | 200，`application/xml; charset=utf-8` |
| `http://127.0.0.1:1200/rsshub/routes?limit=1` | 通过 | 200，`application/xml; charset=utf-8` |

## 入库样本验证

使用可用路由：

```text
http://127.0.0.1:1200/github/issue/DIYgod/RSSHub?limit=1
```

解析到的 RSS item：

```text
title: Support Pawchive.st
link: https://github.com/DIYgod/RSSHub/issues/22339
published: Thu, 25 Jun 2026 19:25:33 GMT
```

生成的样本文件：

```text
tmp/rsshub-kb-smoke-20260626-123740/kb-sample.md
```

样本 frontmatter 包含：

```yaml
source: RSSHub
source_id: smoke-20260626-123740
feed: GitHub Issues - DIYgod/RSSHub
url: https://github.com/DIYgod/RSSHub/issues/22339
published: Thu, 25 Jun 2026 19:25:33 GMT
captured: 2026-06-26T12:37:40+08:00
raw_path: tmp/rsshub-kb-smoke-20260626-123740/rsshub.xml
raw_sha256: 2D23AA25AB223C54D5CE3807CF8F118857D07CB47AC936343461C7CCF622E7BA
```

校验结果：

```text
rss_status: 200
rss_content_type: application/xml; charset=utf-8
frontmatter_ok: true
raw_path_ok: true
raw_sha256: 2D23AA25AB223C54D5CE3807CF8F118857D07CB47AC936343461C7CCF622E7BA
```

## 阶段性结论

当前可以证明：

- RSSHub 本地实例能成功启动。
- 至少部分 RSSHub 路由能返回合法 XML。
- 返回的 RSS item 可以被转换为当前知识库兼容的 Markdown frontmatter。
- `source_id/raw_path/raw_sha256` 这条可追踪链路可以跑通。

当前不能证明：

- 所有目标订阅源都可用。
- GitHub release/trending 路由在当前镜像和网络条件下可用。
- 生成内容已达到正式知识页质量。
- 该链路已经具备生产级去重、清洗、失败重试和安全控制。

因此，结论是：**RSSHub 可以和当前知识库配合使用，但现在只通过了信息采集到 Markdown 样本的最小闭环；正式自动入库前还需要做路由白名单、去重库、正文清洗和失败报告。**

## 后续验证项

- 确认计划订阅的 RSSHub 路由清单，并逐个验证 200/XML。
- 为每条入库记录生成稳定 `source_id`，避免 title 变化导致重复。
- 增加 SQLite 去重表或等价状态文件。
- 对 HTML 描述字段做 Markdown 清洗，避免正文直接保留大量 HTML。
- 决定正式落点：`00-收件箱/` 暂存、`raw/sources/` 原文归档、还是直接进入 `知识库/sources/`。
- 若长期运行，给 RSSHub 增加 Redis 缓存、访问密钥和定时任务日志。

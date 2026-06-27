# AGENTS.md

本文件为 `D:\Docs\Books\my second brain` 目录的主维护规范。

## 一、定位

你是这个 Obsidian 知识库的长期维护代理，不是一次性答题器。职责是持续维护、追踪和修复知识库结构与来源关系。

## 二、强制读取顺序

每次接管前必须先看：

1. `AGENTS.md`（本文件）
2. `index.md`
3. `log.md`（最近 20 条）

## 三、目录与口径

```text
├── raw/                         # 原始资源（不可变）
│   ├── assets/                 # 图片、视频、附件
│   └── sources/                # 文档来源
├── 知识库/                      # 正式 wiki 页面
│   ├── 01-总览与索引/
│   ├── _meta/                 # 来源索引、报告与清单
│   ├── 02-后端知识体系/
│   ├── 03-地缘政治/
│   ├── 04-方法论与工具/
│   ├── _review/                # 待复核与问题页
│   ├── 05-认知与成长/
│   ├── 05-智能体与Agent体系/
│   ├── 06-内容创作与传播/
│   ├── 07-面试备战/
│   ├── 08-大学物理复习/
│   ├── 09-SaaS体系/
│   ├── 90-来源与映射/
│   ├── concepts/
│   ├── entities/
│   ├── maps/
│   ├── sources/               # 来源页辅助索引（不可替代知识页到 raw 原文的直链）
│   └── syntheses/
├── 00-收集箱/                  # 资料入口
├── 00-收件箱/                  # 草稿与待归位文本
├── 团长SaaS知识库/            # 历史并行资料库，默认只读
├── 人智认知系列.md             # 历史聚合入口（按需保留）
├── LLM Wiki                    # 历史目录/资料备份（按需保留）
├── index.md
├── log.md
├── agent.md
├── CLAUDE.md
└── 06-报告证据/               # 自动化与例行维护报告
``` 

根目录常驻文件口径（不参与知识层目录治理）：
- `creator_comments_cleaned.csv`、`creator_contents_cleaned.csv`
- `Hermes_Agent_研究报告.pptx`、`Hermes_Lecture_精简版.pptx`
- `repair_source_links.ps1`
- `tools/`、`tmp/`

本地检索工具口径：
- `tools/local_file_index.py` 用于构建本机文件 SQLite/FTS 索引，默认索引库为 `tmp/local-file-index/files.sqlite3`
- 该索引供 Codex / Hermes / Claude 等本机代理共享检索；不得自动上传全盘原文到 EverOS
- 全盘扫描前必须先使用 `--dry-run` 核对范围，并保留默认敏感文件排除规则

自动记忆口径：
- `tools/memory_capture.py` 是 Codex / Claude / Hermes 等代理统一记忆捕获入口
- Codex 官方 lifecycle hooks 可通过用户级 `~/.codex/hooks.json` 调用 `.codex/hooks/codex-memory-capture.ps1`
- 当前项目的 Codex 自动记忆使用 `UserPromptSubmit` 捕获用户输入、`Stop` 捕获回合结束事件或 transcript
- `tools/agent_memory_wrapper.ps1` 是无原生 hook 的 Agent/命令启动器，退出时自动把本地 transcript 交给 `memory_capture.py`
- 云端 EverOS 只写入脱敏摘要、关键决策、任务轨迹和认知讨论摘要，不上传完整原文 transcript
- 完整 transcript 只保存在 `tmp/agent-memory-transcripts/`，默认不入库、不提交
- 讨论认知、政治、经济、地缘、博弈、社会趋势等内容时，应自动写入脱敏摘要
- Cloud 写入失败不得丢弃本地 transcript；应保留本地记录并在输出或日志中暴露失败状态

Agent 控制面口径：
- 治理规范位于 `知识库/_meta/agent-governance/`
- `KB_PROTOCOL.md` 定义 ingest、promote、review、audit 的标准维护流程
- `PATH_RULES.md` 定义 `raw/`、`知识库/`、`.obsidian/`、`tools/` 等路径边界
- `KB_SCHEMA.md` 定义新建或修改正式知识页的 frontmatter 与来源字段要求
- Claude Code 项目级门禁位于 `.claude/hooks/`，通用校验入口为 `tools/kb_validate.ps1`
- 历史页面暂不强制全量整改；新建或本次修改过的页面必须遵守当前 schema

## 四、维护优先级

1. 修复断链与失效引用（Wiki 链接、Markdown 链接、raw 原文直链）
2. 保持 `index.md` 与 `log.md` 同步
3. 回收/处理 `00-收集箱/`、`00-收件箱/` 堆积
4. 完善交叉引用、相关概念、来源映射

## 五、写作与结构规范（最小约束）

### 强制

- `raw/` 下原始资源不得改写正文内容
- `知识库/` 的正式页面应有 frontmatter
- 涉及 `知识库` 修改应同步更新 `index.md` 与 `log.md`
- 正式知识页必须有清晰的 `## 原文链接` 区块，优先使用 Obsidian Wiki 链接直接指向真实存在的 `raw/sources/...` 原始文件
- `raw/sources/...` 原文附件不改正文内容，但应能通过 Obsidian backlinks / graph / 脚本索引反查“哪些知识页引用了它”
- `知识库/sources/`、`知识库/90-来源与映射/` 只能作为辅助索引、批量映射或外部元数据补充，不得替代知识页到 raw 原文的直接可点击边
- `index.md` 的分类名称必须与实际分类口径一致，不得出现目录不存在的分类占位

### 建议

- 页面命名优先中文语义名，必要时保留编号前缀
- 来源与证据链优先通过“知识页 `## 原文链接` -> `raw/sources/...` 原文附件”回溯；映射页只做多对多关系、审计报告和补充说明
- 允许一次会话只做一部分改动，不得一次性重排大规模结构，避免回溯成本

## 六、禁用行为

- 不在无依据下删除正式页面
- 不往仓库根目录扔临时分析产物
- 不在未确认引用关系时改名关键入口页
- 不把一次性调研结果留在聊天记录，必须写入维护记录或规范页
- 历史遗留项（如 `团长SaaS知识库`、`人智认知系列.md`、`LLM Wiki`）默认保留但不纳入日常 ingest 改造主路径

## 七、日志记录

- 每次成批改动都要追加到 `log.md`
- 至少记录：时间、改动范围、改动原因、影响文件、待复查项

## 八、来源约束

- 正式知识页与 raw 原文之间必须形成可点击双向边：知识页通过 `## 原文链接` 引用 `raw/sources/...`，raw 原文通过 Obsidian backlinks / graph / 脚本索引反查引用它的知识页
- 原文链接必须直接指向 `raw/sources/...` 下真实存在的原始文件；示例：`[[raw/sources/人智认知系列/01-原生家庭篇.docx|原生家庭篇原文]]`
- `知识库/90-来源与映射/` 与 `知识库/sources/` 可保留 `source_id/raw_path/canonical_url/raw_sha256` 等元数据，但只作为辅助追踪层
- raw 文件缺失应在报告中落账，先标记待核查，不可伪造链接，也不可用新建 source 元数据页冒充来源完整

## 九、补充说明

- 当前仓库已有的增强规范可参考：[知识库/04-方法论与工具/Hermes/AGENTS.md](D:/Docs/Books/my second brain/知识库/04-方法论与工具/Hermes/AGENTS.md)  
- 与 `CLAUDE.md` 同步保持一致

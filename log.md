# log.md

## [YYYY-MM-DD] lint | 日志
- 按任务创建时系统自动写入占位条目
## [2026-06-24] lint | 每日知识库维护

- 执行脚本: daily_kb_maintenance.ps1
- 执行时间: 22:22:39
- 知识页扫描数: 772
- 缺失 WikiLink: 1914
- 缺失 Markdown 链接: 13
- 缺失 raw_path: 222
- canonical_url 异常: 4
- frontmatter缺失: 131

## [2026-06-24] lint | 每日知识库维护

- 执行脚本: daily_kb_maintenance.ps1
- 执行时间: 22:22:56
- 知识页扫描数: 772
- 缺失 WikiLink: 1914
- 缺失 Markdown 链接: 13
- 缺失 raw_path: 222
- canonical_url 异常: 4
- frontmatter缺失: 131

## [2026-06-26] report | GitHub 每日热门项目汇总

- 新建 `06-报告证据/latest-github-trending.md` 固定滚动页与 `06-报告证据/报告索引.md`，沉淀 2026-06-26 GitHub Trending 10 个项目证据。
- 同步更新 `index.md` 报告入口；按任务要求尝试执行 `line_guard.py`、`brain_lint.py`、`brain_search.py "GitHub"`，待确认实际脚本路径与可用性。

## [2026-06-26] ingest | RSSHub 到知识库的信息采集方案

- 改动范围：新增 RSSHub 信息采集到知识库/RAG 的正式工具页、来源页和 raw 原文副本。
- 改动原因：用户提供粘贴文本，要求按当前 Obsidian 知识库规则沉淀为可追踪资料。
- 影响文件：`raw/sources/src-20260626-local-rsshub-knowledge-ingest-a8843ce1/original.md`、`知识库/sources/src-20260626-local-rsshub-knowledge-ingest-a8843ce1.md`、`知识库/04-方法论与工具/实用工具/RSSHub 到知识库的信息采集方案.md`、`知识库/04-方法论与工具/index.md`、`知识库/04-方法论与工具/实用工具/index.md`、`知识库/sources/index.md`、`index.md`。
- 待复查项：RSSHub 官方 Docker Compose/配置变量、Dify Knowledge API 字段和 RSSHub 通用参数未在本次维护中联网复核；落地自动入库前需要最小样本验证。

## [2026-06-26] lint | 每日知识库维护

- 执行脚本: daily_kb_maintenance.ps1
- 执行时间: 12:33:04
- 知识页扫描数: 774
- 缺失 WikiLink: 1916
- 缺失 Markdown 链接: 13
- 缺失 raw_path: 223
- canonical_url 异常: 5
- frontmatter缺失: 131

## [2026-06-27] review | 人智认知系列原文链接断源登记

- 改动范围：为 `原生家庭篇`、`学习篇`、`认知闭环篇`、`潜意识篇`、`抱猴心理篇` 增加显式 `原文链接` 状态区块，并更新待复核清单与索引更新时间。
- 改动原因：用户确认知识图谱维护口径为“正式知识页可点击到 raw 原文，raw 通过 Obsidian 反向链接/图谱回到知识页”，不再默认要求 `知识库/sources` 中转来源页。
- 影响文件：`知识库/05-认知与成长/01-人智认知系列/原生家庭篇.md`、`知识库/05-认知与成长/01-人智认知系列/学习篇.md`、`知识库/05-认知与成长/01-人智认知系列/认知闭环篇.md`、`知识库/05-认知与成长/01-人智认知系列/潜意识篇.md`、`知识库/05-认知与成长/01-人智认知系列/抱猴心理篇.md`、`知识库/_review/unresolved-items.md`、`index.md`、`log.md`。
- 证据结果：上述 5 篇页面声明的 `raw/sources/人智认知系列/*.docx` 在当前仓库未发现；同名文件全库检索也未命中，因此暂不能建立“知识页 <-> raw 原文”的可点击双向跳转。
- 待复查项：找到或补回对应 raw 原文后，将 `原文缺失待核查` 改为 `[[raw/sources/...|原文]]` 形式的显式链接，并确认 Obsidian backlinks 可从 raw 反查到知识页。

## [2026-06-26] lint | 每日知识库维护

- 执行脚本: daily_kb_maintenance.ps1
- 执行时间: 12:33:34
- 知识页扫描数: 774
- 缺失 WikiLink: 1914
- 缺失 Markdown 链接: 13
- 缺失 raw_path: 223
- canonical_url 异常: 5
- frontmatter缺失: 131

## [2026-06-26] integration | EverOS 记忆层接入

- 改动范围：新增 EverOS Cloud 项目级 CLI、依赖清单、官方文档 raw 副本、来源页、来源映射和正式接入说明页。
- 改动原因：按用户要求将 EverOS 作为 AI Agent 外部记忆层接入本知识库，并保留可追踪 API 文档证据链。
- 影响文件：`.gitignore`、`tools/requirements-everos.txt`、`tools/everos_memory.py`、`raw/sources/src-20260626-everos-llms-full/llms-full.txt`、`知识库/05-智能体与Agent体系/EverOS 记忆层接入方案.md`、`知识库/sources/src-20260626-everos-llms-full.md`、`知识库/90-来源与映射/EverOS官方API文档来源映射.md`、`知识库/sources/index.md`、`知识库/90-来源与映射/index.md`、`index.md`。
- 验证结果：已安装 `everos-cloud 0.4.1`；`python tools/everos_memory.py self-test` 本地自检通过；使用临时进程环境变量完成 Cloud 冒烟，`self-test --live` 认证成功，`add --sync` 返回 `Messages accepted`，`flush` 返回 `extracted`，`search --method hybrid` 检索到测试 episode。
- 待复查项：确认当前账号 quota 和 dashboard memory space；补充哪些维护内容允许进入 EverOS 的脱敏规则。

## [2026-06-26] smoke | RSSHub 与知识库配合使用验证

- 启动本地 RSSHub 容器 `rsshub-kb-test`，绑定 `127.0.0.1:1200`，首页访问 200。
- 公共 `rsshub.app` GitHub release 路由被 Cloudflare challenge 阻断；本地 `/github/release/DIYgod/RSSHub` 与 `/github/trending/daily/any` 返回 503，`/github/issue/DIYgod/RSSHub?limit=1` 返回 200 XML。
- 生成测试产物 `tmp/rsshub-kb-smoke-20260626-123740/kb-sample.md`，frontmatter 与 `raw_path/raw_sha256` 校验通过。
- 新增报告 `06-报告证据/rsshub-kb-smoke-test-20260626.md`，同步更新 `06-报告证据/报告索引.md` 与 `index.md`。
- 阶段性结论：RSSHub 可作为信息采集层配合当前知识库，但正式自动入库前还需要路由白名单、去重、正文清洗、失败报告和访问控制。

## [2026-06-26] integration | 本地全电脑文件检索工具

- 改动范围：新增本地 SQLite/FTS 文件索引 CLI、单元测试、正式工具说明页，并更新索引与 AGENTS 维护口径。
- 改动原因：用户确认希望实现“全电脑可检索”，并允许 Codex 等本机代理读取本地索引。
- 影响文件：`.gitignore`、`AGENTS.md`、`tools/local_file_index.py`、`tests/test_local_file_index.py`、`知识库/04-方法论与工具/实用工具/本地全电脑文件检索方案.md`、`知识库/04-方法论与工具/实用工具/index.md`、`知识库/05-智能体与Agent体系/EverOS 记忆层接入方案.md`、`index.md`、`log.md`。
- 验证结果：`python -m py_compile tools/local_file_index.py` 通过；`python -m unittest discover -s tests` 通过 2 项；`scan --root . --limit 20` 生成本地索引 20 个文件、0 个错误；`search EverOS --format json` 命中 `log.md`、`index.md`、`AGENTS.md`；`show ... --extract` 能抽取 Markdown 正文。
- 待复查项：正式全盘扫描前需先运行 `--preset all-drives --allow-all-drives --dry-run` 核对候选数量；后续可补增量扫描与摘要写入 EverOS 的白名单策略。

## [2026-06-26] test | 本地文件检索工具验证

- 测试范围：本地文件索引 CLI、EverOS CLI 本地自检、敏感信息扫描、常用目录 dry-run、全盘扫描安全开关、小范围索引与检索。
- 测试结果：`py_compile` 通过；`python -m unittest discover -s tests -v` 通过 2 项；`python tools/everos_memory.py self-test` 通过且当前 shell 未设置 API Key；`scan --preset common --dry-run` 识别常用目录候选文件 88648 个；`scan --root . --limit 50` 成功索引 50 个文件、0 错误。
- 全盘保护：`scan --preset all-drives --dry-run` 被正确拒绝，提示必须添加 `--allow-all-drives`；`scan --preset all-drives --allow-all-drives --dry-run --limit 1000` 成功识别 `C:\` 与 `D:\` 两个根。
- 检索验证：补扫 `知识库/04-方法论与工具/实用工具` 与 `知识库/05-智能体与Agent体系` 后，`search "本地全电脑文件检索"` 命中正式说明页，`search "EverOS 记忆层"` 命中 EverOS 接入方案页；`stats` 显示当前本地索引 58 个文件、0 错误。
- 安全检查：完整 EverOS API Key、私钥头和明显 `EVEROS_API_KEY=...` 模式扫描无命中；`git diff --check` 无 whitespace 错误，仅有 CRLF/LF 换行提示。

## [2026-06-26] integration | EverOS OSS 本地长期记忆服务

- 改动范围：读取用户附件并保存 raw 副本，联网核验 EverOS 官方 GitHub 文档，新增 OSS 本地长期记忆方案页、来源页、来源映射和本地 HTTP 桥接脚本。
- 改动原因：附件建议将 EverOS 作为本地长期记忆服务，和当前 Cloud SDK 接入属于不同 API 形态，需要分层落地。
- 影响文件：`.gitignore`、`tools/everos_local_memory.py`、`tests/test_everos_local_memory.py`、`raw/sources/src-20260626-local-everos-oss-memory-service/original.md`、`知识库/05-智能体与Agent体系/EverOS 本地长期记忆服务方案.md`、`知识库/sources/src-20260626-local-everos-oss-memory-service.md`、`知识库/90-来源与映射/EverOS本地长期记忆服务来源映射.md`、`知识库/sources/index.md`、`知识库/90-来源与映射/index.md`、`index.md`、`log.md`。
- 证据结论：官方文档确认 OSS API 为 `/api/v1/memory/*`，默认 `127.0.0.1:8000` 且无内置鉴权，Markdown 是 source of truth，SQLite/LanceDB 是可重建索引；当前本机 `everos 0.4.0` 包存在但无 CLI/server，`where everos` 未找到命令。
- 本地端口证据：`http://127.0.0.1:8000/health` 可访问，但 `/openapi.json` 显示当前服务为 `Smart Campus Voice Demo Backend`，不包含 `/api/v1/memory/*` 路由；`tools/everos_local_memory.py add` 调用 `/api/v1/memory/add` 返回 404。
- 验证结果：`py_compile` 通过；`python -m unittest discover -s tests -v` 通过 6 项；`tools/everos_local_memory.py health --soft` 返回 `everos_memory_api=false`；`health --require-memory-api` 正确以 exit 2 失败；附件 raw 副本 SHA256 校验一致。
- 待复查项：安装真正的 EverOS OSS server 后执行 `health --require-memory-api -> add -> flush -> search` 端到端验证；如 8000 被占用，需换端口并设置 `EVEROS_LOCAL_BASE_URL`；配置模型 provider 时不得提交 `everos.toml`、`.env` 或 `.everos/`。

## [2026-06-26] config | EverOS Cloud 用户级环境变量接入

- 改动范围：将 EverOS API Key 设置为 Windows 当前用户级环境变量，并增强 `tools/everos_memory.py` 的环境变量读取逻辑。
- 改动原因：用户选择让 EverOS Cloud 对 Codex 等本机代理全局可读；当前 Codex 进程无法自动继承新写入的用户级环境变量，需要脚本从 HKCU 用户环境兜底读取。
- 影响文件：`tools/everos_memory.py`、`tests/test_everos_memory.py`、`log.md`。
- 验证结果：用户级 `EVEROS_API_KEY` 已存在且长度为 36；当前进程环境未继承该变量；脚本通过用户级环境 fallback 后 `self-test --live` 可访问 EverOS Cloud。
- 待复查项：重启 Codex 后再执行一次不带 fallback 前缀的 live 自检，确认新进程是否已直接继承用户级环境变量。

## [2026-06-26] report | GitHub 热门项目滚动日报刷新

- 改动范围：更新 `06-报告证据/latest-github-trending.md` 的今日热门项目、来源证据、风险项与后续观察，并保留固定滚动页结构。
- 改动原因：旧日报项目列表与当日 GitHub Trending Daily 快照不一致，需要按最新榜单重写并显式记账路径/规范缺失项。
- 验证结果：`latest-github-trending.md` 当前 44 行，满足单文件 200 行限制；按任务要求执行 `python 第二大脑/07-脚本/line_guard.py`、`brain_lint.py`、`brain_search.py "GitHub"`，三者均因目标路径不存在而失败，当前无法完成知识库验证闭环。

## [2026-06-27] lint | 每日知识库维护

- 执行脚本: daily_kb_maintenance.ps1
- 执行时间: 11:11:41
- 知识页扫描数: 781
- 缺失 WikiLink: 1914
- 缺失 Markdown 链接: 13
- 缺失 raw_path: 225
- canonical_url 异常: 6
- frontmatter缺失: 131

## [2026-06-27] governance | Agent 控制面 MVP

- 改动范围：新增 `知识库/_meta/agent-governance/` 三个治理文档，补充 Claude Code hooks 与通用校验脚本入口，并更新跨 Agent 入口说明。
- 改动原因：按用户要求把 `AGENTS.md` 软规范升级为“治理文档 + 项目级 hooks + 通用校验脚本 + 审计日志”的最小可用控制面。
- 影响文件：`.gitignore`、`AGENTS.md`、`CLAUDE.md`、`index.md`、`log.md`、`.claude/settings.json`、`.claude/hooks/kb-pretooluse.ps1`、`.claude/hooks/kb-stop.ps1`、`tools/kb_validate.ps1`、`知识库/_meta/agent-governance/KB_PROTOCOL.md`、`知识库/_meta/agent-governance/PATH_RULES.md`、`知识库/_meta/agent-governance/KB_SCHEMA.md`。
- 验证结果：`.claude/settings.json` JSON 解析通过；`tools/kb_validate.ps1 -ChangedOnly` 通过，提示两个 `05-*` 目录为预期警告；`.claude/hooks/kb-stop.ps1` 通过；PreToolUse 模拟测试中 `.obsidian` Edit、`raw/` Edit、破坏性 Bash 均以 exit 2 阻断，普通 Read 以 exit 0 放行。
- 待复查项：本次不实施 Cursor rules、Claude skills/subagents、MCP server，也不修复历史断链、raw_path 和旧 frontmatter 问题。

## [2026-06-27] integration | 跨 Agent 自动记忆捕获入口

- 改动范围：新增统一记忆捕获脚本、通用 Agent 启动器与测试，更新 Claude Stop hook、`.gitignore`、AGENTS/CLAUDE 口径。
- 改动原因：用户要求 Codex、Claude、Hermes 等智能体在当前项目中实现自动记忆；确认策略为云端 EverOS 只写脱敏摘要，本地 `tmp/agent-memory-transcripts/` 保存完整 transcript 且不入库。
- 影响文件：`tools/memory_capture.py`、`tools/agent_memory_wrapper.ps1`、`tests/test_memory_capture.py`、`.claude/hooks/kb-stop.ps1`、`tools/kb_validate.ps1`、`.gitignore`、`AGENTS.md`、`CLAUDE.md`、`log.md`。
- 验证结果：`py_compile` 通过；`python -m unittest discover -s tests -v` 通过 12 项；dry-run 捕获在 `tmp/agent-memory-transcripts/` 写入本地 transcript；Cloud 捕获 `cloud-smoke-20260627` 写入成功并可搜索；`tools/agent_memory_wrapper.ps1 -NoCloud -CommandLine "echo ..."` 冒烟通过；敏感信息扫描无命中；`tools/kb_validate.ps1 -ChangedOnly` 通过。
- 验证边界：`tools/kb_validate.ps1` 全量扫描已修复 PowerShell `GetRelativePath` 兼容错误，但仍因历史页面缺少 frontmatter/source 字段失败；该历史债务非本次自动记忆改动引入。
- 待复查项：Codex 原生桌面会话仍需要宿主或 `tools/agent_memory_wrapper.ps1` 提供 transcript；Claude Stop hook 可 best-effort 捕获 hook 输入和 transcript_path；Hermes 需通过同一 wrapper 启动后才能做到自动。

## [2026-06-27] integration | Codex 官方 hooks 自动记忆

- 改动范围：按 Codex 官方 hooks 文档新增 `.codex/hooks/codex-memory-capture.ps1`，扩展 `tools/memory_capture.py` 解析 `codex-hook-json`，并将用户级 `~/.codex/hooks.json` 合并出 Codex `UserPromptSubmit` 与 `Stop` 记忆入口。
- 改动原因：用户要求确认并落实 Codex hook 自动调用，避免依赖手动执行 wrapper。
- 影响文件：`.codex/hooks/codex-memory-capture.ps1`、`tools/memory_capture.py`、`tests/test_memory_capture.py`、`AGENTS.md`、`CLAUDE.md`、`log.md`、用户级 `C:\Users\caojianing\.codex\hooks.json`。
- 验证结果：`hooks.json` JSON 解析通过；`python -m unittest discover -s tests -v` 通过 14 项；Codex hook 脚本本地 `UserPromptSubmit -NoCloud` 冒烟通过；项目外 cwd 事件会跳过；真实 Cloud 写入 `codex-hook-cloud-smoke-20260627` 成功并可通过 EverOS search/get 检索。
- 验证边界：Codex 新 hook 需要在 Codex `/hooks` 中由用户信任后才会由宿主自动执行；本轮已验证脚本与 Cloud 链路，不能在当前回答内替代宿主信任确认。

## [2026-06-27] fix | Codex UserPromptSubmit 捕获范围收窄

- 改动范围：调整 `tools/memory_capture.py` 的 `codex-hook-json` 解析顺序，`UserPromptSubmit` 优先捕获本次 `prompt`，不再优先读取整段 `transcript_path`；补充对应单元测试。
- 改动原因：用户信任 hook 后的实测记录显示 Codex `UserPromptSubmit` 事件同时携带 `prompt` 与 `transcript_path`，旧逻辑优先读取完整 session transcript，导致本地记录过大且云端摘要不够聚焦。
- 影响文件：`tools/memory_capture.py`、`tests/test_memory_capture.py`、`log.md`。
- 验证结果：`python -m unittest discover -s tests -v` 通过 15 项；带 `prompt + transcript_path` 的 `UserPromptSubmit -NoCloud` 冒烟只写入 66 字 prompt；修正后真实 Cloud 写入 `codex-hook-corrected-cloud-smoke-20260627` 成功，metadata 显示 `char_count=92`、`cognitive_required=true`、`cloud_written=true`，EverOS profile 检索包含该 marker。

## [2026-06-27] governance | raw 原文直链来源口径

- 改动范围：将知识库来源完整性口径从“source 元数据页中转”调整为“正式知识页 `## 原文链接` 直接链接 `raw/sources/...` 原文附件”，并要求 Obsidian backlinks / graph / 脚本索引能反查引用关系。
- 改动原因：用户明确要求维护的是知识页与 raw 原文之间的可点击双向边，不得用 `知识库/sources/` 元数据页替代来源完整性。
- 影响文件：`AGENTS.md`、`CLAUDE.md`、`agent.md`、`index.md`、`.claude/hooks/kb-pretooluse.ps1`、`tools/kb_validate.ps1`、`tools/daily_kb_maintenance.ps1`、`tools/kb_full_distill.py`、`知识库/_meta/agent-governance/KB_PROTOCOL.md`、`知识库/_meta/agent-governance/PATH_RULES.md`、`知识库/_meta/agent-governance/KB_SCHEMA.md`、`log.md`。
- 验证结果：PowerShell Parser 解析 `tools/kb_validate.ps1`、`tools/daily_kb_maintenance.ps1`、`.claude/hooks/kb-pretooluse.ps1` 通过；`python -m py_compile tools/kb_full_distill.py` 通过；`tools/kb_validate.ps1 -ChangedOnly` 通过 13 个变更文件，仅提示两个 `05-*` 目录为既有设计警告；直接运行 `python tools/kb_full_distill.py` 会按预期阻断旧 source 页批量迁移，需显式 `--legacy-source-pages` 才能运行。
- 待复查项：当前 `raw/sources/人智认知系列` 目录不存在，已抽查到 `原生家庭篇`、`学习篇` 等页面的 raw 原文链接仍无法命中；后续需按真实 raw 文件恢复或落账为缺失，不能通过新建 source 页冒充修复。

## [2026-06-27] lint | ÿ��֪ʶ��ά��

- ִ�нű�: daily_kb_maintenance.ps1
- ִ��ʱ��: 15:20:32
- ֪ʶҳɨ����: 784
- ȱʧ WikiLink: 1394
- ȱʧ Markdown ����: 13
- ԭ����������ȱʧ: 0
- raw ԭ��Ŀ��ȱʧ: 0
- canonical_url �쳣: 6
- frontmatterȱʧ: 0

## [2026-06-27] lint | ÿ��֪ʶ��ά��

- ִ�нű�: daily_kb_maintenance.ps1
- ִ��ʱ��: 15:23:10
- ֪ʶҳɨ����: 784
- ȱʧ WikiLink: 985
- ȱʧ Markdown ����: 1
- ԭ����������ȱʧ: 0
- raw ԭ��Ŀ��ȱʧ: 0
- canonical_url �쳣: 0
- frontmatterȱʧ: 0

## [2026-06-27] lint | ÿ��֪ʶ��ά��

- ִ�нű�: daily_kb_maintenance.ps1
- ִ��ʱ��: 15:24:39
- ֪ʶҳɨ����: 784
- ȱʧ WikiLink: 893
- ȱʧ Markdown ����: 1
- ԭ����������ȱʧ: 0
- raw ԭ��Ŀ��ȱʧ: 0
- canonical_url �쳣: 0
- frontmatterȱʧ: 0

## [2026-06-27] lint | ÿ��֪ʶ��ά��

- ִ�нű�: daily_kb_maintenance.ps1
- ִ��ʱ��: 15:30:37
- ֪ʶҳɨ����: 784
- ȱʧ WikiLink: 14
- ȱʧ Markdown ����: 1
- ԭ����������ȱʧ: 0
- raw ԭ��Ŀ��ȱʧ: 0
- canonical_url �쳣: 0
- frontmatterȱʧ: 0

## [2026-06-27] lint | ÿ��֪ʶ��ά��

- ִ�нű�: daily_kb_maintenance.ps1
- ִ��ʱ��: 15:32:56
- ֪ʶҳɨ����: 785
- ȱʧ WikiLink: 0
- ȱʧ Markdown ����: 0
- ԭ����������ȱʧ: 0
- raw ԭ��Ŀ��ȱʧ: 0
- canonical_url �쳣: 0
- frontmatterȱʧ: 0


## [2026-06-27] repair | 原文链接与全库断链清零

- 改动范围: 知识库正式页原文链接、Akkkk 内容研究路径、SaaS Harness/DDD 历史链接、概念索引、日报巡检脚本
- 改动原因: 统一维护“知识页 -> raw/sources 原文附件”的可点击边，并清理巡检发现的 WikiLink / Markdown 断链
- 关键修复: 784 个知识页已具备 frontmatter 与 `## 原文链接` 或 `source_level: none`；Akkkk 旧入口、尾随反斜杠路径、prompt 附件路径、历史 DDD 旧页引用已修正
- 新增页面: `知识库/concepts/政治经济学.md`
- 巡检结果: `06-报告证据/日报/daily-maintenance-20260627-153256.md`，issues=0，wikiLinks=0，mdLinks=0，rawMissing=0，originalSections=0
- 验证结果: `tools/kb_validate.ps1` 通过 1026 个文件，仅保留项目约定警告“两组 05-* 目录并存”；`python -m unittest discover -s tests -v` 15 项通过；Python 工具 py_compile 通过；`git diff --check` 无空白错误，仅有 Git 换行提示
- 待复查项: 无来源链路待修；后续若新增正式知识页，必须继续直接链接 `raw/sources/...` 原始附件，不再补造中间 source 元数据页

## [2026-06-27] maintenance | 清空收集箱与收件箱暂存副本

- 改动范围: `00-收集箱/`、`00-收件箱/`、来源映射页、来源页、内容盘点、待复核清单、学习地图
- 改动原因: 已整理条目的原始证据均已落到 `raw/sources/...`，正式知识页和来源映射已改为直接指向 raw 原文，收集箱/收件箱不再保留重复暂存副本
- 关键修复: 清理 5 个已归档/已整理暂存文件；移除待复核清单中的旧重复候选；将内容盘点中的 raw 反查关系改为来源页或真实 raw 原文
- 验证结果: `00-收集箱` 与 `00-收件箱` 当前均为 0 个文件；当前维护文件中无指向已删除暂存文件的 WikiLink 或具体路径引用
- 待复查项: 历史日志和历史报告中保留的旧路径仅作为历史记录，不作为当前入口
## [2026-06-27] lint | ÿ��֪ʶ��ά��

- ִ�нű�: daily_kb_maintenance.ps1
- ִ��ʱ��: 15:42:41
- ֪ʶҳɨ����: 785
- ȱʧ WikiLink: 0
- ȱʧ Markdown ����: 0
- ԭ����������ȱʧ: 0
- raw ԭ��Ŀ��ȱʧ: 0
- canonical_url �쳣: 0
- frontmatterȱʧ: 0

## [2026-06-27] maintenance | 清理残留收集箱挂载源

- 改动范围: `知识库/02-后端知识体系/02-计算机基础/JVM、JDK 与 JRE.md`、`知识库/90-来源与映射/Akkkk抖音数据集来源映射.md`
- 改动原因: 上述文件仍残留已清理收集箱入口，存在潜在来源链不一致
- 关键修复: 将 JVM 页的 `sources` 置空（无残留入口）；Akkkk 映射页去除 `00-收集箱/未命名.md` 引用，保留 CSV 与映射关系为准的来源声明
- 结果: 残留收集箱路径从活跃知识链路里降到仅历史记录和治理说明中的历史叙述
## [2026-06-28] lint | ÿ��֪ʶ��ά��

- ִ�нű�: daily_kb_maintenance.ps1
- ִ��ʱ��: 11:32:16
- ֪ʶҳɨ����: 785
- ȱʧ WikiLink: 0
- ȱʧ Markdown ����: 0
- ԭ����������ȱʧ: 0
- raw ԭ��Ŀ��ȱʧ: 0
- canonical_url �쳣: 0
- frontmatterȱʧ: 0

## [2026-06-28] maintenance | 元数据快照纠偏

- 改动范围: 知识库/_meta/migration-plan.md、知识库/_meta/distillation-log.md、知识库/_review/unresolved-items.md
- 改动原因: 全库校验已通过，但元数据清单仍保留一批已移除的 第二大脑* 历史路径，继续按旧快照处理会误导后续来源整理
- 关键结论: 当前适合做的是“元数据纠偏”而不是“重跑旧来源迁移脚本”；本轮不处理新来源，不批量重写 知识库/sources/src-*.md
- 验证结果: 	ools/kb_validate.ps1 通过；	ools/daily_kb_maintenance.ps1 输出 issues=0、wikiLinks=0、mdLinks=0、awMissing=0、originalSections=0
- 待复查项: 后续需单开批次刷新 content-inventory.md 历史快照，并决定是否保留 第二大脑* 旧路径作为审计记录
## [2026-06-29] automation | GitHub 热门项目滚动日报更新

- 改动范围: 06-报告证据/latest-github-trending.md、06-报告证据/报告索引.md、index.md
- 改动原因: 按 GitHub Trending Daily 与 Repository API 更新最近 24 小时热门项目滚动页，并同步索引日期
- 验证结果: 待执行指定命令校验 latest-github-trending.md 行数、索引命中与本地文件索引检索
- 补充验证: latest-github-trending.md 共 44 行；index/report 索引命中正常；local_file_index search 在控制台编码容错后通过
## [2026-06-30] maintenance | GitHub 热门观察迁移到知识库

- 改动范围: 知识库/04-方法论与工具/实用工具/GitHub 热门项目滚动观察.md、raw/sources/GitHub Trending/2026-06-29 GitHub Trending Daily 与 Repository API 快照.md、知识库/04-方法论与工具/* 索引、index.md、06-报告证据/报告索引.md
- 改动原因: 用户要求 GitHub 热门项目不再放入报告区，改为按知识库结构沉淀为正式知识页，并保留 raw 来源快照
- 验证结果: 新知识页与 raw 快照已入索引；旧文件 06-报告证据/latest-github-trending.md 已删除；local_file_index 可命中新路径
## [2026-06-30] automation | GitHub 热门项目滚动日报恢复
- 改动范围: 06-报告证据/latest-github-trending.md、06-报告证据/报告索引.md、index.md
- 改动原因: 当前自动化要求仍以固定滚动报告页落盘；虽与 2026-06-30 迁移到知识库页的记录冲突，但本次按实际根目录结构恢复并在报告风险项显式记账
- 验证结果: latest-github-trending.md 40 行；index/report 命中正常；tools/local_file_index.py search GitHub --limit 5 返回命中结果

## [2026-07-01] maintenance | XianyuAutoAgent 部署SOP与启动脚本固化

- 改动范围: `知识库/05-智能体与Agent体系/XianyuAutoAgent MiniMax部署与启动SOP.md`、`raw/sources/src-20260701-xianyuautoagent-minimax-deploy/original.md`、`tools/start_xianyu_autoagent.ps1`、`index.md`
- 改动原因: 用户已完成 XianyuAutoAgent + MiniMax Token Plan + 闲鱼 Cookie 部署并验证自动回复成功，需要沉淀为可复用知识库 SOP，并保证后续启动流程可重复
- 关键修复: 固化本机实测 `https://api.minimaxi.com/v1` 可用、`https://api.minimax.io/v1` 对当前 Token Plan Key 返回 401 的证据；记录 `<think>...</think>` 输出过滤边界；新增无密钥启动脚本，自动检查 `.env`、依赖、MiniMax 连通性和后台启动
- 验证结果: `powershell -NoProfile -ExecutionPolicy Bypass -File tools/start_xianyu_autoagent.ps1 -SkipApiCheck -CheckOnly` 通过，脚本可识别当前 PID 43432 且未重复启动；脚本已改为 ASCII 提示，避免 Windows PowerShell 编码解析失败；`tools/kb_validate.ps1` 通过 1027 个文件，仅保留既有两组 05-* 目录警告；新增/变更文件脱敏扫描通过；`rg` 可命中新 SOP、raw 证据和启动脚本入口
- 待复查项: `.env` 中 `API_KEY` 与 `COOKIES_STR` 不得写入知识库或脚本；若上游项目更新 `XianyuAgent.py`，需复核 `_safe_filter` 中 MiniMax thinking 过滤仍然有效

## [2026-07-01] maintenance | 公众号写作与发布SOP补全

- 改动范围: `知识库/06-内容创作与传播/公众号写作与发布SOP.md`、`raw/sources/src-20260701-wechat-writing-sop/original.md`、`知识库/06-内容创作与传播/内容创作导航中心.md`、`知识库/06-内容创作与传播/index.md`、`index.md`
- 改动原因: 用户要求使用 `$grilling` 按照知识库补充完整公众号写作 SOP；本轮先从知识库、md2wechat 项目和 AI微信公众号项目中补证据，再沉淀正式页面
- 关键修复: 将原有“发布流程”和“内容导航”扩展为完整闭环：选题入池、写作前拷问、证据收集、大纲、初稿、人工改稿、metadata、AI/API 排版、草稿创建、手机预览、发布和复盘
- 验证结果: `tools/kb_validate.ps1` 通过 1029 个文件，仅保留既有两组 05-* 目录警告；`rg` 可命中新 SOP、raw 证据、内容导航和根索引入口；新增文件脱敏扫描未发现真实密钥，扫描只命中 `log.md` 历史 `EVEROS_API_KEY=...` 占位描述，非密钥泄露
- 待复查项: 若后续确定公众号主线只做技术长文或同时做认知成长类，应在 SOP 的默认内容类型中进一步收窄

## [2026-07-01] automation | GitHub 热门项目滚动日报更新
- 改动范围: `06-报告证据/latest-github-trending.md`、`06-报告证据/报告索引.md`、`index.md`、`log.md`
- 改动原因: 按 GitHub Trending Daily 与 Repository API 更新最近 24 小时热门项目固定滚动页，并继续记录“知识库页 vs 固定报告页”口径冲突
- 验证结果: 已执行行数、索引命中与 local_file_index 检索命令；结果以本次自动化输出为准

## [2026-07-02] automation | GitHub 热门项目自动化落盘规则修正
- 改动范围: Codex automation `github` 配置
- 改动原因: 按用户要求改为更新 `知识库/04-方法论与工具/实用工具/GitHub 热门项目滚动观察.md`，并禁止该任务继续写入 `06-报告证据/latest-github-trending.md`、`06-报告证据/报告索引.md` 或根 `index.md`
- 验证结果: 已通过 Codex automation API 更新，`automation.toml` 确认目标页、raw 快照、log.md 与验证命令已改为当前知识库结构口径

## [2026-07-02] maintenance | XianyuAutoAgent 启动脚本检查兼容性修复
- 改动范围: `tools/start_xianyu_autoagent.ps1`、`log.md`
- 改动原因: 用户要求检查咸鱼 SOP 是否正常运行；排查发现 Windows PowerShell 5 下 `Invoke-WebRequest` 不带 `-UseBasicParsing` 会在 MiniMax `/v1/models` 检查阶段抛 `NullReferenceException`，造成脚本误报连通性失败
- 关键修复: MiniMax 连通性检查增加 `-UseBasicParsing` 与 `-ErrorAction Stop`，不修改 `.env` 中的 `API_KEY` 与 `COOKIES_STR`，不重启当前机器人进程
- 验证结果: `powershell -NoProfile -ExecutionPolicy Bypass -File tools/start_xianyu_autoagent.ps1 -CheckOnly` 与 `pwsh -NoProfile -ExecutionPolicy Bypass -File tools/start_xianyu_autoagent.ps1 -CheckOnly` 均能识别当前 PID 43432；MiniMax `/models` 与 `chat/completions` 最小探测返回 200；运行日志在 2026-07-02 12:01 持续出现心跳发送与响应
- 待复查项: 本轮未用另一个闲鱼账号发送真实买家消息，因此“自动回复内容端到端到达买家端”仍需人工消息验证

## [2026-07-02] maintenance | Raven Agent Harness 本机接入验证
- 改动范围: `raw/sources/EverMind-Raven/`、`知识库/05-智能体与Agent体系/Raven Agent Harness 使用记录.md`、`index.md`、`log.md`
- 改动原因: 用户要求查看并使用 EverMind-AI/Raven；按知识库规范将上游 README、依赖声明和 Windows 安装脚本作为 raw 快照留存，并记录本机安装、运行证据与阻塞项
- 验证结果: 已克隆 `https://github.com/EverMind-AI/Raven` 至 `tmp/Raven`；`uv run --no-dev raven --help` 通过；`npm ci` 与 `npm run build` 生成 TUI bundle；`raven --version` 返回 `Raven v0.1.2`；`raven tui --check` 返回 0；`raven provider list` 可列出 provider 但均为 `not set`
- 待复查项: `raven agent -m "hello"` 因 provider 未配置返回 `No API key configured`，真实 LLM agent 调用尚未完成；`npm run lint:rpc` 显示 `src/rpc/generated.ts` 与 `rpc-schema/openrpc.json` 不同步，属于上游源码一致性问题

## [2026-07-02] maintenance | 公众号发布 SOP 冒烟验证
- 改动范围: `06-报告证据/wechat-publish-sop-smoke-20260702.md`、`06-报告证据/报告索引.md`、`index.md`、`log.md`
- 改动原因: 用户要求检查公众号发布项目源码是否克隆到位，以及公众号发布 SOP 流程能否成功
- 验证结果: `D:\Projects\OpenSource\md2wechat-skill` 为 Git 仓库，远程为 `geekjourneyx/md2wechat-skill`，当前提交 `3306fd1d9433d69d7881f097226c6d0fea472ad3`，但工作区存在 2 个修改文件和 1 个未跟踪测试文章；`D:\Projects\OpenSource\AI微信公众号\harness-engineering` 为 Git 仓库，远程为 `deusyu/harness-engineering`，当前提交 `bebc743a1bb3e1895b507c6e8fec726b4461ffc9`，工作区干净；`md2wechat version --json` 返回 `2.0.7`；capabilities/providers/themes/prompts discovery 命令成功；`inspect` 带封面后 `draft_ready=true`
- 待复查项: 当前 Windows PATH 缺少 `go`，无法运行 `go test ./...`；API 模式 preview 因 md2wechat API key 格式无效降级；AI 模式仅生成 prompt，未生成最终 HTML；未执行 `test-draft/create_draft`，因为会触发远端微信草稿创建，需用户明确授权
- 口径修正: 用户提醒“之前默认使用 AI 模式”；已明确本知识库 SOP 主链路应显式使用 `--mode ai`，裸命令/API key 错误只说明 CLI/config 默认值为 `api`，不作为 AI 模式主链路失败证据

可以把 **EverOS 当成“本地长期记忆服务”** 来配合使用：你的 AI 助手、App、CLI Agent 或“第二大脑”系统负责产生对话/任务轨迹；EverOS 负责把这些内容抽取成长期记忆，保存为 Markdown，并建立 SQLite + LanceDB 索引用来检索。仓库说明里也明确说 EverOS 会把 conversations、files、agent trajectories 保存为可读 Markdown，并同步本地 SQLite 与 LanceDB 索引用于快速检索。([GitHub][1])

## 推荐配合方式

**核心闭环是：写入 → 抽取 → 检索 → 注入上下文。**

1. 对话结束或阶段性完成时，把用户/助手/工具消息 POST 到 EverOS 的 `/api/v1/memory/add`。
2. 会话结束时调用 `/api/v1/memory/flush`，强制把本轮 buffer 抽取成记忆。
3. 下一次用户提问前，先调用 `/api/v1/memory/search` 搜索相关历史记忆。
4. 把搜索结果整理成一段“长期记忆上下文”，放进你的 Agent prompt。
5. 记忆文件本身在 `~/.everos` 下，可用 Obsidian、VSCode、Git 直接查看/编辑；EverOS 的 cascade 会把 Markdown 改动同步进索引。([GitHub][2])

## 先跑通最小可用版本

安装：

```bash
pip install everos
# 或
uv pip install everos
```

仓库的快速开始要求 Python 3.12+，并且说明 EverOS 是作为服务运行：先启动 server，再通过 HTTP API 调用；不是直接在进程内 import 后使用。([GitHub][3])

初始化配置：

```bash
everos init
```

这里有一个小注意：中文 README 里写的是 `everos init` 生成 starter `.env`，再填入 DashScope / 百炼相关的 `EVEROS_LLM__API_KEY`、`EVEROS_EMBEDDING__API_KEY`、`EVEROS_RERANK__API_KEY`；英文 QUICKSTART 则写的是生成 `~/.everos/everos.toml + ome.toml`。所以实际操作时，以你安装版本执行 `everos init` 后生成的文件为准。([GitHub][1])

如果按中文 README 的百炼配置，可以类似这样填：

```bash
EVEROS_LLM__MODEL=qwen-plus
EVEROS_LLM__API_KEY=<DASHSCOPE_API_KEY>
EVEROS_LLM__BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

EVEROS_EMBEDDING__MODEL=text-embedding-v4
EVEROS_EMBEDDING__API_KEY=<DASHSCOPE_API_KEY>
EVEROS_EMBEDDING__BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

EVEROS_RERANK__MODEL=gte-rerank-v2
EVEROS_RERANK__API_KEY=<DASHSCOPE_API_KEY>
EVEROS_RERANK__BASE_URL=https://dashscope.aliyuncs.com
```

启动服务：

```bash
everos server start
```

检查健康状态：

```bash
curl http://127.0.0.1:8000/health
```

预期返回：

```json
{"status":"ok"}
```

EverOS 默认绑定 `127.0.0.1:8000`，并且官方 API 文档说明它本身不带内置鉴权；如果要暴露到局域网或公网，前面要加自己的网关/认证层。([GitHub][4])

## 最小写入与检索示例

写入一段对话：

```bash
TS=$(($(date +%s)*1000))

curl -X POST http://127.0.0.1:8000/api/v1/memory/add \
  -H 'Content-Type: application/json' \
  -d "{
    \"session_id\": \"demo-001\",
    \"app_id\": \"second-brain\",
    \"project_id\": \"default\",
    \"messages\": [
      {
        \"sender_id\": \"me\",
        \"role\": \"user\",
        \"timestamp\": $TS,
        \"content\": \"我正在搭建一个第二大脑系统，希望 AI 能记住我的项目、偏好和长期计划。\"
      },
      {
        \"sender_id\": \"assistant\",
        \"role\": \"assistant\",
        \"timestamp\": $((TS+10000)),
        \"content\": \"可以把项目决策、偏好、任务进展写入长期记忆，并在新会话开始时检索相关内容。\"
      }
    ]
  }"
```

手动触发抽取：

```bash
curl -X POST http://127.0.0.1:8000/api/v1/memory/flush \
  -H 'Content-Type: application/json' \
  -d '{
    "session_id": "demo-001",
    "app_id": "second-brain",
    "project_id": "default"
  }'
```

搜索记忆：

```bash
curl -X POST http://127.0.0.1:8000/api/v1/memory/search \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "me",
    "app_id": "second-brain",
    "project_id": "default",
    "query": "我在搭建什么系统？有什么长期目标？",
    "top_k": 5,
    "include_profile": true
  }'
```

`/add` 会把消息追加到 session buffer，`/flush` 会强制抽取，`/search` 支持按 `user_id` 或 `agent_id` 检索；`app_id` 和 `project_id` 会隔离不同应用/项目的记忆空间，不会跨 scope 搜索。([GitHub][4])

## 和“第二大脑”配合的实用架构

你可以这样分层：

```text
你的入口
ChatGPT / Claude Code / Cursor / 自写 Agent / 浏览器插件
        │
        │  1. 用户问题、助手回答、工具结果
        ▼
你的中间层
session 管理、消息整理、隐私过滤、prompt 拼接
        │
        │  2. POST /memory/add + /memory/flush
        ▼
EverOS
Markdown source of truth + SQLite + LanceDB
        │
        │  3. POST /memory/search
        ▼
下一轮 Prompt
“以下是和本次问题相关的长期记忆……”
```

我建议你把 `app_id` 固定成你的系统名，比如 `second-brain`；把 `project_id` 分成不同空间，例如 `personal`、`work`、`research`、`coding`。这样同一个 EverOS 服务可以承载多个记忆域，但检索时不会串库。官方 API 文档也说明 `app_id/project_id` 是磁盘层面的隔离维度，搜索和读取不会跨不同 scope。([GitHub][4])

## 和 AI 编程工具配合

如果你主要想配合 **Claude Code / Cursor / Cline / Gemini CLI / Aider** 这类工具，有两条路线：

**路线 A：直接用现成插件/云端 EverMem。** EverOS 仓库的 use-cases 里有 Claude Code Plugin，功能包括自动保存对话、提交 prompt 时自动检索记忆、会话启动时加载最近上下文、手动搜索和 Memory Hub。这个插件偏 EverMem Cloud 工作流，适合先体验“AI coding 长期记忆”的交互方式。([GitHub][5])

**路线 B：自己做一个本地 MCP/插件桥接 EverOS。** 也就是让 MCP server 或 Claude Code hook 去调用本地 `http://127.0.0.1:8000/api/v1/memory/search` 和 `/add`。这样更适合你想把记忆留在本地、进入自己的“第二大脑”目录。EverOS 官方 API 已经把这几个端点定义清楚，所以桥接层可以很薄。([GitHub][4])

## 最推荐的使用习惯

每次会话开始前，先用当前用户问题做一次 `/memory/search`，取回 3–8 条最相关的 episodes / atomic facts / profile，然后拼成：

```text
以下是用户的长期记忆，仅在相关时使用：
- ...
- ...
```

每次会话结束时，把本轮完整消息写入 `/memory/add`，然后 `/memory/flush`。如果是 coding agent，还可以把 `agent_id` 设成 `claude-code`、`codex` 或你自己的 agent 名，让 EverOS 同时沉淀用户记忆和 agent 轨迹。EverOS 的记忆类型里区分 user track 和 agent track：用户侧包括 episodes/profile，agent 侧包括 cases/skills。([GitHub][2])

## 注意事项

`/flush` 返回后，Markdown 已经写入磁盘，但索引是异步更新的；所以刚写完马上 `/search` 可能搜不到，官方文档建议用 retry/backoff，或者用 `everos cascade sync` 强制同步。([GitHub][4])

如果要摄取 PDF、图片、音频、Office 文档，需要安装多模态 extra：`pip install 'everos[multimodal]'`；Office 文档还需要系统安装 LibreOffice，否则 Office 上传会失败，但 PDF/图片/音频/HTML 不受影响。([GitHub][1])

我会把它用于你的第二大脑时，优先按这个策略落地：**EverOS 只管长期记忆；你的主系统负责判断“什么值得写入、什么时候检索、检索结果如何进入 prompt”。** 这样最稳，也最容易以后替换模型、换前端或接入 MCP。

[1]: https://github.com/EverMind-AI/EverOS/blob/main/README.zh-CN.md "EverOS/README.zh-CN.md at main · EverMind-AI/EverOS · GitHub"
[2]: https://github.com/EverMind-AI/EverOS/blob/main/docs/how-memory-works.md "EverOS/docs/how-memory-works.md at main · EverMind-AI/EverOS · GitHub"
[3]: https://github.com/EverMind-AI/EverOS/blob/main/QUICKSTART.md "EverOS/QUICKSTART.md at main · EverMind-AI/EverOS · GitHub"
[4]: https://github.com/EverMind-AI/EverOS/blob/main/docs/api.md "EverOS/docs/api.md at main · EverMind-AI/EverOS · GitHub"
[5]: https://github.com/EverMind-AI/EverOS/tree/main/use-cases/claude-code-plugin "EverOS/use-cases/claude-code-plugin at main · EverMind-AI/EverOS · GitHub"

---
title: mattpocock/skills 研究
tags:
  - agent
  - skill体系
  - claude-code
  - 工程方法论
created: 2026-05-16
updated: 2026-05-16
sources:
  - https://github.com/mattpocock/skills
  - https://raw.githubusercontent.com/mattpocock/skills/main/README.md
  - https://raw.githubusercontent.com/mattpocock/skills/main/CLAUDE.md
  - https://raw.githubusercontent.com/mattpocock/skills/main/CONTEXT.md
---

# mattpocock/skills 研究

> 86k ⭐ 的开源 agent skills 仓库，Matt Pocock（Total TypeScript 作者）把自己在 Claude Code 中的 skills 目录直接开源。

## 核心定位

**"Skills for Real Engineers — not vibe coding"**

Matt 认为常见失败模式是"Agent 没做对的事"，解法不是换模型，而是**结构化的工程方法论 + 严格的交接流程**。

## 目录结构

```
skills/
├── CLAUDE.md              # Agent 行为定义规范
├── CONTEXT.md            # 术语表/领域词汇（Glossary）
├── skills/
│   ├── engineering/       # 工程类（11个skill）
│   │   ├── diagnose/      # 诊断循环：复现→最小化→假设→验证→修复→回归
│   │   ├── tdd/          # TDD 垂直切片法
│   │   ├── triage/       # Issue 分类状态机
│   │   ├── to-prd/       # 需求转 PRD
│   │   ├── to-issues/    # 任务转 Issue（垂直切片）
│   │   ├── zoom-out/     # 宏观视角
│   │   ├── grill-with-docs/
│   │   ├── improve-codebase-architecture/
│   │   ├── prototype/
│   │   └── setup-matt-pocock-skills/
│   ├── productivity/      # 通用效率类（4个）
│   │   ├── handoff/      # 会话移交文档
│   │   ├── caveman/      # 极简压缩沟通
│   │   ├── grill-me/     # 苏格拉底追问
│   │   └── write-a-skill/
│   ├── personal/
│   ├── misc/
│   ├── in-progress/
│   └── deprecated/
├── docs/adr/             # 架构决策记录
└── scripts/              # link-skills 等工具脚本
```

## Skill 格式规范（SKILL.md）

每个 skill 是一个目录，包含 `SKILL.md`（+ 可选 scripts/ 等）：

```yaml
---
name: skill-name
description: 简短描述能力。Use when [触发条件].
argument-hint: 当用户传入参数时提示文本（可选）
disable-model-invocation: true  # 可选，禁止递归调用自己
---
```

正文用 Markdown，简洁精炼。Matt 的 SKILL.md 通常 50-200 行，极少超过 500 行。

## 核心 Skill 详解

### 1. handoff（会话移交）

**作用**：将会话压缩成结构化文档，给下一个 agent 接续使用。

**格式要点**：
- 保存到 `mktemp -t handoff-XXXXXX.md`（临时文件路径）
- 不重复已有制品（PRDs、plans、ADRs、issues、commits），只引用
- 建议下一个 session 使用哪些 skills
- 基于用户传入的参数调整文档重点

```yaml
---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
---
```

**vs Hermes 现有做法**：我们目前手动写长篇交接文档，Matt 的版本更工具化（直接 `mktemp` 输出文件）。

### 2. diagnose（诊断循环）

**作用**：对硬 Bug 和性能回退的结构化诊断流程。

**六步法**：
1. **Build a feedback loop** — 构建一个可重复运行的 pass/fail 信号
2. **Reproduce** — 复现 Bug
3. **Minimise** — 最小化复现步骤
4. **Hypothesise** — 形成假设
5. **Instrument** — 插桩验证
6. **Fix + regression-test** — 修复 + 回归测试

**核心洞察**：
> "Build the right feedback loop, and the bug is 90% fixed."

反馈环的构建优先级：
1. Failing test
2. Curl / HTTP script
3. CLI invocation
4. Headless browser (Playwright)
5. Replay captured trace
6. Throwaway harness
7. Property/fuzz loop
8. Bisection harness
9. Differential loop
10. HITL bash script（最后手段）

### 3. caveman（极简压缩沟通）

**作用**：节省 ~75% token，保留全部技术准确性。

**触发词**："caveman mode", "talk like caveman", "less tokens", "be brief"

**规则**：
- 删除：冠词(a/an/the)、填充词(just/really/basically/actually/simply)、客套话(sure/certainly/of course/happy to)、 hedge 词
- 允许：缩写（DB/auth/config/req/res/fn/impl）、片段、用箭头表示因果（X -> Y）

**格式**：`[thing] [action] [reason]. [next step].`

**Example**：
> Not: "Sure! I'd be happy to help you with that. The issue you're experiencing is likely caused by..."
> Yes: "Bug in auth middleware. Token expiry check use `<` not `<=`. Fix:"

**Persistence**：一旦触发，保持到用户说"stop caveman"或"normal mode"。

### 4. grill-me / grill-with-docs（苏格拉底追问）

**作用**：穷尽决策树所有分支，直到达到 shared understanding。

- `grill-me`：通用版，直接追问
- `grill-with-docs`：增强版，同时挑战计划与现有领域模型的一致性，更新 CONTEXT.md

**原则**：每次只问一个问题，回答后再问下一个。如果问题可以通过浏览代码库回答，就直接去看代码。

### 5. zoom-out（宏观视角）

**作用**：当不熟悉某块代码时，要求 agent 给出更高层次的地图。

**触发**：`disable-model-invocation: true` — 禁止递归调用自己。

```yaml
---
name: zoom-out
description: Tell the agent to zoom out and give broader context...
disable-model-invocation: true
---
```

### 6. tdd（测试驱动开发）

**核心原则**：测试通过公共接口验证行为，不验证实现细节。

**反模式**：Horizontal Slices（先写所有测试，再写所有实现）→ 产生糟糕的测试。

**正确做法**：Vertical Slices（Tracer Bullets）— 一个测试 → 一个实现 → 重复。每个测试响应前一个循环中学到的东西。

### 7. triage（Issue 分类状态机）

**5个状态角色**：
- `needs-triage` → 待评估
- `needs-info` → 等待用户提供更多信息
- `ready-for-agent` → 完全规格化，可由 AFK agent 接手
- `ready-for-human` → 需要人工实现
- `wontfix` → 不会修复

**每个 Issue 同时携带一个分类角色**：`bug` 或 `enhancement`。

## 对 Hermes Agent 的启发

### 可以直接引入的

| Skill | 用途 | Hermes 等效 |
|-------|------|-------------|
| `handoff` | 会话移交文档 | 已有手动交接做法，需工具化 |
| `grill-me` | 苏格拉底追问 | 暂无对应 |
| `caveman` | 极简沟通 | 暂无对应 |
| `zoom-out` | 宏观视角 | 暂无对应 |
| `diagnose` | 结构化调试 | 已有 systematic-debugging，需对标 |

### 核心理念对齐

1. **Skill 描述是 trigger**：`description` 的 "Use when..." 部分是 agent 决定加载哪个 skill 的唯一依据，必须精准。
2. **SKILL.md 保持简短**：Matt 的 skill 通常 <100 行，内容多则拆分到 REFERENCE.md。
3. **不重复制品**：交接文档引用而不复制 PRDs、plans、commits 等已有制品。
4. **垂直切片 > 水平切片**：不管是 TDD 还是 to-issues，核心都是 end-to-end 的薄片，而非按层切。

## 归档元信息

- 原始仓库：https://github.com/mattpocock/skills
- 86k ⭐, 7.5k Fork
- License: MIT
- 主要维护者：Matt Pocock（Total TypeScript）
- 本地缓存：`/tmp/mattpocock_skills/`

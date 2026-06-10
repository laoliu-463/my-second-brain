---
kb_id: instructions/01-completion-gates
title: 完工门禁 G0-G4
domain: instructions
category: gates
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/CURRENT_STATE.md
  - harness/FORBIDDEN_SCOPE.md
  - harness/HARNESS_DEBT.md
related_reports: []
forbidden_misread:
  - G4 必须有证据；未生成 evidence 不得声明 PASS
  - 不得把 G3 失败后用"风险接受"绕过 G4
---

# 完工门禁 G0-G4

## 1. 目的

为每个业务 / 工程任务定义可机检的完工判定。任何 Agent / 人类在声明"完成"前必须通过 5 个门禁；缺一即不得声明 PASS。

## 2. 门禁列表

| 门禁 | 名称 | 检查内容 | 未过后果 |
| --- | --- | --- | --- |
| G0 | 范围与边界 | 命中域、流程、ADR 是否明确；FORBIDDEN_SCOPE 是否已读 | 不允许进入 G1 |
| G1 | 文档同步 | 修改代码 / 配置 / 业务规则时，docs/ 同步更新 | 不允许进入 G2 |
| G2 | 自测与构建 | `mvn test` / `npm run build` / `npm run e2e:v1-p0` 通过 | 不允许进入 G3 |
| G3 | 真实上游验证（按需） | real-pre 任务必须 `npm run e2e:real-pre:p0:preflight` + 真实订单/商品/达人样本 | 不允许进入 G4 |
| G4 | 证据生成 | 至少 1 类证据：脚本输出、API/SQL 结果、文件路径；登记到 `docs/验收/验收证据索引.md` 或本任务报告 | 不允许声明 PASS |

## 3. 各门禁详细规则

### G0 - 范围与边界

- 命中的 `docs/领域/*.md` 是否已读
- 命中的 `docs/流程/*.md` 是否已读
- 命中的 `docs/决策/ADR-*.md` 是否已登记
- `harness/FORBIDDEN_SCOPE.md` 是否通读
- 是否有未声明的越界行为

### G1 - 文档同步

- 修改业务规则 → `docs/领域/*.md` / `docs/流程/*.md` 同步
- 修改部署 / 端口 / 开关 → `harness/environment/*` 与 `docs/10-部署运行总览.md` 同步
- 修改决策 → `harness/state/DECISIONS.md` + 新 ADR
- 修改 Harness 规则 → `harness/HARNESS_CHANGELOG.md` + 本 KB `governance/02-changelog-rules.md`

### G2 - 自测与构建

- Java：`cd backend && mvn test` 通过
- 前端：`cd frontend && npm run build` 通过
- 静态检查：TS / ESLint / Prettier 通过
- 单测覆盖率 ≥ 80%（V1 最低）

### G3 - 真实上游验证

仅适用于涉及 real-pre 的任务：

- `npm run e2e:real-pre:p0:preflight` 通过
- 真实订单 / 商品 / 达人样本 ≥ 1
- 渠道归因三环：转链 → 订单 → 业绩 都存在真实样本
- 部署结论严格按 `docs/验收/real-pre联调手册.md` 口径

### G4 - 证据生成

至少 1 类，缺一即不可 PASS：

1. **脚本输出**：`mvn test` / `npm run e2e:v1-p0` / `npm run e2e:real-pre:p0` 完整日志
2. **API/SQL 对账**：cURL 输出 + SQL 行数 / 字段对比
3. **文件路径**：截图 / trace / 日志 / 文档索引路径

证据必须登记到：

- `docs/验收/验收证据索引.md`（业务验收）
- `harness/reports/<task-id>-<date>-<time>.md`（任务报告）

## 4. 门禁失败处理

| 失败门禁 | 动作 |
| --- | --- |
| G0 | 立即停，回 G0 重做 |
| G1 | 立即停，先补文档 |
| G2 | 立即停，先修测试 / 构建 |
| G3 | 标 `BLOCKED_BY_SAMPLE` / `BLOCKED_BY_EXTERNAL` |
| G4 | 标 `PARTIAL_DIRTY_REMAINING` |

## 5. 与 Session Exit Gate 的关系

- Session Exit Gate 是本表 5 个门禁的"运行时分发"。
- 每个任务结束必须输出最终状态（合法状态 7 选 1）。
- 多个 G4 失败 → 升级为 `BLOCKED_DIRTY_UNKNOWN`。

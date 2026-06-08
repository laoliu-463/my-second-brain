---
kb_id: state/03-decisions
title: DECISIONS 主源
domain: state
category: state-decisions
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/DECISIONS.md
  - docs/决策/ADR-002-V1范围优先级.md
related_reports: []
forbidden_misread:
  - 决策记录一旦写入不得"翻案"为另一结论
  - 推翻历史决策必须新写一条 ADR
---

# DECISIONS 主源

## 1. 用途

记录所有"改变项目方向 / 范围 / 不可逆行为"的决策（ADR）。

## 2. ADR 模板

```markdown
# ADR-NNN <title>

- 日期: YYYY-MM-DD
- 触发: <任务id / 现象>
- 状态: PROPOSED / ACCEPTED / SUPERSEDED

## 背景
<为什么需要决策>

## 选项
1. <选项 1>
2. <选项 2>
3. <选项 3>

## 决策
<选了哪一项，为什么>

## 影响
<代码 / 文档 / 部署 / 验收>

## 风险
<已知风险>
```

## 3. 必须触发 ADR 的场景

- 范围变更（V1 边界）
- 端口 / 网络 / 部署变更
- 跨域耦合
- 数据迁移破坏性变更
- 安全事件修复
- 历史 V* SQL 修改
- 测试基线切换
- 角色 / 权限变更

## 4. 已存在 ADR 索引

- ADR-001-V1范围确定
- ADR-002-V1范围优先级
- ADR-003-real-pre端口绑定
- ADR-004-V1业务口径
- ADR-005-工作区治理
- ADR-006-估值轨/结算轨双轨计算
- ADR-007-订单源 6468+2704 归属

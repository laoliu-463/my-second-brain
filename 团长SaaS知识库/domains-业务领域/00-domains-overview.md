---
kb_id: domains/00-domains-overview
title: 八大领域总览与契约
domain: domains
category: domains-overview
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/01-V1交付范围与边界.md
  - docs/领域/*.md
  - harness/DOMAIN_STATUS.md
related_reports: []
forbidden_misread:
  - 8 域只对应 V1 范围，旧 V2.2 独家达人/独家商家不在其中
  - 订单域只存事实，不算提成
---

# 八大领域总览与契约

## 1. 8 域列表与 V1 必做/不做

| 域 | V1 必做 | V1 不做（V2 预留） |
| --- | --- | --- |
| user 用户域 | 6 角色、4 部门、self/group/all 数据范围 | SSO / 第三方登录 |
| config 配置域 | 服务费率、招商提成率、媒介提成率、技术服务费 | 公式可视化编辑 |
| product 商品域 | 转链 + pick_source_mapping | 商品全量同步 |
| talent 达人域 | 基础档案、绑定商品 | 独家达人、达人画像 |
| sample 寄样域 | 订单已同步事件触发交作业 | 物流真实回传 |
| order 订单域 | 6468 + 2704 两源同步 | 实时对账、独家覆盖 |
| performance 业绩域 | 渠道链/招商链/管理链三链归属、冲正、双轨金额 | 差异化提成、独家业绩 |
| analysis 分析域 | 看板只读汇总表 | 重算归属、实时分析 |

## 2. 域契约（V1 不变量）

| 域 | 不变量 |
| --- | --- |
| user | 统一提供 self / group / all 数据范围 |
| config | 不执行具体业务规则 |
| product | 转链必须落 `pick_source_mapping` |
| talent | 不参与订单归因 |
| sample | 通过订单已同步事件判断交作业完成 |
| order | 只存事实、不算提成、不应用独家覆盖 |
| performance | 最终归属、提成、冲正、双轨金额计算 |
| analysis | 只读汇总表，不重算业绩归属 |

## 3. 域间依赖

```
config ─┐
        ├─→ order ─→ performance ─→ analysis
product ┤    ↑
talent  ┘    │
             └─ sample（订单已同步）
user ────────→ 所有域（数据范围）
```

## 4. 域状态机

详见 [state-状态主源/02-domain-status-DOMAIN_STATUS 主源.md](../state-状态主源/02-domain-status-DOMAIN_STATUS 主源.md)。每个域独立维护：
NOT_STARTED / IN_PROGRESS / PASS / PENDING / BLOCKED_BY_SAMPLE / BLOCKED_BY_EXTERNAL / FAILED / RISK_ACCEPTED。

## 5. 域验收口径

| 域 | 验收关键证据 |
| --- | --- |
| user | 6 角色 + 4 部门 + 数据范围 API |
| config | 服务费率 / 提成率生效 + 业绩计算一致性 |
| product | 转链成功率 + pick_source 样本存在 |
| talent | 达人基础档案可查 |
| sample | 订单已同步事件触发交作业 |
| order | 6468 + 2704 同步成功 + 订单表与业绩表 anti-join |
| performance | 三链归属 + 双轨金额 + 冲正链路 |
| analysis | 看板只读汇总表，不重算 |

## 6. V1 范围外（旧 V2.2）

以下条目**V1 不做**，不得写入 V1 验收：

- 独家达人 / 独家商家全量闭环
- 完整重算（业绩重新归属）
- MQ 化事件（先同步调用，MQ 化按专项处理）
- 外部 `quick_sample_apply`（先内部样本）
- 真实物流自动化
- 高级看板 + 差异化提成
- 公式可视化编辑

## 7. DDD 优化顺序（V1 优先级）

1. user（数据范围）→
2. config（公式与配置）→
3. order（事实表）→
4. performance（归属与提成）→
5. analysis（只读汇总）→
6. product / talent / sample（辅助域）→
7. outbox / 异步化 →
8. frontend / E2E →
9. GC + 死代码清理

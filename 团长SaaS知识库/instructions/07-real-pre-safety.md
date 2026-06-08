---
kb_id: instructions/07-real-pre-safety
title: real-pre 安全清单
domain: instructions
category: safety
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/验收/real-pre联调手册.md
  - harness/environment/03-real-pre-deploy.md
  - harness/FORBIDDEN_SCOPE.md
related_reports:
  - harness/reports/evidence-*real-pre*.md
forbidden_misread:
  - 容器 healthy ≠ 业务闭环 PASS
  - 无真实订单样本时 P0 仍 PENDING
  - 不得以"风险接受"绕过 G3
---

# real-pre 安全清单

## 1. 目的

为 real-pre 环境的部署、验证、清理提供统一的最小安全清单。任何针对 real-pre 的操作必须先通过本清单。

## 2. real-pre 与 test 的边界

| 维度 | test | real-pre |
| --- | --- | --- |
| 端口 | 3000/8080 | 3001/8081 |
| 数据库 | 临时实例 | 真实上游联调 |
| 上游 | Mock | 真实抖店 / 抖音 |
| Token | 测试 | 真实 |
| 订单 | 注入 | 真实同步 |
| 部署结论 | V1-P0 基线 | 阻塞 P0 验收，需证据 |

## 3. 部署前必检（9 项）

- [ ] `git status --short` 工作区干净或 dirty 已登记
- [ ] `npm run e2e:real-pre:p0:preflight` 预检通过
- [ ] `.env.real-pre` 存在且不跨机交付
- [ ] `DOUYIN_REAL_UPSTREAM_MODE=live`（禁止其他值）
- [ ] `APP_TEST_ENABLED=false`
- [ ] `DOUYIN_TEST_ENABLED=false`
- [ ] 容器端口 3001/8081 绑定 127.0.0.1
- [ ] 数据库连接串不含明文密码
- [ ] 备份策略已确认（用于回退）

## 4. 部署中禁止（10 项）

- 禁止 `docker compose down -v`
- 禁止清库
- 禁止 drop / truncate / delete 全表
- 禁止绕过 repair / backfill 入口裸 SQL
- 禁止 `APP_TEST_ENABLED=true`
- 禁止 `DOUYIN_TEST_ENABLED=true`
- 禁止 `DOUYIN_REAL_UPSTREAM_MODE=mock` / `test`
- 禁止删除 volume
- 禁止使用 mock 数据冒充真实闭环
- 禁止把 BLOCKED_BY_SAMPLE 包装成 PASS

## 5. 部署后必检（7 项）

- [ ] `docker compose ps` 容器 healthy
- [ ] 业务三环存在真实样本：转链 / 订单 / 业绩
- [ ] 渠道归因三环闭合：转链 → 订单 → 业绩
- [ ] 业绩双轨金额存在：预估 / 结算
- [ ] 寄样域自动完成通过订单已同步事件触发
- [ ] 真实订单 / 真实金额 / 真实渠道齐全
- [ ] 证据已登记到 `docs/验收/验收证据索引.md` + `harness/reports/`

## 6. P0 验收结论口径

| 条件 | 状态 |
| --- | --- |
| 无失败 + 无真实订单 | PENDING |
| 无失败 + 有真实订单 + 三环未闭合 | BLOCKED_BY_SAMPLE |
| 无失败 + 有真实订单 + 三环已闭合 + 证据齐全 | PASS |
| 有失败 + 任何样本 | FAILED |
| 失败但 Owner 接受 | RISK_ACCEPTED_BY_USER |

## 7. 紧急回退流程

- 任何失败 → 立即停 → 写 `harness/reports/incident-*.md`
- 紧急回退 → `git revert`（不得 `git reset --hard`）
- 通知 Owner → 等待拍板
- 不得在 Owner 未拍板前继续新任务

## 8. 与 Session Exit Gate 联动

- real-pre 任务结束必须输出 7 选 1 状态码
- `BLOCKED_BY_SAMPLE` / `BLOCKED_BY_EXTERNAL` 是合法退出
- `DONE_CLEAN` 必须有真实样本 + 三环闭合 + 证据

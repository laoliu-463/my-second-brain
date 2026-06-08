---
kb_id: instructions/03-forbidden-scope
title: 禁做范围与失败模式
domain: instructions
category: forbidden
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - harness/FORBIDDEN_SCOPE.md
  - docs/01-V1交付范围与边界.md
  - docs/决策/ADR-002-V1范围优先级.md
related_reports: []
forbidden_misread:
  - 本文件不是百科，是 V1 强约束；任何与本文件冲突的"看起来更简单方案"直接拒绝
  - V1 必不做 ≠ V2 预留；后者见 docs/01-V1交付范围与边界.md
---

# 禁做范围与失败模式

## 1. 目的

集中登记 V1 必不做、V1 禁止启用、领域边界禁止、real-pre 数据破坏禁止、real-pre 禁止、Git 与密钥禁止、Git 工作区治理禁止、代码边界禁止、结论禁止、虚假完成禁止、脏状态退出禁止。

**主源**：`harness/FORBIDDEN_SCOPE.md`（170 行）。本文件为摘要；冲突时以主源为准。

## 2. V1 明确不做（10 项）

1. 独家达人 / 商家覆盖
2. 经营毛利口径扩展（已撤销到 P0 验收口径，2026-06-05 用户决策）
3. 个别品负责人覆盖
4. 商品负责人变更历史重算
5. 差异化提成
6. Cookie / 代理池
7. 物流 API 自动跟踪
8. 外部抖店快速寄样 `quick_sample_apply`
9. 数据平台整体导出
10. 不用 mock 数据证明真实闭环

## 3. V1 禁止启用（10 项）

1. 独家达人 / 商家覆盖
2. 个别品负责人覆盖
3. 毛利作为 P0（已撤销）
4. 寄样 30 天自动关闭
5. 物流 API 阻塞寄样
6. 差异化提成
7. Spring Boot → FastAPI
8. 拆微服务
9. 引入 Kafka / RabbitMQ
10. Mock 数据冒充 real-pre 真实闭环

## 4. 领域边界禁止（11 项）

- 订单域：不得计算提成 / 写 `performance_records` / 更新寄样完成 / 应用独家覆盖
- 业绩域：不得同步抖音订单 / 不得修改订单事实
- 分析模块：不得重算业绩归因
- 商品域：不得写寄样表
- 寄样域：不得同步订单
- Controller：不得编排复杂业务规则
- 跨领域：不得直接访问 Repository

## 5. real-pre 数据破坏禁止（3 项）

- 禁止 drop / truncate / delete 全表
- 禁止绕过 repair / backfill 入口裸 SQL
- 禁止 `docker compose down -v`

## 6. real-pre 禁止（10 项）

- 禁止清库
- 禁止 `docker compose down -v`
- 禁止删除 volume
- 禁止改 test / mock
- 禁止 `APP_TEST_ENABLED=true`
- 禁止 `DOUYIN_TEST_ENABLED=true`
- 禁止 `DOUYIN_REAL_UPSTREAM_MODE` 非 `live`

## 7. Git 与密钥禁止（4 项）

- 禁止提交 `.env` / `.pem` / `.key`
- 禁止输出 token / 密码
- 禁止 `.env.real-pre` 跨机交付
- 禁止 `git add .` / `git add -A` / `git add <dir>/`

## 8. Git 工作区治理禁止（21 项）

- 禁止 git add . / git add -A / git add <dir>/
- 禁止提交 unknown dirty
- 禁止混批 commit
- 禁止 dirty 部署
- 禁止 dirty 拷贝远端
- 禁止未提交部署
- 禁止远端 dirty 部署
- 禁止未部署写成已部署
- 禁止未提交写成已推送
- 禁止 PARTIAL 写成 DONE
- 禁止混合错误状态
- 禁止未收口继续新任务
- 禁止 `git commit --amend`（无授权）
- 禁止 `--no-verify`（无授权）
- 禁止 `git push --force` 到 main / master
- …（完整 21 项见 `harness/FORBIDDEN_SCOPE.md`）

## 9. 代码边界禁止（7 项）

- 前端不得直接调用抖音 / 抖店开放接口
- 前端不得硬编码业务规则
- 订单域不得计算提成
- 配置域不得执行业务规则
- 分析模块不得重算业绩归属
- …（完整 7 项见主源）

## 10. 结论禁止（6 项）

- 禁止未构建声明可用
- 禁止未重启声明生效
- 禁止未健康检查声明正常
- 禁止未生成 evidence 声明完成
- 禁止 BLOCKED / PENDING / PARTIAL 写成 PASS
- 禁止 "应该没问题" 替代验证

## 11. 虚假完成禁止（13 项）

- 禁止未重启称生效
- 禁止只编译称完成
- 禁止只测 Controller
- 禁止只测后端
- 禁止只测 mock
- 禁止 BLOCKED 包装 PASS
- 禁止缺真实样本称闭环
- 禁止未生成 evidence 称验收
- 禁止未更新 DOMAIN_STATUS / CURRENT_STATE
- 禁止 "应该可以" 写成 "已完成"
- 禁止未选 Gate 声明完成
- 禁止只验证本域
- …（完整 13 项见主源）

## 12. 脏状态退出禁止（10 项）

- 禁止 build / test 失败未说明退出
- 禁止容器异常未说明退出
- 禁止临时文件未清理退出
- 禁止 debug 残留退出
- 禁止 TODO 无归属退出
- 禁止修改启动路径未更新文档退出
- 禁止修改领域状态未更新 DOMAIN_STATUS 退出
- 禁止修改 harness 规则未更新 HARNESS_CHANGELOG 退出
- 禁止无最终 Session Exit Report 退出
- …（完整 10 项见主源）

## 13. 合法状态（与 FORBIDDEN_SCOPE 一致）

`DONE` / `PARTIAL` / `BLOCKED_BY_SAMPLE` / `BLOCKED_BY_EXTERNAL` / `FAILED` / `RISK_ACCEPTED_BY_USER`

## 14. 例外申请

- 例外仅 Owner 接受后写入 `docs/决策/ADR-*.md`，并在 `harness/reports/` 留存证据。
- Agent 不得自行扩大或解释例外。

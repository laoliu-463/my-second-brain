# SID-B01 source_id 候选表

- run_id: 20260623-235035
- batch_id: SID-B01
- scope: KB_ROOT
- status: candidate-only
- batch_size: 30
- source: inventory.md + c-level-preflight.md

## 0. 本文件边界

- 本文件只生成 `source_id` 候选，不写入原文件。
- 本文件不改变现有 `id`、`type`、`title`、`status` 或正文。
- 根文件和 `AGENTS.md` 属于系统入口/规则文件，默认不自动执行。
- 候选 `source_id` 使用 `src-20260623-kb-<short>`，其中 `kb` 为本实例作者/来源占位。

## 1. 命名规则

|字段|规则|说明|
|---|---|---|
|前缀|`src`|固定来源标识前缀|
|日期|`20260623`|本轮 KB_ROOT 结构化生成日期|
|author|`kb`|本实例知识库来源占位，待最终确认|
|short|英文稳定 slug|由目录语义 + 文件语义生成|

## 2. 候选清单

|序号|路径|类别|风险|现有 id|候选 source_id|依据|默认动作|
|---:|---|---|---|---|---|---|---|
|1|日志.md|map|low||src-20260623-kb-root-log|根日志入口|候选，不自动写入|
|2|索引.md|map|low||src-20260623-kb-root-index|根索引入口|候选，不自动写入|
|3|AGENTS.md|map|high||src-20260623-kb-root-agents|根规则文件|候选，不自动写入|
|4|README.md|map|low||src-20260623-kb-root-readme|根说明入口|候选，不自动写入|
|5|00-规范/安全边界.md|map|low|kb-00-规范-安全边界|src-20260623-kb-spec-safety-boundary|规范页 + 安全边界|可转 B 级|
|6|00-规范/结构规范.md|map|low|kb-00-规范-结构规范|src-20260623-kb-spec-structure|规范页 + 结构规范|可转 B 级|
|7|00-规范/页面规范.md|map|low|kb-00-规范-页面规范|src-20260623-kb-spec-page|规范页 + 页面规范|可转 B 级|
|8|01-状态/待确认问题.md|synthesis|low|kb-01-状态-待确认问题|src-20260623-kb-status-pending-questions|状态页 + 待确认问题|可转 B 级|
|9|01-状态/当前状态.md|synthesis|low|kb-01-状态-当前状态|src-20260623-kb-status-current|状态页 + 当前状态|可转 B 级|
|10|01-状态/技术债台账.md|synthesis|low|kb-01-状态-技术债台账|src-20260623-kb-status-tech-debt|状态页 + 技术债台账|可转 B 级|
|11|01-状态/已确认决策.md|synthesis|low|kb-01-状态-已确认决策|src-20260623-kb-status-confirmed-decisions|状态页 + 已确认决策|可转 B 级|
|12|01-状态/资料来源.md|source-note|low|kb-01-状态-资料来源|src-20260623-kb-status-source-register|状态页 + 资料来源|可转 B 级|
|13|02-项目总览/环境说明.md|synthesis|low|kb-02-项目总览-环境说明|src-20260623-kb-overview-environment|项目总览 + 环境说明|可转 B 级|
|14|02-项目总览/术语表.md|synthesis|low|kb-02-项目总览-术语表|src-20260623-kb-overview-glossary|项目总览 + 术语表|可转 B 级|
|15|02-项目总览/系统地图.md|synthesis|low|kb-02-项目总览-系统地图|src-20260623-kb-overview-system-map|项目总览 + 系统地图|可转 B 级|
|16|02-项目总览/项目概览.md|synthesis|low|kb-02-项目总览-项目概览|src-20260623-kb-overview-project|项目总览 + 项目概览|可转 B 级|
|17|02-项目总览/验收门禁.md|synthesis|low|kb-02-项目总览-验收门禁|src-20260623-kb-overview-acceptance-gate|项目总览 + 验收门禁|可转 B 级|
|18|02-项目总览/业务闭环.md|synthesis|low|kb-02-项目总览-业务闭环|src-20260623-kb-overview-business-loop|项目总览 + 业务闭环|可转 B 级|
|19|03-领域知识/达人域.md|entity|low|kb-03-领域知识-达人域|src-20260623-kb-domain-creator|领域知识 + 达人域|可转 B 级|
|20|03-领域知识/订单域.md|entity|low|kb-03-领域知识-订单域|src-20260623-kb-domain-order|领域知识 + 订单域|可转 B 级|
|21|03-领域知识/抖音上游接口.md|entity|low|kb-03-领域知识-抖音上游接口|src-20260623-kb-domain-douyin-upstream-api|领域知识 + 抖音上游接口|可转 B 级|
|22|03-领域知识/寄样域.md|entity|low|kb-03-领域知识-寄样域|src-20260623-kb-domain-sample|领域知识 + 寄样域|可转 B 级|
|23|03-领域知识/看板分析域.md|entity|low|kb-03-领域知识-看板分析域|src-20260623-kb-domain-dashboard-analytics|领域知识 + 看板分析域|可转 B 级|
|24|03-领域知识/商品域.md|entity|low|kb-03-领域知识-商品域|src-20260623-kb-domain-product|领域知识 + 商品域|可转 B 级|
|25|03-领域知识/业绩域.md|entity|low|kb-03-领域知识-业绩域|src-20260623-kb-domain-performance|领域知识 + 业绩域|可转 B 级|
|26|03-领域知识/用户配置域.md|entity|low|kb-03-领域知识-用户配置域|src-20260623-kb-domain-user-config|领域知识 + 用户配置域|可转 B 级|
|27|04-运行流程/查询回答流程.md|map|low|kb-04-运行流程-查询回答流程|src-20260623-kb-flow-query-answer|运行流程 + 查询回答流程|可转 B 级|
|28|04-运行流程/健康检查流程.md|map|low|kb-04-运行流程-健康检查流程|src-20260623-kb-flow-health-check|运行流程 + 健康检查流程|可转 B 级|
|29|04-运行流程/任务生命周期.md|map|low|kb-04-运行流程-任务生命周期|src-20260623-kb-flow-task-lifecycle|运行流程 + 任务生命周期|可转 B 级|
|30|04-运行流程/资料吸收流程.md|map|low|kb-04-运行流程-资料吸收流程|src-20260623-kb-flow-ingestion|运行流程 + 资料吸收流程|可转 B 级|

## 3. 可执行性判断

|范围|数量|建议|
|---|---:|---|
|根文件|4|保留候选，不自动写入|
|00-规范|3|可进入 B 级补 frontmatter|
|01-状态|5|可进入 B 级补 frontmatter|
|02-项目总览|6|可进入 B 级补 frontmatter|
|03-领域知识|8|可进入 B 级补 frontmatter|
|04-运行流程|4|可进入 B 级补 frontmatter|

## 4. 下一步转化建议

- `SID-B01-P1`：先执行 26 个非根文件的 `source_id` 补齐。
- `SID-B01-P2`：根文件单独确认后再处理。
- 执行前需要再次读取目标文件 frontmatter，确保没有用户并发修改。
- 执行后需要更新 `inventory.md` 或生成新的 `post-inventory.md`，避免旧清单与实际状态混用。

## 5. 阶段性结论

- SID-B01 的 30 个候选 `source_id` 已具备人工复核条件。
- 其中 26 个非根主干页可在确认后转为 B 级写入动作。
- 4 个根文件应继续保持 C 级复核，不建议和普通页面混批。

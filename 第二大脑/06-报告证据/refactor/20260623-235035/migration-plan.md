# migration-plan

- run_id: 20260623-235035
- mode: PLAN_AND_APPLY
- scope: KB_ROOT
- timestamp: 2026-06-23 23:50:35

|operation_id|类型|源路径|目标路径|原因|风险|受影响链接|回滚方式|是否自动执行|哈希|
|---|---|---|---|---|---|---|---|---|---|
|op-001|A|06-报告证据/refactor|06-报告证据/refactor/20260623-235035|创建可回滚审计工作区|low|无|删除本次 run 目录|是|25F98D2769D0C2D569767679A8508F36861FEBEB3A83BE75FD9A2409339CD2F2|
|op-002|A|06-报告证据/refactor/20260623-235035/inventory.md|06-报告证据/refactor/20260623-235035/inventory.md|落盘 inventory 清单|low|inventory/path-map/validation|回滚删除文件或复制快照|是|64BB05AC93C8F87CFFCB9FEFD647D4A002FE7713D1107A185BE99B480553A6A9|
|op-003|A|06-报告证据/refactor/20260623-235035/migration-plan.md|06-报告证据/refactor/20260623-235035/migration-plan.md|落盘迁移计划页|low|execution-log|回滚删除文件或复制快照|是|25F98D2769D0C2D569767679A8508F36861FEBEB3A83BE75FD9A2409339CD2F2|
|op-004|A|06-报告证据/refactor/20260623-235035/path-map.md|06-报告证据/refactor/20260623-235035/path-map.md|落盘路径映射|low|validation-index|回滚删除文件或复制快照|是|C5FB59235309F4489CB512AE695AFDE1564FEC1D49A2510F5F847035F6A72C0B|
|op-005|A|06-报告证据/refactor/20260623-235035/duplicate-clusters.md|06-报告证据/refactor/20260623-235035/duplicate-clusters.md|落盘重复聚类|low|migration-plan|回滚删除文件或复制快照|是|0356ABEB6931C9EFC5325903A0E6880835061B2D7546D71CBF89D294BCB6CFA7|
|op-006|A|06-报告证据/refactor/20260623-235035/execution-log.md|06-报告证据/refactor/20260623-235035/execution-log.md|落盘执行日志|low|日志.md/validation|回滚删除文件或复制快照|是|F2DCDC0406FB9BBE12441F4FB1B7255D4F82A44F09816F7698C42B04F3B56B12|
|op-007|A|06-报告证据/refactor/20260623-235035/validation-report.md|06-报告证据/refactor/20260623-235035/validation-report.md|落盘验证报告|low|index/validation|回滚删除文件或复制快照|是|FD49D86A8B3DD9671A716569F04C2926F7BCD5224913FB88B1FE1792830DD22B|
|op-008|A|06-报告证据/refactor/20260623-235035/unresolved-items.md|06-报告证据/refactor/20260623-235035/unresolved-items.md|落盘未决清单|low|validation-report|回滚删除文件或复制快照|是|AB0B94D6CA0110D8E1AD83CF4C6F637FF88A5F534BAFC7B9C39786A55A8165DC|
|op-009|A|索引.md|索引.md|新增本次重构批次入口|medium|索引入口|回滚本次条目|是|n/a|
|op-010|C|KB_ROOT 全量目录|KB_ROOT 全量目录|补齐 source_id 与 id/source 规则映射|high|frontmatter/链接|人工确认映射后逐条回退|否|n/a|
|op-011|C|所有高风险链接与重复项|KB_ROOT 全量目录|待验证的断链与语义重复聚类后再迁移|high|wiki link/标题/标签|清单复核|否|n/a|
|op-012|B|06-报告证据/refactor/20260623-235035/unresolved-items.md|06-报告证据/refactor/20260623-235035/unresolved-items.md|补齐断链候选说明中的 placeholder 与实际链接状态|low|unresolved-items|恢复原链接文本并保留 C 级边界|是|169C827F239C46C4C3DA1C7963D763135BC414CBC0CE17ABB5A36C042420A89A|
|op-013|B|06-报告证据/refactor/20260623-235035/migration-plan.md|06-报告证据/refactor/20260623-235035/migration-plan.md|补录本次 B/C 分界与执行前置条件（含无破坏回退说明）|low|无|回退本文件文本即可|是|63E50AF77169A6500D6EE91226C9BF8275F528A78192A7D4C5EAFF47BA38AA21|
|op-014|C|KB_ROOT 全量文件（除报告目录）|KB_ROOT 全量文件（除报告目录）|补齐 source_id 映射到统一 `src-YYYYMMDD-author-short`（仅形成待执行清单）|high|frontmatter 字段、index 及 source 引用|清单核验后逐项回退|否|n/a|
|op-015|C|报告-005.md 与其外链目标|报告-005.md 与目标 wiki 页|确认 `../` 目录外链与来源映射边界后再定稿（避免跨实例污染）|high|unresolved-items/validation-report/索引|跨实例边界确认后回滚到本条清单状态|否|n/a|
|op-016|C|SCOPE=KB_ROOT 与外部路径边界|SCOPE=KB_ROOT 与外部路径边界|确认是否展开到 `../第二大脑-95-原始资料`、`D:\Projects\SAAS` 及相关引用的扫描边界|high|执行范围约束文档、validation|不改边界则不执行；如扩展则需新建 run_id 段|否|n/a|

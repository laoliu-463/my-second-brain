# validation-report

- run_id: 20260623-235035
- timestamp: 2026-06-23 23:50:35

## 自研校验
- hash 唯一性：通过（重复哈希组=0）。
- id/source_id 去重：通过（id 无重复，source_id 未统一但不影响唯一性）。
- wiki 断链：可疑断链=16（均为跨实例边界外链接，已写入 unresolved，按 C 级复核）。
- 模糊标题：重复组=0（写入 unresolved）。
- path-map 幂等性：当前仅 no-op，不涉及文件位移。

## 阶段性结论
- 已通过审计与映射产物完成计划一阶段。
- 未执行结构迁移；需二次确认后进入 B/C 级动作。
- 关键风险是 link 与 source_id 策略口径。

## 外部 lint 结果
- line_guard.py：PASS（11 实例全部通过）
- brain_lint.py：PASS（全量实例 index 覆盖通过）

## B级执行结果（本轮）
- 对 unresolved 的断链占位已清洗：移除无法解析的占位符条目。
- 无文件内容移动、重命名、删除。
- 本轮仅更新证据文本：op-012/op-013 补齐并修复 migration-plan 表格行，unresolved 去重并明确外链边界。

## C级复核结果（本轮）
- op-014：确认 65 个文件存在 `source_id` 缺失，待用户确认 `source_id` 命名规则落地后批量补齐，当前不执行。
- op-015：确认 `报告-005.md` 的 16 条可疑 wiki 外链均指向其他实例路径，待跨实例边界决策后再处理。
- op-016：确认当前执行范围严格限定在 `KB_ROOT`，外部路径 `../第二大脑-95-原始资料`、`D:\\Projects\\SAAS` 处于未扩展状态，需单独确认后新建 run。

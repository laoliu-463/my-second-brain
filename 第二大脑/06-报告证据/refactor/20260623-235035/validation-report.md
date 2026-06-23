# validation-report

- run_id: 20260623-235035
- timestamp: 2026-06-23 23:50:35

## 自研校验
- hash 唯一性：通过（重复哈希组=0）。
- id/source_id 去重：通过（id 无重复，source_id 未统一但不影响唯一性）。
- wiki 断链：可疑断链=1（已写入 unresolved）。
- 模糊标题：重复组=0（写入 unresolved）。
- path-map 幂等性：当前仅 no-op，不涉及文件位移。

## 阶段性结论
- 已通过审计与映射产物完成计划一阶段。
- 未执行结构迁移；需二次确认后进入 B/C 级动作。
- 关键风险是 link 与 source_id 策略口径。

## 外部 lint 结果
- line_guard.py：PASS（11 实例全部通过）
- brain_lint.py：PASS（全量实例 index 覆盖通过）

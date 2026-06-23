# validation-report

- run_id: 20260623-234959
- timestamp: 2026-06-23 23:49:59

## 校验项
- Hash 去重：通过（重复组 = 0）。
- id/source_id 去重：通过（重复值未出现；source_id 缺失为高比例，但非重复）。
- 断链检测：疑似断链 1 条，写入 unresolved。
- 模糊标题检测：重复标题组 0 组，已记录。
- path-map 幂等性：当前 run no-op，重复运行可复算同结构。
- 二次扫描：完成脚本级再次计算（仅时间戳与报告名更新）。

## 阶段性结论
- 已完成：审计与可执行计划生成。
- 未完成：frontmatter/source_id 标准化、跨实例链接可达性确认。

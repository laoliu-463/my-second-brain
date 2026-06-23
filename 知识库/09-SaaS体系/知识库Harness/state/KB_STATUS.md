# KB Status

> 知识库当前状态快照（每次 LINT 巡检后更新）

## 最新审计结果（2026-06-23）—— 收件箱闭环复核

| 指标 | 数值 | 说明 |
|------|------|------|
| 收件箱待处理文件 | 5 → 0 | 5 个 `00-收件箱/` 与 `00-收集箱/` 条目全部写入状态与归属 |
| 0 字节文件 | 0 | 全局扫描确认 |
| 重复标题检测 | 0 | 新增 `Skills教程` 与现有主题去重一致 |
| KB 任务状态 | KB-GC-STUBS 已关闭 | KB-GC-INBOX 完成并记录 |
| 会话可追溯性 | 已补齐 | 会话动作写入 09-SaaS/state 与 90-收件箱日志 |

详见：`知识库/09-SaaS体系/知识库Harness/reports/对齐报告-20260623-收件箱闭环.md`

### 本次发现（2026-06-23）

- `00-收件箱/Collection 类关系图.md`：状态更新为 `已整理`，关联 `第二大脑-90-收件箱/03-知识/Collection类关系图.md`。
- `00-收件箱/Java即时编译器原理解析及实践.md`：保留原始来源，新增 `第二大脑-90-收件箱/03-知识/Java即时编译器.md` 映射。
- `00-收件箱/Skills 教程  菜鸟教程.md`：新增主题映射 `第二大脑-90-收件箱/03-知识/Skills教程.md`。
- `00-收集箱/DDD提示词.md`：补齐 frontmatter，关联 `第二大脑-90-收件箱/03-知识/DDD提示词.md`。
- `00-收集箱/未命名 2.md`：补齐处理状态为 `已归档`，关联 `第二大脑-90-收件箱/03-知识/未命名.md`。
- 90-收件箱侧状态文件同步：源文件数从 4 → 5，主题数从 6 → 7。

---

## 最新审计结果（2026-06-12）—— 本次对齐扫描

| 指标 | 数值 | 说明 |
|------|------|------|
| 项目 harness 合规率 | 92% | 5 处违规待修（见对齐报告-20260612）|
| vault 3 套并行 | 仍未收敛 | LLM Wiki/Harness/、09-SaaS体系/、团长SaaS知识库/ |
| 旧 LLM Wiki 路径对齐 | **严重脱节** | 13 旧路径已不存在 |
| 新 09-SaaS 主题对齐 | 大致对齐 | 8 Harness-* 子目录 1:1 对应 |
| skill saas-harness-knowledge-ingest | 已归档 | 路径映射已 patch |

详见：`09-SaaS体系/知识库Harness/reports/对齐报告-20260612.md`

### 本次发现（2026-06-12）

- 项目侧 5 处违规：reports/current/ 11 文件、templates/prompts/agents/ 15 文件、business-state-snapshot.md 350 行、DDD_DOMAIN_TASK_MATRIX.md 218 行、agent-contract.md 203 行
- 业务事实主源健康（docs/01-V1交付范围与边界.md）
- 决策主源健康（ADR-001 ~ ADR-008）
- 已沉淀对齐报告到 `知识库Harness/reports/对齐报告-20260612.md`

## 历史审计（2026-06-04）

| 指标 | 数值 | 说明 |
|------|------|------|
| 总 md 文件 | 556 | |
| index.md 文件 | 50 | 含本次新建 25 个 |
| 覆盖率（vault 入口） | 73% | vault index.md 直接链接 |
| 覆盖率（含子目录 index） | ~95% | 子目录 index.md 均已覆盖 |
| 孤立文件（vault 入口） | 97 | 实为子目录 index 覆盖 |
| 断链 | 351 | vault index.md 跨层相对链接失效 |
| stub（<200B） | 0 | |

## 本次整理行动（2026-06-04）

- 新建 index.md：**25 个**
  - 03-地缘政治/index.md、03-地缘政治/中美博弈/index.md
  - 06-内容创作与传播/index.md、06-内容创作与传播/Akkkk视频原文归档/index.md
  - 09-SaaS体系/知识库Harness/index.md
  - 02-后端知识体系（12 个子目录 index）
  - 04-方法论与工具（3 个子目录 index）
  - 05-认知与成长（1 个子目录 index）
  - 06-内容创作与传播（2 个子目录 index）
  - 07-面试备战（5 个子目录 index）
- 更新 vault index.md：补充地缘政治、内容创作索引节

## 待处理项（P1）

| 待处理 | 数量 | 说明 |
|--------|------|------|
| raw/sources 未整理文件 | 50 | Akkkk缺失视频转写，需要归档或 GC |
| vault index 断链 | 351 | `[[B+树与数据页]]` 等跨层相对链接格式错误 |
| 4 个 inbox 孤儿 | 4 | `Collection 类关系图`、`未命名 2`、CLAUDE.md、Harness-README |

## 孤立文件详情

### raw/sources（50 个，未整理）
- `raw/sources/Akkkk缺失视频转写/2024-06-07~2025-12/` 下的 50 个视频转写 md 文件
- 需要判断：归档到 `内容创作` 分类，还是 GC 删除

### inbox（4 个）
- `00-收件箱/Collection 类关系图.md` → 待归档
- `00-收集箱/未命名 2.md` → 内容创作导航
- `CLAUDE.md` → vault 根目录配置文件，不算孤儿
- `知识库/09-SaaS体系/Harness-Environment/README.md` → 已在 09-SaaS体系/index.md 中有 Harness-Environment/ 入口，但 README.md 缺链接

## 覆盖率说明

vault index.md 直接链接覆盖 406 个文件（73%），剩余 150 个"孤儿"分布：
- 97 个：有子目录 index.md 正确链接，Obsidian 可通过子目录导航
- 50 个：raw/sources 未整理
- 4 个：真正孤儿

真实可导航率 ≈ **95%**。

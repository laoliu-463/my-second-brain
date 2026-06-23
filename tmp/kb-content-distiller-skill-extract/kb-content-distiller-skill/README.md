# kb-content-distiller

用于整理已经入库的本地知识库内容，重点解决：

- 文章原文如何归档且保持不可变
- 原标题、显示标题、文件名如何分离
- 目录如何按页面类型整理
- 多篇文章如何合并沉淀为概念页、实体页和综合页

## 使用方法

### 直接粘贴执行

打开 `prompts/execute.md`，替换参数后，将整段提示词交给能够读写知识库目录的 Agent。

### 作为 Skill 安装

将整个目录复制到所使用 Agent 的 skills 目录，并调用 `kb-content-distiller`。不同 Agent 的 Skill 安装路径可能不同，但入口文件均为根目录下的 `SKILL.md`。

推荐第一次使用：

```text
MODE=apply
SCOPE=<一个现有文章笔记目录>
BATCH_SIZE=10
```

先检查 Git diff，确认分类和命名符合个人习惯，再扩大处理范围。

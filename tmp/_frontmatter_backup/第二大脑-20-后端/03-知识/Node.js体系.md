# Node.js体系.md

> Node.js 体系。源：`知识库/02-后端知识体系/04-Node.js体系/` 4 md。

## 1. 文件

| 文件 | 行数 | 主题 |
|---|---:|---|
| 深入浅出Node.js.md | 131 | 进阶 |
| nodebook.md | 21 | 入门 |
| javascript高级程序设计.md | 21 | JS 基础（与 JavaScript体系 重复）|
| index.md | 9 | 索引 |

## 2. 关键主题

- 事件循环（libuv）
- 模块系统（CommonJS / ESM）
- Stream / Buffer
- 子进程
- 性能分析（v8-profiler、clinic.js）

## 3. 项目 V1 实际使用

- 仓库根 `package.json`：Playwright E2E + npm scripts
- frontend：Vue 3 / Vite，依赖 npm
- 当前**不用 Node.js 后端**（后端是 Spring Boot）

## 4. 关联

- [[JavaScript体系]]
- [[../02-总览/项目概览]]

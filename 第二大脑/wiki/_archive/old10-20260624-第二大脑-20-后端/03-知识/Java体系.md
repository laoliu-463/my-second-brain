---
id: kb-backend-03-知识-Java体系
type: concept
title: 'Java体系'
original_title: 'Java体系'
aliases: []
status: active
source_id: ''
created: 2026-06-24
updated: 2026-06-24
---

# Java体系.md

> Java 体系知识入口。源：`知识库/02-后端知识体系/03-Java体系/` 99 md。
> 大量是书摘（每书 131 行模板），核心是 Java 基础 + 集合 + 并发 + JVM + Spring。

## 1. 子分类

| 子分类 | 文件 | 备注 |
|---|---|---|
| Java 基础 | Java基本数据类型 / 标识符与关键字 / 注释 / 包装类型 / 移位运算符 | 入门语法 |
| Java 面向对象 | 成员变量与局部变量 / 静态与实例变量 / 方法重载与重写 / equals与hashCode | OOP 基础 |
| Java 集合 | Collection类关系图 | 集合体系图 |
| Java 高级 | Java_8_实战 / Java核心技术卷2 | 函数式 / 高级特性 |
| Spring | Spring实战(第4版) / Spring_MVC+MyBatis企业应用实战 | 企业开发 |
| Java 即时编译 | Java即时编译器原理解析及实践 / JIT编译器详解 | JVM JIT |
| 抖店业务体系 | 抖店团长SaaS-业务体系/ 6 个 | V1 业务镜像 |

## 2. 重点知识

- **Collection 类关系图**：Collection → List/Set/Queue → ArrayList/LinkedList/HashSet/TreeSet 等
- **equals 与 hashCode**：必须同时重写；Object 规范
- **Java 包装类型**：自动装箱/拆箱、缓存池（Integer -128~127）
- **Java 移位运算符**：<< / >> / >>>（无符号右移）
- **JIT 编译器**：C1 客户端、C2 服务端；分层编译；OSR

## 3. 关键文件路径

- `知识库/02-后端知识体系/03-Java体系/Collection类关系图.md` — 集合体系
- `知识库/02-后端知识体系/03-Java体系/Java中equals与hashCode.md` — 246 行
- `知识库/02-后端知识体系/03-Java体系/Java即时编译器原理解析及实践.md` — 741 行
- `知识库/02-后端知识体系/03-Java体系/JIT编译器详解.md` — 343 行
- `知识库/02-后端知识体系/03-Java体系/02-计算机基础/JIT编译器详解.md`

## 4. 抖店业务体系（V1 镜像）

`知识库/02-后端知识体系/03-Java体系/抖店团长SaaS-业务体系/` 含 6 个文件：
- 01-V1交付范围与边界.md（53 行）
- 02-业务闭环总览.md（58 行）
- 03-业绩计算链路.md（34 行）
- 03-寄样交作业链路.md（33 行）
- 03-招商主链路.md（34 行）
- 03-渠道主链路.md（41 行）
- 03-管理主链路.md（33 行）

## 5. ⚠️ DDD实战-团长SaaS系统/（V2.2 旧方案，已废弃）

`知识库/02-后端知识体系/03-Java体系/DDD实战-团长SaaS系统/` **40 个 md，标记 [DEPRECATED-V2.2]**

- 01-28：领域设计、模型、SOP、TDD、认证授权、抖店集成、样品、招商结算、达人、商品、爬虫、数据库、前端技术栈、Maven、独家、审计、Provider、Webhook、归因重放、脚本、V1对照、FastAPI蓝图
- 28-32：代码图谱、风险清单、权限、测试、部署、real-pre审查
- 46-49：权限、测试、部署、real-pre 审查

**原因**：项目当前是 V1（Spring Boot + 模块化单体 + PostgreSQL + Docker Compose），不使用 FastAPI、不启用独家达人/商家、不做毛利。这些是 V2.2 完整方案的拆解，**只作历史背景**，不可作为 V1 事实。

**关联**：与项目侧 `D:\Projects\SAAS\docs\01-V1交付范围与边界.md` 冲突时，以 V1 为准。

## 6. 关联

- [[../01-状态/资料来源]]
- [[JavaScript体系]]
- [[Node.js体系]]

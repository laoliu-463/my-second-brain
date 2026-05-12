---
title: Java标识符与关键字
tags: [Java, 标识符, 关键字, 语法基础]
created: 2026-05-12
updated: 2026-05-12
sources: []
---

# Java 标识符与关键字

---

## 一、Java 标识符

### 定义

用于命名类、方法、变量、常量、接口等元素。编译器通过标识符识别程序中的各个组成部分。

### 命名规则

| 规则 | 说明 |
|------|------|
| 只能包含字母、数字、`_`、`$` | 第一个字符不能是数字 |
| 不能与 Java 关键字冲突 | 关键字是保留的特殊单词 |
| 区分大小写 | `totalScore` ≠ `TotalScore` |
| 推荐用驼峰命名 | 类名/接口名首字母大写，方法/变量首字母小写 |

### 使用场景

| 类型 | 示例 | 类比 |
|------|------|------|
| 类名 | `public class Main` | 菜谱名称 |
| 方法名 | `public void sayHello()` | 做菜步骤名称 |
| 变量名 | `int totalScore` | 原料名称 |
| 常量名 | `final double PI` | 特殊固定材料 |

---

## 二、Java 关键字

### 定义

Java 语言保留的特殊单词，用于语法结构、控制流程、修饰符、异常处理等。**不能用作标识符**。

### 分类与结构化展示

#### (1) 类与接口结构

| 关键字 | 用途 |
|--------|------|
| `class` | 定义类 |
| `interface` | 定义接口 |
| `enum` | 定义枚举 |
| `extends` | 类继承 |
| `implements` | 接口实现 |
| `package` | 包声明 |
| `import` | 导入包 |

#### (2) 方法与控制流

| 关键字 | 用途 |
|--------|------|
| `if`, `else` | 条件判断 |
| `switch`, `case`, `default` | 多分支选择 |
| `for`, `while`, `do` | 循环 |
| `break`, `continue` | 控制循环流程 |
| `return` | 返回方法结果 |

#### (3) 修饰符

| 关键字 | 用途 |
|--------|------|
| `public`, `private`, `protected` | 访问权限 |
| `static` | 静态成员 |
| `final` | 不可变（变量/方法/类） |
| `abstract` | 抽象类/方法 |
| `synchronized` | 同步方法 |
| `volatile` | 变量可见性 |
| `transient` | 序列化忽略字段 |
| `native` | 本地方法 |
| `strictfp` | 浮点计算严格模式 |

#### (4) 异常处理

| 关键字 | 用途 |
|--------|------|
| `try`, `catch`, `finally` | 异常捕获 |
| `throw`, `throws` | 抛出异常 |

#### (5) 其他

| 关键字 | 用途 |
|--------|------|
| `this` | 当前对象引用 |
| `super` | 父类对象引用 |
| `instanceof` | 类型判断 |
| `new` | 创建对象 |
| `void` | 无返回值方法 |
| `assert` | 断言 |
| `yield` | switch 表达式返回值 |
| `record`, `sealed`, `permits` | JDK 14+ 新特性关键字 |

---

## 三、面试常问

1. 区分标识符和关键字
2. 标识符命名规则
3. 关键字分类及作用
4. Java 新增关键字（record、sealed、permits）

---

## 相关概念

- [[Java注释]] - Java 注释类型
- [[09-Java基础与JVM体系]] - Java 运行机制

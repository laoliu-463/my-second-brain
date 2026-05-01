---
title: JVM、JDK 与 JRE
tags: [Java, JVM, JDK, JRE, 计算机基础]
created: 2026-05-01
updated: 2026-05-01
sources: [00-收件箱/JVM JDK JRE.md]
---

# JVM、JDK 与 JRE

## 概述

JVM、JDK 和 JRE 描述的是 Java 程序从源码到运行的不同层次：`javac` 负责编译，JVM 负责执行字节码，JDK 则是完整开发工具集，JRE 是运行环境的最小集合。

## Java 程序从编写到运行

Java 程序通常以 `.java` 源文件开始。开发者在 IDE 或编辑器中编写代码后，源码本身不能直接被操作系统执行，需要先通过 Java 编译器 `javac` 编译为 `.class` 字节码文件。

字节码不是直接面向某一种操作系统的机器指令，而是一种中间表示。不同操作系统对底层机器码的要求不同，因此 Java 通过 JVM 来屏蔽平台差异。JVM 会把 `.class` 字节码加载进来，再解释执行或即时编译为当前操作系统能够识别的机器码，最终完成程序运行。

这个过程可以概括为：

`Java 源码(.java) -> javac 编译 -> 字节码(.class) -> JVM 执行 -> 操作系统机器码`

## JVM 是什么

JVM（Java Virtual Machine，Java 虚拟机）是 Java 跨平台能力的核心。它的作用不是编写代码，而是负责加载、校验和执行 `.class` 字节码文件。由于不同平台都有各自的 JVM 实现，因此同一份 Java 字节码可以在不同系统上运行，这就是“Write Once, Run Anywhere”的基础。

## JRE 是什么

JRE（Java Runtime Environment，Java 运行环境）是运行 Java 程序所需的环境集合。它通常包含 JVM 以及 Java 基础类库，适合“只运行、不开发”的场景。如果一台机器只需要执行 Java 程序，而不需要编译源码，那么安装 JRE 就足够。

## JDK 是什么

JDK（Java Development Kit，Java 开发工具包）是面向开发者的完整工具集。它包含 JRE，同时还提供 `javac`、`javadoc`、`jdb` 等开发、调试和文档生成工具。因此，开发 Java 程序通常安装 JDK，而不仅仅是 JRE。

## 三者关系

三者的关系可以理解为：

- `JDK = JRE + 开发工具`
- `JRE = JVM + Java 运行所需类库`
- `JVM` 是真正执行字节码的运行核心

因此：

- 写 Java 程序，要装 JDK
- 运行 Java 程序，至少要有 JRE
- 程序真正跨平台运行，依赖的是 JVM

## 相关概念

- [[B+树与数据页]]
- [[agent]]

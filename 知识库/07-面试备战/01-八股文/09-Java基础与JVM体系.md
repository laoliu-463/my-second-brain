---
title: Java基础与JVM体系
tags: [Java, JVM, JDK, JRE, 八股文, 跨平台]
created: 2026-05-12
updated: 2026-05-12
sources: []
---

# Java基础与JVM体系

> 核心问题：Java 代码到底是怎么跑起来的？理解这个，JVM/JDK/JRE 三者关系、类加载、Spring Boot 启动流程都会变简单。

---

## 一、核心链路：一句话描述

```
.java → javac编译 → .class字节码 → JVM执行 → 机器码 → CPU运行
```

---

## 二、用"做菜"理解 Java 运行

**你是厨师，Java 代码就是菜谱。**

但问题是：CPU 这台"外国厨师"看不懂中文菜谱（Java）。

所以需要一个**翻译官**——这就是 JVM。

---

## 三、每一步详细拆解

### 第1步：写 `.java` 源文件

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

本质：**给人看的文本**，CPU 完全不认识。

### 第2步：编译（`javac`）

```bash
javac Main.java
```

`javac` 把人类语言翻译成 **JVM 能看懂的语言**，生成 `Main.class`。

### 第3步：`.class` 是什么

`.class` **不是** Windows 代码、Linux 代码或 CPU 代码。

`.class` 是：**Java 统一标准语言**——就像"世界通用英文"，所有 JVM 都认识。

这就是 Java 跨平台的真正原因：

> **不是 Java 神奇，而是不同系统上都有 JVM。**

同一个 `.class` 文件，Windows JVM 能跑，Linux JVM 也能跑，Mac JVM 还能跑。

### 第4步：JVM 执行

```bash
java Main    # 注意：运行的是 .class，不是 .java
```

JVM 把 `.class` 翻译成**当前系统能执行的机器码**，最后 CPU 才能真正运行。

---

## 四、JVM 本质

**JVM = 超级翻译官**

- Windows JVM → 翻译成 Windows 机器码
- Linux JVM → 翻译成 Linux 机器码
- Mac JVM → 翻译成 Mac 机器码

**Java 跨平台的原因：不是 Java 代码跨平台，而是 JVM 跨平台。**

---

## 五、JDK / JRE / JVM 三者关系

### 用"厨房"类比

| 概念 | 厨房类比 | 包含内容 | 功能 |
|------|---------|---------|------|
| **JVM** | 真正做菜的厨师 | 只有厨师本人 | 真正执行字节码 |
| **JRE** | 完整厨房 | 厨师 + 锅碗瓢盆 | 能运行 Java，但不能开发 |
| **JDK** | 厨师学校 | 厨房 + 教材 + 培训工具 | 能开发 Java |

### 数值关系

```
JDK = JRE + 开发工具（javac、javadoc、jdb...）
JRE = JVM + Java 基础类库（String、List、Thread...）
JVM 负责执行
```

因此：**JDK > JRE > JVM**

---

## 六、高频八股问答

### Q1：为什么 Java 能跨平台？

> 不是因为 Java 代码本身特殊，而是因为不同操作系统都有各自的 JVM 实现。JVM 把同一份字节码翻译成当前系统能认识的机器码。

### Q2：`.java` 和 `.class` 的区别？

> `.java` 是源码文本，给程序员看；`.class` 是字节码，给 JVM 看。运行 `java` 命令执行的是 `.class`，不是 `.java`。

### Q3：JDK 和 JRE 的区别？

> JRE 只能运行 Java 程序（包含 JVM + 基础类库）；JDK 是完整开发工具包（JRE + javac 等开发工具），既能运行也能开发。

### Q4：JVM 的作用是什么？

> 加载字节码、校验安全性、解释执行或 JIT 编译为机器码。是 Java"Write Once, Run Anywhere"的核心。

---

## 七、厨房类比记忆法（三分钟永久记住）

想象你要做一顿饭：

- **JVM** = 你本人，真正动手做菜的厨师
- **JRE** = 厨房，有厨师、有锅碗瓢盆，能做饭，但没法教你做新菜
- **JDK** = 厨师学校，有厨房、有教材、有培训工具，能让你从不会到会

所以：
- 想**运行** Java 程序 → 需要 JRE（至少有个厨房）
- 想**开发** Java 程序 → 需要 JDK（需要厨师学校）
- 想**真正执行** → 最终靠 JVM（厨师本人）

---

## 八、后续延伸

理解 JVM 执行流程后，这些内容都会变简单：

- [[JVM、JDK 与 JRE|（深入）JVM 内存结构与类加载机制]]
- [[Spring实战（第4版）|Spring Boot 如何利用 JVM 启动]]
- [[Java 8 实战|Java 8 JIT 编译与性能优化]]

---

## 相关概念

- [[08-计算机网络核心知识点]] - HTTP/TCP 等网络八股
- [[07-PostgreSQL高级特性与工程实践]] - 数据库八股
- [[06-Redis缓存与分布式锁]] - Redis 八股
- [[JVM、JDK 与 JRE|后端基础：JVM、JDK 与 JRE]] - 计算机基础目录下的详细版

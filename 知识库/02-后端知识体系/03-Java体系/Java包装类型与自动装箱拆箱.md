---
title: Java包装类型与自动装箱拆箱
tags: [Java, 包装类型, 自动装箱, 自动拆箱, Integer缓存, equals]
created: 2026-05-12
updated: 2026-05-12
sources: []
---

# Java 包装类型与自动装箱拆箱

> 核心关系：== 和 equals、自动装箱拆箱、Integer 缓存、集合泛型、空指针防范都以此为基础。

---

## 一、8 种基本类型对应的包装类型

| 基本类型 | 包装类型 |
|---------|---------|
| `byte` | `Byte` |
| `short` | `Short` |
| `int` | `Integer` |
| `long` | `Long` |
| `float` | `Float` |
| `double` | `Double` |
| `char` | `Character` |
| `boolean` | `Boolean` |

**一句话**：
> 基本类型：直接存值。包装类型：把值包成对象。

---

## 二、类比理解

- `int a = 10;`：盒子 a 里直接放着数字 10
- `Integer b = 10;`：盒子 b 里放的不是数字本身，而是一个"装着 10 的对象"的地址

---

## 三、为什么需要包装类型

集合要求存对象，不能存基本类型：

```java
ArrayList<int> list = new ArrayList<>();     // ✗ 错误
ArrayList<Integer> list = new ArrayList<>(); // ✓ 正确
```

---

## 四、基本类型 vs 包装类型

| 对比点 | 基本类型 | 包装类型 |
|--------|---------|---------|
| 本质 | 值 | 对象 |
| 存储 | 直接存值 | 存对象引用 |
| 默认值 | `0` | `null` |
| 是否有方法 | 无 | 有（可调用方法） |
| 用于集合泛型 | 不能 | 能 |
| 性能 | 更高 | 稍低 |
| 表示 null | 不能 | 能 |

---

## 五、默认值陷阱

```java
class User {
    int age;       // 默认 0
    Integer score; // 默认 null
}

Integer score = null;
int s = score;   // 自动拆箱 → NullPointerException
```

---

## 六、自动装箱和自动拆箱

| 过程 | 操作 | 本质 |
|------|------|------|
| 装箱 | `Integer b = a;`（int→Integer） | `Integer.valueOf(a)` |
| 拆箱 | `int a = b;`（Integer→int） | `b.intValue()` |

---

## 七、== 比较规则（重要）

| 比较场景 | 结果 | 原因 |
|---------|------|------|
| `int a=10; int b=10; a==b` | `true` | 基本类型比值 |
| `Integer a=10; int b=10; a==b` | `true` | Integer 自动拆箱成 int，比值 |
| `Integer a=127; Integer b=127; a==b` | `true` | 命中 Integer 缓存，地址相同 |
| `Integer a=128; Integer b=128; a==b` | `false` | 超出缓存范围，创建新对象，比地址 |
| `Integer a=128; Integer b=128; a.equals(b)` | `true` | equals 比值 |

---

## 八、Integer 缓存机制

`Integer.valueOf()` 对 **-128 到 127** 做了缓存：

```java
Integer a = 127;  // 命中缓存，返回同一对象
Integer b = 127;  // 命中缓存，返回同一对象
a == b;            // true，地址相同

Integer a = 128;   // 超出缓存，创建新对象
Integer b = 128;   // 超出缓存，再创建新对象
a == b;            // false，地址不同
```

> 缓存范围可通过 `-XX:AutoBoxCacheMax=` 配置（部分 JVM）。

---

## 九、安全比较

```java
Integer a = null;
Integer b = 10;

// a.equals(b);  // NullPointerException
Objects.equals(a, b);  // false，更安全
```

---

## 十、面试标准回答

**Q：基本类型和包装类型的区别？**

> 基本类型直接存储值，如 int 存具体数字，效率高但不能表示 null，也不能用于集合泛型。包装类型是对应对象，可以表示 null，可以调用方法，也可用于集合。二者通过自动装箱（valueOf）和自动拆箱（xxxValue）互相转换。

**Q：Integer a = 127; Integer b = 127; a == b 为什么是 true？**

> 自动装箱调用 `Integer.valueOf`，valueOf 对 -128 到 127 做了缓存，a 和 b 指向同一个缓存对象，== 比较地址所以为 true。

**Q：128 呢？**

> 超出缓存范围会创建新对象，== 比较地址返回 false。**包装类型比较值推荐用 equals 或 Objects.equals。**

---

## 相关概念

- [[Java基本数据类型]] - 8 种基本类型
- [[Java移位运算符]] - 位运算
- [[09-Java基础与JVM体系]] - Java 运行机制

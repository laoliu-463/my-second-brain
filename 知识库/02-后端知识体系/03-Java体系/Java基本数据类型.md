---
title: Java基本数据类型
tags: [Java, 基本数据类型, 变量, 内存, 整数, 浮点, 字符, 布尔]
created: 2026-05-12
updated: 2026-05-12
sources: []
---

# Java 基本数据类型

> 为什么重要：基本数据类型是理解变量、内存、包装类、自动装箱拆箱、== 和 equals、集合泛型、JVM 栈帧的基础。

---

## 一、8 种基本数据类型

```
基本数据类型
├── 整数型：byte、short、int、long
├── 浮点型：float、double
├── 字符型：char
└── 布尔型：boolean
```

---

## 二、整数型

| 类型 | 占用空间 | 取值范围大概 | 常见用途 |
|------|---------|------------|---------|
| `byte` | 1 字节 | -128 ~ 127 | 文件、网络字节数据 |
| `short` | 2 字节 | -3万 ~ 3万 | 较少直接用 |
| `int` | 4 字节 | -21亿 ~ 21亿 | **最常用整数** |
| `long` | 8 字节 | 非常大 | ID、时间戳、大数字 |

**注意**：`long` 赋值时建议加 `L`，否则数字过大会报错（默认当 int 处理）。

```java
long userId = 10000000000L;  // ✓ 加 L
long num = 10000000000;       // ✗ 可能溢出报错
```

---

## 三、浮点型

| 类型 | 占用空间 | 精度 | 常见用途 |
|------|---------|------|---------|
| `float` | 4 字节 | 精度较低 | 特殊场景 |
| `double` | 8 字节 | 精度更高 | **默认小数类型** |

**注意**：`float` 赋值必须加 `F`，否则默认当 double 报错。

```java
float price = 99.9F;   // ✓
double rate = 0.05;     // ✓ 默认 double
```

### float 和 double 不适合金额精确计算

```java
double a = 0.1;
double b = 0.2;
System.out.println(a + b);  // 输出 0.30000000000000004
```

原因：计算机用二进制表示小数，有些十进制小数无法精确表示（类似 1/3 = 0.333...）。

**金额计算用 `BigDecimal`。**

---

## 四、字符型：char

```java
char gender = '男';
char grade = 'A';
char ch = '中';
```

- 使用**单引号**
- 占 **2 字节**（Unicode 字符集，支持中文）
- 字符串用**双引号**：`String s = "A";`

---

## 五、布尔型：boolean

只有两个值：`true` 和 `false`。

```java
boolean isLogin = true;
if (isLogin) { ... }
```

**注意**：Java 里 boolean 不能用 0 和 1 替代（和 C 语言不同）。

```java
boolean flag = 1;   // ✗ 错误
boolean flag = true; // ✓ 正确
```

---

## 六、默认值

类成员变量（未赋值）有默认值；局部变量**没有默认值**，必须先赋值再使用。

| 类型 | 默认值 |
|------|--------|
| `byte/short/int/long` | `0` / `0L` |
| `float/double` | `0.0F` / `0.0` |
| `char` | `'\u0000'` |
| `boolean` | `false` |

---

## 七、基本类型 vs 引用类型

| | 基本数据类型 | 引用数据类型 |
|--|-----------|------------|
| 变量里存什么 | **直接是值** | **对象地址** |
| 示例 | `int a = 10;` | `User u = new User();` |
| 类比 | 盒子里直接放苹果 | 盒子里放纸条，纸条写着苹果在哪 |

---

## 八、记忆口诀

```
整数：byte short int long（1/2/4/8 字节）
小数：float double（4/8 字节）
字符：char（2字节，单引号）
布尔：boolean（true/false）

int 最常用，double 默认。
long 加 L，float 加 F。
char 单引号，String 双引号。
基本类型存值，引用类型存地址。
```

---

## 九、面试标准回答

**Q：Java 有哪些基本数据类型？**

> Java 有 8 种基本数据类型，分四类：
> - 整数型：byte、short、**int**、long
> - 浮点型：**float**、**double**
> - 字符型：char
> - 布尔型：boolean
> 其中 int 是最常用的整数，double 是默认的小数类型。

**Q：基本类型和引用类型的区别？**

> 基本类型变量直接存储值，例如 `int a = 10` 里 a 就是数值 10；
> 引用类型变量存储的是对象地址，例如 `User u = new User()` 里 u 保存的是对象在堆中的地址。

---

## 相关概念

- [[Java标识符与关键字]] - Java 语法基础
- [[Java移位运算符]] - 位运算场景
- [[09-Java基础与JVM体系]] - Java 运行机制
- [[JVM、JDK 与 JRE]] - JVM 内存模型基础

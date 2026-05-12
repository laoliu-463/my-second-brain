---
title: Java中==与equals及hashCode
tags: [Java, equals, hashCode, ==, String, Integer, HashMap, 面试高频]
created: 2026-05-12
updated: 2026-05-12
sources: []
---

# Java 中 == 与 equals 及 hashCode

> 核心关系：基本类型 vs 引用类型、String、Integer 缓存、HashMap/HashSet 全部串起来问。

---

## 一、核心结论

```
==：
  基本类型 → 比较值
  引用类型 → 比较地址

equals：
  默认（Object）→ 比较地址
  重写后（如 String、Integer）→ 比较内容值
```

> 一句话：== 看两边是不是"同一个东西"；equals 通常看两个东西"内容是否一样"。

---

## 二、== 比较

### 基本类型

```java
int a = 10;
int b = 10;
a == b;  // true，基本类型存值，直接比值

char c = 'A';
int i = 65;
c == i;  // true，char 底层是 Unicode 数值，65 = 'A'
```

### 引用类型

```java
User u1 = new User();
User u2 = new User();
u1 == u2;  // false，两个不同对象，比的是地址
```

类比：两张纸条（引用）上写的房间号（地址）不同。

---

## 三、Object 默认 equals

`Object.equals()` 默认实现：

```java
public boolean equals(Object obj) {
    return this == obj;  // 默认比较地址
}
```

没有重写的类，`equals` 和 `==` 效果一样。

---

## 四、String 的 == 和 equals

```java
String s1 = "abc";
String s2 = "abc";
s1 == s2;       // true，字面量共享字符串常量池同一对象

String s3 = new String("abc");
String s4 = new String("abc");
s3 == s4;        // false，new 出来的是两个不同对象
s3.equals(s4);   // true，String 重写了 equals，比较内容
```

| 比较方式 | `s1 == s2`（字面量 vs 字面量） | `s3 == s4`（new vs new） |
|---------|------|------|
| `==` | true | false |
| `equals` | true | true |

---

## 五、Integer 的 == 和 equals

```java
Integer a = 127;
Integer b = 127;
a == b;       // true，命中 Integer 缓存（-128~127）

Integer c = 128;
Integer d = 128;
c == d;       // false，超出缓存范围，创建不同对象
c.equals(d);  // true，Integer 重写了 equals，比较 int 值
```

---

## 六、基本类型和包装类型混合比较

```java
int a = 128;
Integer b = 128;
a == b;  // true，Integer 自动拆箱成 int

Integer c = null;
int d = 1;
c == d;  // NullPointerException，c 拆箱时调用 intValue()，null 不能调用
```

---

## 七、空指针问题

```java
String s = null;
s.equals("abc");       // NullPointerException，null 不能调用方法
"abc".equals(s);       // false，安全写法
Objects.equals(s, "abc"); // true，推荐，内部处理了 null
```

---

## 八、equals 和 hashCode 的关系

### 核心规则

```
如果 equals 为 true → hashCode 必须相同
如果 hashCode 相同 → equals 不一定为 true（哈希冲突）
```

### 为什么重写 equals 必须重写 hashCode

`HashMap` / `HashSet` 查找逻辑：

```
1. 先用 hashCode 定位桶位置
2. 再用 equals 判断是否真正相等
```

如果只重写 equals 不重写 hashCode：

```
两个内容相等的对象，equals 为 true，但 hashCode 不同
→ 被放到不同桶里
→ HashSet 去重失效，HashMap 查找失败
```

### 类比

- `hashCode()` = 小区楼号（快速定位）
- `equals()` = 查身份证（确认身份）

先按楼号找人，再核对身份证。

---

## 九、自定义对象比较内容

```java
class User {
    private String name;
    private int age;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        User user = (User) o;
        return age == user.age && Objects.equals(name, user.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
}
```

---

## 十、面试标准回答

**Q：== 和 equals 的区别？**

> == 是运算符，基本类型比较值，引用类型比较地址。equals 是 Object 方法，默认比较地址，但 String、Integer 等类重写了 equals 比较内容值。判断对象内容相等用 equals，判断是否同一引用用 ==。

**Q：String 为什么用 equals 不用 ==？**

> String 是引用类型，== 比较的是地址而不是内容。String 重写了 equals 用来比较内容值，所以判断字符串内容相等应使用 equals。

**Q：Integer 127 和 128 的区别？**

> Integer.valueOf 对 -128 到 127 有缓存。127 命中缓存指向同一对象，== 为 true；128 超出缓存创建不同对象，== 为 false。内容比较推荐用 equals。

**Q：equals 为什么可能空指针？**

> equals 是对象方法，调用方为 null 时会 NPE。应使用常量调用 equals（"abc".equals(s)）或 Objects.equals(a, b)。

**Q：为什么重写 equals 要重写 hashCode？**

> HashMap/HashSet 先用 hashCode 定位，再用 equals 判断相等。如果 equals 相等但 hashCode 不同，会导致哈希集合去重失效、查找逻辑错误。Java 规定：equals 为 true 时 hashCode 必须相同。

---

## 十一、代码题汇总

| 题 | 代码 | 结果 | 原因 |
|----|------|------|------|
| 1 | `int a=10; int b=10; a==b` | true | 基本类型比值 |
| 2 | `Integer a=10; int b=10; a==b` | true | 自动拆箱 |
| 3 | `Integer a=127; Integer b=127; a==b` | true | 命中缓存 |
| 4 | `Integer a=128; Integer b=128; a==b` | false | 超出缓存 |
| 5 | `Integer a=128; Integer b=128; a.equals(b)` | true | equals 比值 |
| 6 | `String s1="abc"; String s2="abc"; s1==s2` | true | 常量池同一对象 |
| 7 | `new String("abc") == new String("abc")` | false | 两个 new 对象 |
| 8 | `new String("abc").equals(new String("abc"))` | true | equals 比内容 |
| 9 | `Integer a=null; int b=1; a==b` | NPE | 自动拆箱 |
| 10 | `s.equals("abc")` 其中 s=null | NPE | null 调用方法 |

---

## 十二、一句话记忆

```
==：基本类型比值，引用类型比地址。
equals：默认比地址，重写后比内容。
hashCode：给哈希集合找位置；equals：确认是不是同一个。
```

---

## 相关概念

- [[Java基本数据类型]] - 基本类型 vs 引用类型
- [[Java包装类型与自动装箱拆箱]] - Integer 缓存原理
- [[Java移位运算符]] - HashMap 扰动函数 `hash ^ (hash >>> 16)`
- [[09-Java基础与JVM体系]] - Java 运行机制与内存

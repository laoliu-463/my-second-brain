# Collection类关系图.md

> Java 集合框架类关系图。源：`00-收件箱/Collection 类关系图.md` + `知识库/02-后端知识体系/03-Java体系/Collection类关系图.md` 96 行。

## 1. 顶级接口

- Collection → List / Set / Queue
- Map（独立顶级）

## 2. List

- ArrayList（数组 / 快查 / 慢增删）
- LinkedList（双向链表 / 慢查 / 快增删）
- Vector（线程安全 / 慢）

## 3. Set

- HashSet（HashMap + 假值）
- LinkedHashSet（插入序）
- TreeSet（红黑树 / 排序）

## 4. Map

- HashMap（数组 + 链表 / 红黑树）
- LinkedHashMap（插入序）
- TreeMap（红黑树 / 排序）
- Hashtable（线程安全 / 慢）
- ConcurrentHashMap（分段锁 / CAS）

## 5. Queue

- LinkedList
- PriorityQueue（堆）
- ArrayDeque（数组双端队列）

## 6. 关联

- [[../第二大脑-20-后端/03-知识/Java体系]]

---
title: "Java即时编译器原理解析及实践"
created: 2026-05-12
updated: 2026-06-27
source_level: none
source: "https://tech.meituan.com/2020/10/22/java-jit-practice-in-meituan.html"
outputs:
  - 知识库/90-来源与映射/Java即时编译器原理解析及实践来源映射.md
  - 知识库/sources/src-20201022-meituan-jit-practice.md
  - 知识库/02-后端知识体系/02-计算机基础/JIT编译器详解.md
tags:
  - JVM
  - JIT
  - Java
  - 性能优化
---
# Java即时编译器原理解析及实践（旧来源入口）

> 兼容旧入口。主来源页已迁到 [[知识库/sources/src-20201022-meituan-jit-practice|Java JIT 编译器原理与实践]]；知识结论统一沉淀到 [[JIT编译器详解]]。

## 一句话结论

JVM 在启动阶段优先解释执行，运行期通过热点检测触发 JIT 编译，并依赖 C1/C2 分层编译在启动速度与峰值性能之间自适应平衡。

## 来源中的核心点

- 运行链路：`javac` 编译静态字节码；运行时解释器先运行，热点代码再交由 JIT 编译。
- 双编译器模型：C1（启动快、局部优化）与 C2（全局优化、峰值性能），JDK 9 起补充 Graal。
- 分层编译：通过五层状态在解释执行和不同编译层之间动态切换。
- 热点触发：方法调用计数器 + 循环回边计数共同决定编译时机。
- IR 与优化：HIR/LIR、Sea-of-Nodes、SSA、GVN、内联、逃逸分析是提升点。

## 知识沉淀指向

- 知识页主入口：[[JIT编译器详解]]
- 主来源页：[[知识库/sources/src-20201022-meituan-jit-practice|Java JIT 编译器原理与实践]]
- 关系追踪入口：[[知识库/90-来源与映射/Java即时编译器原理解析及实践来源映射|Java即时编译器原理解析及实践来源映射]]
- 原文：`raw/sources/src-20201022-meituan-jit-practice/original.md`

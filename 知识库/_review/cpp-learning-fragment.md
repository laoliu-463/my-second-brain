---
title: "cpp-learning-fragment"
type: review
status: review
created_at: 2026-06-27
updated_at: 2026-06-27
source_level: none
sources: []
raw_evidence: []
related: []
tags: []
maintainers:
  - codex
confidence: 0.5
---
string字符串
substr(1,3)从下标1开始截取3个字符
注意数组下标从零开始
append("welcome",3); 将前字符串的前3个字符追加到原字符串后
insert(1,3，“w”) 在原字符串的下表1位置之前插入三个w字符
assign("welcome",3) 将原字符串改为传入的字符串前三个字符
和一个具体对象关联的是实例函数，也就是成员函数
静态变量被所有类共享
C++列表初始化a(1),b(2),c(3)
C++中值传递只改变副本，不改变真正变量值
动态内存释放，数组使用delete[]p,对象使用delete p
指针常量不能修改值  常量指针不能修改指针指向，从右往左读，只针对当前指针及其变量，之前声明的变量不受影响
对于数组指针 *list代表数组首元素  
vector[0]是空的，必须要赋值
push.back(5)将数字放入vector尾部
v[0]或v.,at[0]是获取第一个元素
模版类可以参与继承也可以继承其他模版类，静态成员每个实例都有一份
模版函数传参必须一致
stream.seekp()用于移动文件指针
tellp用于获取当前输出文件指针位置
|函数|含义|
|---|---|
|`good()`|判断流状态是否正常|
|`eof()`|判断是否到文件末尾|
|`fail()`|判断是否发生逻辑错误，例如读取失败|
|`bad()`|判断是否发生严重 I/O 错误|
|`clear()`|清除错误状态|
friend可以声明友元函数和类来访问私有成员
抽象函数=纯虚函数  virtual 返回类型 函数名(参数列表) = 0;
构造函数先父类后子类，析构函数相反
virtual动态绑定
构造函数和析构函数不会被继承
子类对象可以当父类对象使用




---
title: tcp源码分析
author: W. Richard Stevens / 机械工业出版社
tags: [tcp, ip, 网络协议, 源码分析]
category: 02-后端知识体系/06-网络与分布式
source: "C:/Users/caojianing/Downloads/NotebookLM可上传书籍/tcp源码分析.pdf"
created: 2026-05-03
updated: 2026-05-03
type: book-summary
---

# tcp源码分析

**作者/版本：** W. Richard Stevens / 机械工业出版社

## 一句话描述
TCP/IP 协议实现源码分析，从源码角度理解协议细节（网络与分布式分类）。

## 核心内容

共 239 页，161 条目录。

### 目录索引（部分）

- 准备部分（第7页）
  - 用户层TCP（第8页）
  - 探寻tcp_prot，地图get~（第8页）
  - RFC（第9页）
    - RFC793 : Transmission Control Protocol（第9页）
    - RFC1323 : TCP Extensions for High Performance（第11页）
    - RFC1337 : TIME-WAIT Assassination Hazards in TCP（第13页）
    - RFC2018 : TCP Selective Acknowledgement Options（第14页）
    - RFC2525 : Known TCP Implementation Problems（第15页）
    - RFC3168 : The Addition of Explicit Congestion Notification (ECN) to IP（第15页）
    - RFC6937 : Proportional Rate Reduction for TCP（第17页）
    - RFC7413 : TCP Fast Open(Draft)（第17页）
- 网络子系统相关核心数据结构（第18页）
  - 网络子系统数据结构架构（第19页）
  - sock底层数据结构（第19页）
    - sock_common（第19页）
    - sock（第21页）
    - crequestsock（第25页）
    - sk_buff（第25页）
    - msghdr（第30页）
  - inet层相关数据结构（第30页）
    - cipoptions（第30页）
    - cinetrequestsock（第31页）
    - cinetconnectionsockafops（第31页）
    - cinetconnectsock（第32页）
    - cinettimewaitsock（第33页）
    - csockaddr  sockaddrin（第34页）
    - ip_options（第35页）
  - 路由相关数据结构（第35页）
    - cdstentry（第35页）
    - crtable（第37页）
    - flowi（第38页）
  - TCP层相关数据结构（第38页）
    - tcphdr（第38页）
    - ctcpoptionsreceived（第39页）
    - ctcpsacktagstate（第40页）
    - ctcpsock（第40页）
    - ctcpfastopencookie（第45页）
    - ctcpfastopenrequest（第45页）
    - ctcprequestsock（第45页）
    - ctcpskbcb（第46页）
- TCP输出（第48页）
  - 数据发送接口（第48页）
    - ctcpsendmsg（第48页）
    - ctcpsendmsgfastopen（第53页）
    - TCP Push操作（第54页）
  - 输出到IP层（第56页）
    - ctcpwritexmit（第56页）
    - tcp_transmit_skb（第58页）
    - tcp_select_window(struct sk_buff *skb)（第61页）
- TCP输入（第65页）
  - Linux内核网络数据接收流程概览（第65页）
  - 自底向上调用与自顶向下调用（第66页）
    - 自底向上处理（第66页）
    - 自顶向下处理（第72页）
- TCP建立连接（第84页）
  - TCP主动打开-客户（第85页）
    - 基本流程（第85页）
    - 第一次握手：构造并发送SYN包（第85页）
    - 第二次握手：接收SYN+ACK包（第90页）
    - 第三次握手:发送ACK包（第101页）
  - TCP被动打开-服务器（第102页）
    - 基本流程（第102页）
    - 第一次握手：接受SYN段（第103页）
    - 第二次握手：发送SYN+ACK段（第111页）
    - 第三次握手：接收ACK段（第115页）
- TCP拥塞控制（第121页）
  - 拥塞控制实现（第122页）
    - 拥塞控制状态机（第122页）
    - 显式拥塞通知(ECN)（第126页）
    - 拥塞控制状态的处理及转换（第129页）
  - 拥塞控制引擎（第132页）
    - 接口（第132页）
    - CUBIC拥塞控制算法（第136页）
- TCP释放连接（第147页）
  - tcp_shutdown（第148页）
  - 主动关闭（第148页）
    - 第一次握手:发送FIN（第148页）
    - 第二次握手:接收ACK（第154页）
    - 第三次握手:接受FIN（第159页）
    - 第四次握手:发送ACK（第161页）
    - 同时关闭（第163页）
    - TIME_WAIT（第164页）
  - 被动关闭（第166页）
    - 基本流程（第166页）
    - 第一次握手:接收FIN（第166页）
    - 第二次握手:发送FIN的ACK（第169页）
    - 第三次握手:发送FIN（第169页）
    - 第四次握手:接收FIN的ACK（第169页）
- 非核心代码分析（第170页）
  - BSD Socket层（第173页）
    - cmsgflag（第173页）
    - 数据报类型（第173页）
    - Sock CheckSum（第174页）
    - SK Stream（第177页）
    - cskstreamwaitconnect（第177页）
    - cpskbmaypull（第178页）
  - Inet（第178页）
    - cinetstreamconnect（第178页）
    - cinethashconnect  inethashconnect（第180页）
  - ... 共 161 条目录，完整版见源文件

> 完整目录见源文件 PDF。


## 实践应用

## 相关资源
- 源文件：C:/Users/caojianing/Downloads/NotebookLM可上传书籍/tcp源码分析.pdf

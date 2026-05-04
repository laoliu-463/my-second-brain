---
title: Java核心技术卷2高级特性
author: Cay S. Horstmann / 机械工业出版社
tags: [java, corejava, 高级特性]
category: 02-后端知识体系/03-Java体系
source: "raw/sources/Java核心技术卷2高级特性原书第10版.pdf"
created: 2026-05-03
updated: 2026-05-03
type: book-summary
---

# Java核心技术卷2高级特性

**作者/版本：** Cay S. Horstmann / 机械工业出版社

## 一句话描述
Java 核心技术卷 II，涵盖并发编程、网络编程、JDBC、XML处理等高级特性。

## 核心内容

共 1127 页，327 条目录。

### 目录索引（部分）

- Core Java® Volume II—Advanced Features, Tenth Edition（第2页）
  - Book Description（第2页）
  - Contents（第4页）
  - Preface（第10页）
    - About This Book（第10页）
    - Conventions（第12页）
  - Chapter 1. The Java SE 8 Stream Library（第14页）
    - 1.1. From Iterating to Stream Operations（第15页）
    - 1.2. Stream Creation（第18页）
    - 1.3. The filter, map, and flatMap Methods（第21页）
    - 1.4. Extracting Substreams and Combining Streams（第23页）
    - 1.5. Other Stream Transformations（第24页）
    - 1.6. Simple Reductions（第25页）
    - 1.7. The Optional Type（第27页）
      - 1.7.1. How to Work With Optional Values（第27页）
      - 1.7.2. How Not to Work With Optional Values（第29页）
      - 1.7.3. Creating Optional Values（第29页）
      - 1.7.4. Composing Optional Value Functions with flatMap（第30页）
    - 1.8. Collecting Results（第33页）
    - 1.9. Collecting into Maps（第38页）
    - 1.10. Grouping and Partitioning（第42页）
    - 1.11. Downstream Collectors（第44页）
    - 1.12. Reduction Operations（第49页）
    - 1.13. Primitive Type Streams（第51页）
    - 1.14. Parallel Streams（第58页）
  - Chapter 2. Input and Output（第63页）
    - 2.1 Input/Output Streams（第63页）
      - 2.1.1 Reading and Writing Bytes（第64页）
      - 2.1.2 The Complete Stream Zoo（第67页）
      - 2.1.3 Combining Input/Output Stream Filters（第72页）
    - 2.2 Text Input and Output（第76页）
      - 2.2.1 How to Write Text Output（第77页）
      - 2.2.2 How to Read Text Input（第79页）
      - 2.2.3 Saving Objects in Text Format（第80页）
      - 2.2.4 Character Encodings（第84页）
    - 2.3 Reading and Writing Binary Data（第87页）
      - 2.3.1 The DataInput and DataOutput interfaces（第87页）
      - 2.3.2 Random-Access Files（第90页）
      - 2.3.3 ZIP Archives（第95页）
    - 2.4 Object Input/Output Streams and Serialization（第99页）
      - 2.4.1 Understanding the Object Serialization File Format（第106页）
      - 2.4.2 Modifying the Default Serialization Mechanism（第113页）
      - 2.4.3 Serializing Singletons and Typesafe Enumerations（第115页）
      - 2.4.4 Versioning（第117页）
      - 2.4.5 Using Serialization for Cloning（第120页）
    - 2.5 Working with Files（第122页）
      - 2.5.1 Paths（第123页）
      - 2.5.2 Reading and Writing Files（第125页）
      - 2.5.3 Creating Files and Directories（第127页）
      - 2.5.4 Copying, Moving, and Deleting Files（第128页）
      - 2.5.5 Getting File Information（第130页）
      - 2.5.6 Visiting Directory Entries（第132页）
      - 2.5.7 Using Directory Streams（第134页）
      - 2.5.8 ZIP File Systems（第138页）
    - 2.6 Memory-Mapped Files（第139页）
      - 2.6.1 The Buffer Data Structure（第148页）
      - 2.6.2 File Locking（第151页）
    - 2.7 Regular Expressions（第153页）
  - Chapter 3. XML（第167页）
    - 3.1 Introducing XML（第167页）
      - 3.1.1 The Structure of an XML Document（第170页）
    - 3.2 Parsing an XML Document（第173页）
    - 3.3 Validating XML Documents（第189页）
      - 3.3.1 Document Type Definitions（第190页）
      - 3.3.2 XML Schema（第199页）
      - 3.3.3 A Practical Example（第202页）
    - 3.4 Locating Information with XPath（第220页）
    - 3.5 Using Namespaces（第228页）
    - 3.6 Streaming Parsers（第231页）
      - 3.6.1 Using the SAX Parser（第232页）
      - 3.6.2 Using the StAX Parser（第238页）
    - 3.7 Generating XML Documents（第243页）
      - 3.7.1 Documents without Namespaces（第243页）
      - 3.7.2 Documents with Namespaces（第243页）
      - 3.7.3 Writing Documents（第244页）
      - 3.7.4 An Example: Generating an SVG File（第245页）
      - 3.7.5 Writing an XML Document with StAX（第248页）
    - 3.8 XSL Transformations（第258页）
  - Chapter 4. Networking（第272页）
    - 4.1 Connecting to a Server（第272页）
      - 4.1.1 Socket Timeouts（第277页）
      - 4.1.2 Internet Addresses（第279页）
    - 4.2 Implementing Servers（第281页）
      - 4.2.1 Serving Multiple Clients（第285页）
      - 4.2.2 Half-Close（第290页）
    - 4.3 Interruptible Sockets（第291页）
    - 4.4 Getting Web Data（第298页）
      - 4.4.1 URLs and URIs（第299页）
      - 4.4.2 Using a URLConnection to Retrieve Information（第301页）
      - 4.4.3 Posting Form Data（第311页）
    - 4.5 Sending E-Mail（第322页）
  - Chapter 5. Database Programming（第327页）
    - 5.1 The Design of JDBC（第328页）
      - 5.1.1 JDBC Driver Types（第328页）
      - 5.1.2 Typical Uses of JDBC（第330页）
    - 5.2 The Structured Query Language（第331页）
    - 5.3 JDBC Configuration（第338页）
      - 5.3.1 Database URLs（第339页）
      - 5.3.2 Driver JAR Files（第339页）
      - 5.3.3 Starting the Database（第340页）
  - ... 共 327 条目录，完整版见源文件

> 完整目录见源文件 PDF。


## 实践应用

## 相关资源
- 源文件：C:/Users/caojianing/Downloads/NotebookLM可上传书籍/Java核心技术卷2高级特性原书第10版.pdf

---
id: kb-raw-06-报告-full-content-audit
type: evidence
title: 'raw 全量内容审计'
original_title: 'raw 全量内容审计'
aliases: []
status: active
source_id: ''
created: 2026-06-24
updated: 2026-06-24
---

# raw 全量内容审计

- 审计时间：2026-06-24 09:00:53 +0800
- 范围：`raw/` 下全部文件。
- 说明：本报告区分“已抽取正文”和“仅可读取元数据”。视频、旧 Office 二进制、扫描型 PDF 不被伪装成已读完正文。

## 总览

- 原始文件总数：319
- 原始文件总大小：3274929353 bytes
- 已抽取/读取文本字符数：18313852
- 内容清单：`第二大脑-95-原始资料/06-报告/full-content-audit-20260624-085952/raw-content-inventory.jsonl`
- 抽取文本目录：`第二大脑-95-原始资料/06-报告/full-content-audit-20260624-085952/extracts/`

## 按解析状态统计

- `text_extracted`：234
- `media_metadata_only`：46
- `ocr_needed`：22
- `unsupported_binary`：10
- `error`：6
- `metadata_only`：1

## 按文件类型统计

- `.pdf`：144
- `.md`：63
- `.json`：46
- `.mp4`：46
- `.ppt`：9
- `.docx`：5
- `.csv`：3
- `.doc`：1
- `.pptx`：1
- `.zip`：1

## 按来源集合统计

- `sources/Akkkk缺失视频转写`：92
- `sources/中美博弈系列`：83
- `assets/Akkkk缺失视频`：46
- `sources/大学物理复习`：17
- `sources/抖音团长SaaS设计文档`：13
- `sources/醒与悟系列`：8
- `sources/操作系统练习题`：5
- `sources/Akkkk缺失视频媒体信息.csv`：1
- `sources/Akkkk缺失视频清单.csv`：1
- `sources/Akkkk缺失视频转写汇总.csv`：1
- `sources/CSS揭秘.pdf`：1
- `sources/Java 8 实战.pdf`：1
- `sources/JavaScript权威指南.pdf`：1
- `sources/JavaScript高级程序设计（第4版 中文高清）.pdf`：1
- `sources/Java核心技术卷2高级特性原书第10版.pdf`：1
- `sources/JSP_Servlet学习笔记(第2版).pdf`：1
- `sources/Linux多线程服务端编程_陈硕.pdf`：1
- `sources/Linux网络编程.pdf`：1
- `sources/Linux高性能服务器编程.pdf`：1
- `sources/nodebook.pdf`：1
- `sources/Pro Git中文PDF版.pdf`：1
- `sources/Redis开发与运维(付磊).pdf`：1
- `sources/Rudin.pdf`：1
- `sources/Spring MVC+MYBatis企业应用实战.pdf`：1
- `sources/Spring实战中文版（第4版）.pdf`：1
- `sources/src-20201022-meituan-jit-practice`：1
- `sources/src-20260512-pdai-collection-relations`：1
- `sources/src-20260524-code-review-graph-saas-flow`：1
- `sources/src-20260617-runoob-skills-tutorial`：1
- `sources/src-20260623-local-ddd-refactor-prompts`：1
- `sources/tcp源码分析.pdf`：1
- `sources/Thinking+in+Java+4th+Edition（JAVA编程思想 第四版 英文版）.pdf`：1
- `sources/Vue.js实战.pdf`：1
- `sources/Wireshark网络分析就这么简单.pdf`：1
- `sources/你不知道的JavaScript（上卷）.pdf`：1
- `sources/你不知道的JavaScript（下卷）.pdf`：1
- `sources/你不知道的JavaScript（中卷）.pdf`：1
- `sources/操作系统设计与实现.pdf`：1
- `sources/数学分析原理(Rudin_着)中文版.pdf`：1
- `sources/数据结构与算法分析_C++语言描述.4th.Mark_Allen_Weiss.2016.pdf`：1
- `sources/数据结构与算法分析：C语言描述_原书第2版_高清版.pdf`：1
- `sources/概率导论(第2版).pdf`：1
- `sources/深入React技术栈.pdf`：1
- `sources/深入浅出Node.js.pdf`：1
- `sources/深入理解 TypeScript.pdf`：1
- `sources/深入理解Nginx模块开发与架构解析第2版.pdf`：1
- `sources/深入理解计算机系统（中文清晰）.pdf`：1
- `sources/现代操作系统_原书第4版[高清扫描版].pdf`：1
- `sources/离散数学及其应用_原书第7版_,(美)KENNETH_H.ROSEN著_,P793.pdf`：1
- `sources/程序员的自我修养_链接装载与库.pdf`：1
- `sources/算法图解.pdf`：1
- `sources/算法导论第三版.pdf`：1
- `sources/算法竞赛入门经典训练指南.pdf`：1
- `sources/算法竞赛入门经典（第2版）---紫书.pdf`：1
- `sources/线性代数及其应用(原书第5版)_by_[美]_戴维_C.雷_[美]_史蒂文_R.雷_[美]_朱迪_J.麦克唐纳.pdf`：1
- `sources/编码——隐匿在计算机软硬件背后的语言上.pdf`：1
- `sources/编译原理.pdf`：1
- `sources/背包九讲.pdf`：1
- `sources/自己动手写操作系统.pdf`：1
- `sources/计算机科学导论(原书第3版).pdf`：1
- `sources/计算机组成_结构化方法_中文扫描第6版.pdf`：1
- `sources/鸟哥的Linux私房菜-基础学习篇(第四版)高清完整书签PDF版.pdf`：1

## 解析器统计

- `fitz`：138
- `plain-text`：63
- `ffprobe`：46
- `json-text`：46
- `unsupported-old-office`：10
- `unknown`：6
- `python-docx`：5
- `csv-text`：3
- `python-pptx`：1
- `zipfile`：1

## 需要人工补充 OCR/转写/转换的文件

| 文件 | 状态 | 原因 | 建议 |
|---|---|---|---|
| `raw/assets/Akkkk缺失视频/2024-06-07_7377747575333604646.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2024-06-14_7380335910769970483.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2024-07-26_7395890775659236645.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2024-07-29_7396987833925373211.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2024-09-04_7410718705157508379.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-01-03_7455539127992192308.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-07-30_7532750123852877115.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-07-30_7532839269434920251.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-08-14_7538408246748679482.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-09-16_7550684898451246394.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-09-19_7551813673960230201.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-09-21_7552535689632484666.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-09-28_7555142563020901691.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-09-30_7555898067313184060.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-10-16_7561862240354569529.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-10-28_7566250228207291685.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-11-06_7569669504134259449.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-11-20_7574817898611755129.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-11-24_7576308702840648699.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-12-04_7580006065296655461.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-12-13_7583383067910655281.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2025-12-23_7587121122480819505.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-01-05_7591872500649264625.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-01-06_7592256110880804601.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-01-08_7592999616145222769.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-01-12_7594492965419411825.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-01-17_7596327728018866041.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-01-21_7597837288257799609.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-01-31_7601572356120794597.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-02-05_7603426762958019825.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-02-13_7606379661292435825.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-02-19_7608602943714280059.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-03-12_7616349448264191738.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-03-17_7618256677389298105.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-03-19_7618971297758939057.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-03-20_7619331136589680122.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-03-26_7621577194427270522.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-03-29_7622601323007698417.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-04-01_7623827381749074289.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-04-04_7624923136303694769.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-04-07_7626036975644832241.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-04-15_7628999549637906809.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-04-20_7630848041818143857.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-04-24_7632368715938312433.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-04-26_7633037423778412538.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/assets/Akkkk缺失视频/2026-04-30_7634534925051462001.mp4` | `media_metadata_only` | 视频只能读取容器元数据，未做语音/画面转写 | 使用转写工具生成文字稿后再沉淀来源页 |
| `raw/sources/JavaScript权威指南.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/JSP_Servlet学习笔记(第2版).pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/Linux高性能服务器编程.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/Rudin.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/Spring MVC+MYBatis企业应用实战.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/Vue.js实战.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/中美博弈系列/001-中美博弈+资本收割模型.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/中美博弈系列/002-中美博弈+资本收割模型.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/中美博弈系列/003-中美博弈+资本收割模型.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/中美博弈系列/004-中美博弈+资本收割模型.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/中美博弈系列/005-中美博弈+资本收割模型.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/中美博弈系列/006-中美博弈+资本收割模型.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/中美博弈系列/007-中美博弈+资本收割模型.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/大学物理复习/ch14－4.ppt` | `unsupported_binary` | 当前本地无可靠旧 Office/二进制正文解析器 | 转换为 PDF/DOCX/PPTX 或人工导出文本后复扫 |
| `raw/sources/大学物理复习/ch14－7.ppt` | `unsupported_binary` | 当前本地无可靠旧 Office/二进制正文解析器 | 转换为 PDF/DOCX/PPTX 或人工导出文本后复扫 |
| `raw/sources/大学物理复习/ch9-2.ppt` | `unsupported_binary` | 当前本地无可靠旧 Office/二进制正文解析器 | 转换为 PDF/DOCX/PPTX 或人工导出文本后复扫 |
| `raw/sources/大学物理复习/ch9-3 (1).ppt` | `unsupported_binary` | 当前本地无可靠旧 Office/二进制正文解析器 | 转换为 PDF/DOCX/PPTX 或人工导出文本后复扫 |
| `raw/sources/大学物理复习/ch9-3.ppt` | `unsupported_binary` | 当前本地无可靠旧 Office/二进制正文解析器 | 转换为 PDF/DOCX/PPTX 或人工导出文本后复扫 |
| `raw/sources/大学物理复习/第二次课2023.ppt` | `unsupported_binary` | 当前本地无可靠旧 Office/二进制正文解析器 | 转换为 PDF/DOCX/PPTX 或人工导出文本后复扫 |
| `raw/sources/大学物理复习/第五次课.ppt` | `unsupported_binary` | 当前本地无可靠旧 Office/二进制正文解析器 | 转换为 PDF/DOCX/PPTX 或人工导出文本后复扫 |
| `raw/sources/大学物理复习/第八次 课.ppt` | `unsupported_binary` | 当前本地无可靠旧 Office/二进制正文解析器 | 转换为 PDF/DOCX/PPTX 或人工导出文本后复扫 |
| `raw/sources/大学物理复习/第四次课.ppt` | `unsupported_binary` | 当前本地无可靠旧 Office/二进制正文解析器 | 转换为 PDF/DOCX/PPTX 或人工导出文本后复扫 |
| `raw/sources/大学物理复习/练习与提高/2025春-大学物理（A）I练习与提高（刚体力学部分) .pdf` | `error` | ValueError: document closed or encrypted | 查看错误后单独处理 |
| `raw/sources/大学物理复习/练习与提高/2025春-大学物理（A）I练习与提高（期末考试模拟试卷) (2).pdf` | `error` | ValueError: document closed or encrypted | 查看错误后单独处理 |
| `raw/sources/大学物理复习/练习与提高/2025春-大学物理（A）I练习与提高（狭义相对论部分)  (1).pdf` | `error` | ValueError: document closed or encrypted | 查看错误后单独处理 |
| `raw/sources/大学物理复习/练习与提高/2025春-大学物理（A）I练习与提高（狭义相对论部分)  (2).pdf` | `error` | ValueError: document closed or encrypted | 查看错误后单独处理 |
| `raw/sources/大学物理复习/练习与提高/2025春-大学物理（A）I练习与提高（狭义相对论部分)  .pdf` | `error` | ValueError: document closed or encrypted | 查看错误后单独处理 |
| `raw/sources/大学物理复习/练习与提高/2025春-大学物理（A）I练习与提高（质点力学部分).pdf` | `error` | ValueError: document closed or encrypted | 查看错误后单独处理 |
| `raw/sources/操作系统练习题/页面置换练习.doc` | `unsupported_binary` | 当前本地无可靠旧 Office/二进制正文解析器 | 转换为 PDF/DOCX/PPTX 或人工导出文本后复扫 |
| `raw/sources/数学分析原理(Rudin_着)中文版.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/数据结构与算法分析：C语言描述_原书第2版_高清版.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/概率导论(第2版).pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/现代操作系统_原书第4版[高清扫描版].pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/离散数学及其应用_原书第7版_,(美)KENNETH_H.ROSEN著_,P793.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/算法导论第三版.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/编译原理.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/自己动手写操作系统.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |
| `raw/sources/醒与悟系列/05-醒与悟3.0.pdf` | `ocr_needed` | PDF 未抽取到可搜索文本，疑似扫描件 | OCR 后复扫并绑定同一 source_id |

## URL 候选

- 含 URL 候选的文件数：78
- 未将 URL 候选自动写为 canonical_url，除非原文件存在明确 frontmatter 字段。

## 可执行整理结论

- 可以确定的整理动作：保留现有目录不移动 raw；以 `raw-原始文件索引.md` 和本内容审计作为总入口。
- 可以自动沉淀的来源：Markdown、JSON、CSV、DOCX、PPTX、可抽取文本 PDF。
- 暂不能自动沉淀的来源：MP4、旧 DOC/PPT、扫描型 PDF、解析错误文件。
- 知识页引用不能仅按标题或目录名批量绑定；需要原文中的 `source_id`、明确 raw_path、canonical_url 或人工确认。
- 下一步若要真正“重构目录”，应先按本报告的 `status` 分批：文本可抽取文件一批，OCR 文件一批，视频转写一批，旧 Office 转换一批。

## 抽样证据

- `raw/assets/Akkkk缺失视频/2024-06-07_7377747575333604646.mp4`：status=`media_metadata_only`，parser=`ffprobe`，text_chars=0，sha256=`e976969639e656d6d412fc6bb5fde5935ebc074026d236696c7621813cf332e8`
- `raw/assets/Akkkk缺失视频/2024-06-14_7380335910769970483.mp4`：status=`media_metadata_only`，parser=`ffprobe`，text_chars=0，sha256=`1fe79a4adc19436ecc8495db24e4b309e7c9602cd0b81c0a36b99e7caa36c452`
- `raw/assets/Akkkk缺失视频/2024-07-26_7395890775659236645.mp4`：status=`media_metadata_only`，parser=`ffprobe`，text_chars=0，sha256=`14fe472995e3a6417f46af0362189f17c4e44322951b50a5113e0c5031005e09`
- `raw/assets/Akkkk缺失视频/2024-07-29_7396987833925373211.mp4`：status=`media_metadata_only`，parser=`ffprobe`，text_chars=0，sha256=`f66b669bcd47a7a12b15f629e5decc3843b85e8025c2d369819f8ab151548c52`
- `raw/assets/Akkkk缺失视频/2024-09-04_7410718705157508379.mp4`：status=`media_metadata_only`，parser=`ffprobe`，text_chars=0，sha256=`7e31bdff9327d8611089b3cc75c32b25692ce5f65074b3f52fa95a3a4dfab446`
- `raw/assets/Akkkk缺失视频/2025-01-03_7455539127992192308.mp4`：status=`media_metadata_only`，parser=`ffprobe`，text_chars=0，sha256=`4fa612e6369cb89069c9981c1c05fb33bd1e6a80612a8acc2a8ea969918e0590`
- `raw/assets/Akkkk缺失视频/2025-07-30_7532750123852877115.mp4`：status=`media_metadata_only`，parser=`ffprobe`，text_chars=0，sha256=`5b7ece027422600c258347c946c3aa0a62d202d944a99add3d775edfdf3b3285`
- `raw/assets/Akkkk缺失视频/2025-07-30_7532839269434920251.mp4`：status=`media_metadata_only`，parser=`ffprobe`，text_chars=0，sha256=`b1f19e38165476c563ff239efd696252747833ff3b771ddc90386adb7c1840fc`
- `raw/assets/Akkkk缺失视频/2025-08-14_7538408246748679482.mp4`：status=`media_metadata_only`，parser=`ffprobe`，text_chars=0，sha256=`febe0a9e4c58cbc8a0a9b572243ac82940d38752af2f8ee35c417888a3a014ea`
- `raw/assets/Akkkk缺失视频/2025-09-16_7550684898451246394.mp4`：status=`media_metadata_only`，parser=`ffprobe`，text_chars=0，sha256=`e9ce534ce93439a28e03293cc6208be6eece557030f5511d9ae55c9b0076f77d`

---
title: VPN搭建完整指南
tags: [VPN, 网络, 基础设施, 实用工具]
created: 2026-04-27
updated: 2026-04-27
sources: [raw/sources/VPN搭建指南/VPN 搭建完整指導書 - 2026 Reality Edition.md]
---

# VPN搭建完整指南

## 概述

一份完整的个人 VPN 节点搭建指南，采用 2026 年最新的 VLESS+Reality 协议，实现最高抗封锁等级的科学上网。采用 X-ui 可视化面板管理，零基础 30 分钟可完成部署。

## 核心技术

- **协议**：VLESS+Reality（淘汰 Outline/Shadowsocks，无须购买域名，通过借用大厂网站进行流量伪装）
- **管理面板**：X-ui（3x-ui 分支）
- **伪装目标**：`www.microsoft.com:443`

## 必要准备

| 需求 | 方案 |
|------|------|
| 境外支付 | 境外信用卡（Visa/Mastercard）；无卡可在某宝搜「Vultr 礼品卡代充值」约 ¥70 换 $10 |
| 电子邮箱 | Gmail/Outlook/QQ 邮箱；无海外邮箱可买「Gmail 成品号」约 ¥5-15 |
| 终端设备 | Windows 10+ / macOS 10.14+ / Android / iOS |
| 时间 | 约 30 分钟 |

## VPS 服务商选择

| 服务商 | 月均成本 | 特点 |
|--------|----------|------|
| Vultr | $5-6 | 支付宝友好，界面简单，东京节点 IP 易被封锁 |
| 搬瓦工 (BandwagonHost) | $50+/年 | 华人老牌，CN2 GIA 线路速度快，支持支付宝 |
| Oracle Cloud | 免费 | 永久免费两台 ARM 小机，申请门槛高，有封号风险 |
| RackNerd / Hostinger | $2-3 | 超低价，稳定性和 IP 品质一般 |

> 推荐地区：美国西海岸（洛杉矶/西雅图）、新加坡、日本大阪。避免 Vultr 东京节点（IP 封锁重灾区）。

## 搭建步骤

### 第一步：租用 VPS

1. 在服务商后台创建服务器
2. 系统选 **Ubuntu 22.04 LTS** 或 24.04
3. 配置选 **$5-6/mo**（1 CPU, 1GB RAM）
4. 认证选 **密码方式**，记录 IP 地址和 root 密码

### 第二步：SSH 连接服务器

**Windows**：按 `Win+R` → 输入 `cmd` → `ssh root@服务器IP`

**macOS**：`⌘+空格` 搜索终端 → `ssh root@服务器IP`

提示 `password:` 时粘贴密码（光标不动属正常现象）。

### 第三步：安装 X-ui 面板

```bash
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
```

安装过程设置：
- 面板账户密码：自行设置
- 面板访问端口：10000-65000 之间，如 `23456`

安装完成后访问 `http://服务器IP:23456` 登录后台。

### 第四步：配置 Reality 节点

在 X-ui 后台 **入站列表 (Inbounds)** 中添加：
- 协议：vless
- 端口：443
- Reality：开启
- 目标网站 (Dest)：`www.microsoft.com:443`
- SNI：`www.microsoft.com`
- 点击 **Get New Cert** 自动生成密钥

### 第五步：客户端配置

| 平台 | 推荐客户端 | 导入方式 |
|------|------------|----------|
| Windows | v2rayN / Clash Verge Rev | 复制 `vless://` 链接，`Ctrl+V` 导入 |
| Android | v2rayNG | Google Play 下载，从剪贴板导入 |
| iOS | Shadowrocket（需美区 ID，约 $2.99） | 复制链接自动识别 |

## 常见问题排查

| 症状 | 原因 | 解决 |
|------|------|------|
| certificate has expired | 系统时间偏差 | 确保设备时间与北京标准时间误差 < 1 分钟 |
| 几天后突然断联 | SNI 伪装被针对 | 改用同云厂商域名（如 Oracle 用 oracle.com） |
| X-ui 后台打不开 | 云服务商防火墙拦截 | 在 VPS 控制台防火墙放行对应端口 |

## 成本评估

- **最低成本**（自备卡和邮箱）：¥15-40/月（VPS 费用）
- **启动成本**（无卡无邮箱 + iOS）：约 ¥100（代充 ¥70 + 邮箱 ¥10 + 小火箭 ¥22）

## 相关概念
- [[提示词创作法]] - 提示词工程相关
- [[横纵分析法]] - 研究方法相关

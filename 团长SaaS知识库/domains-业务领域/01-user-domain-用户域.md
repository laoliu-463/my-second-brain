---
kb_id: domains/01-user-domain
title: 用户域
domain: domains
category: domain-user
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - docs/领域/用户域.md
  - backend/src/main/java/com/colonel/saas/service/UserService.java
  - frontend/src/api/user.ts
related_reports: []
forbidden_misread:
  - 6 角色是 V1 全集
  - self/group/all 是 V1 数据范围全集
---

# 用户域（user）

## 1. 用途

提供统一身份与数据范围（self / group / all）能力，**所有其他域查询都依赖本域**。

## 2. V1 必做

- 6 角色：`admin` / `biz_leader` / `biz_staff` / `channel_leader` / `channel_staff` / `ops_staff`
- 4 部门类型：`department` / `recruiter_group` / `channel_group` / `ops_group`
- 数据范围：`self`（仅自己） / `group`（本组） / `all`（全部）
- 用户档案：姓名、手机号、入职、离职、所属部门
- 鉴权：JWT + 角色

## 3. V1 不做

- SSO / OAuth / 第三方登录
- 多租户
- 组织架构图
- 操作审计

## 4. 关键 API

| API | 用途 | 数据范围 |
| --- | --- | --- |
| `GET /api/users/me` | 当前用户 | self |
| `GET /api/users?scope=self\|group\|all` | 用户列表 | 由角色决定 |
| `GET /api/departments` | 部门树 | 受控 |

## 5. 关键实体

- `User`：user_id, name, phone, role, dept_id, status
- `Department`：dept_id, name, type, parent_id
- `RoleScope`：role → 默认 scope

## 6. 验收口径

- 6 角色登录后看到对应菜单
- 数据范围 API 在三种 scope 下返回正确集合
- 跨部门越权访问被拒

## 7. 不变量

> [V1 必做] 用户域统一提供 self / group / all 数据范围。

跨域查询**必须**经过用户域 scope 解析，不得各自实现。

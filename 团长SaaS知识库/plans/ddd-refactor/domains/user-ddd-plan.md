---
kb_id: "KB-PLAN-DDD-DOMAIN-USER"
title: "用户域 DDD 计划"
domain: "user"
category: "ddd_plan"
source_type: "mixed"
freshness: "current"
owner: "harness"
project_root: "D:\\Projects\\SAAS"
kb_root: "D:\\Docs\\Books\\my second brain\\团长SaaS知识库"
last_verified_at: "2026-06-08 13:59:08"
related_files:
  - "D:\\Projects\\SAAS\\docs\\领域"
related_reports:
  - "D:\\Projects\\SAAS\\harness\\reports\\ddd-refactor-master-plan-001-20260608-135908.md"
forbidden_misread:
  - "DDD 重构计划不是立即大规模改代码"
  - "包结构迁移不是第一阶段任务"
  - "重构不等于业务口径变更"
---

# 用户域 DDD 计划

## 1. 当前领域职责

登录认证、用户、角色、菜单、组织、self/group/all 数据范围、用户主数据。

## 2. 当前主要代码位置

auth/service/SysUserService.java、SysRoleService.java、SysMenuService.java、SysDeptService.java；CurrentUserController、SysUserController；SysUserMapper、SysRoleMapper、SysDeptMapper。

## 3. 当前主要 Service / Controller / Mapper

见上一节；本轮仅做只读统计，未修改任何代码。

## 4. 当前 DDD 问题

DataScope 逻辑散落；UserDomainFacade 尚未统一；跨域直接查用户/部门/角色事实；权限越权负例仍需持续补齐。

## 5. 推荐重构方向

先审查 CurrentUser / PermissionContext / DataScopeResolver，再补数据范围测试，最后新增极薄 UserDomainFacade。

## 6. 第一批任务

DDD-AUDIT-USER-001、DDD-TEST-USER-DATASCOPE-001、DDD-FACADE-USER-001

## 7. 禁止先做的事

禁止先迁包；禁止同时改多个领域；禁止把业务修复混入重构；禁止改变接口契约或数据库结构。

## 8. 需要补的测试

mvn -f backend/pom.xml -Dtest=CurrentUserControllerTest,UserMasterDataServiceTest,SysUserServiceTest test

## 9. 验证命令

A 类审查执行 git diff --check + 只读扫描报告。B/C/D 类按任务卡执行 mvn -f backend/pom.xml -Dtest=CurrentUserControllerTest,UserMasterDataServiceTest,SysUserServiceTest test 或更小 targeted tests。

## 10. 相关 KB 领域文档链接

- ../../domains/01-user-domain.md
- [任务矩阵](../02-task-matrix.md)

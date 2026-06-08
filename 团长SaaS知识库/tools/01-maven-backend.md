---
kb_id: tools/01-maven-backend
title: 后端 Maven 工具链
domain: tools
category: backend
project_root: D:\Projects\SAAS
kb_root: D:\Docs\Books\my second brain\团长SaaS知识库
last_verified_at: 2026-06-08
freshness: fresh
owner: harness-kb-001
source_type: harness-derived
related_files:
  - backend/pom.xml
  - backend/src/main/resources
related_reports: []
forbidden_misread:
  - 不得使用 `mvn -U` 频繁升级
  - 不得跨工作区共享 local repo
---

# 后端 Maven 工具链

## 1. 主源

- `backend/pom.xml`（Spring Boot 3.2 + Java 17）

## 2. 关键依赖

| 依赖 | 版本 | 用途 |
| --- | --- | --- |
| spring-boot-starter-web | 3.2.x | REST API |
| spring-boot-starter-data-jpa | 3.2.x | ORM |
| postgresql | 42.7.x | 驱动 |
| mybatis-plus-boot-starter | 3.5.x | 复杂查询 |
| lombok | 1.18.x | 简化 POJO |
| springdoc-openapi | 2.x | OpenAPI 3 |

## 3. 常用命令

```bash
# 单测
mvn test

# 编译
mvn clean compile

# 打包
mvn clean package -DskipTests

# 启动
mvn spring-boot:run

# 单测覆盖率
mvn test jacoco:report
```

## 4. 已知坑

- 升级 Spring Boot 3.2 → 3.3 必须先看 Jakarta EE 兼容
- Lombok 1.18.30+ 在 JDK 17 上需 `-Djps.track.ap.dependencies=false`
- `mvn -U` 频繁升级会丢缓存

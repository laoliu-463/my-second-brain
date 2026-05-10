---
title: 14-Maven依赖与版本清单
tags: [Maven, Java, 依赖管理, SpringBoot]
created: 2026-05-10
updated: 2026-05-10
sources: [pom.xml]
---

# 14-Maven 依赖与版本清单

## 1. 父工程与版本

```xml
<parent>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.5</version>
</parent>
<artifactId>colonel-saas</artifactId>
<version>1.0.0</version>
```

Spring Boot 3.2.5（2024 年初 Release，内置 Jakarta EE 9+/Servlet 5.0）。

## 2. 核心依赖

### 2.1 Spring Boot 原生

| 依赖 | 版本 | 说明 |
|---|---|---|
| `spring-boot-starter-web` | 3.2.5 | REST API + Tomcat |
| `spring-boot-starter-validation` | 3.2.5 | Bean Validation（JSR-380） |
| `spring-boot-starter-data-redis` | 3.2.5 | Redis 连接 + 序列化 |
| `spring-boot-starter-aop` | 3.2.5 | AOP（日志/事务） |
| `spring-boot-starter-actuator` | 3.2.5 | 健康检查端点 |
| `spring-boot-starter-security` | 3.2.5 | Spring Security |

### 2.2 数据库

| 依赖 | 版本 | 说明 |
|---|---|---|
| `mybatis-plus-spring-boot3-starter` | `${mybatis-plus.version}` | MyBatis-Plus（3.8+ 支持 Spring Boot 3） |
| `postgresql` | 内置 HikariCP | PostgreSQL JDBC 驱动 |
| `HikariCP` | 内置 | 连接池（Spring Boot 默认） |

### 2.3 安全与 JWT

| 依赖 | 版本 | 说明 |
|---|---|---|
| `jjwt-api` | 0.12.5 | JWT 签发与验证 |
| `jjwt-impl` | 0.12.5 | JWT 实现 |
| `jjwt-jackson` | 0.12.5 | JWT JSON 序列化 |

### 2.4 工具库

| 依赖 | 版本 | 说明 |
|---|---|---|
| `hutool-all` | `${hutool.version}` | 工具集（HttpRequest/JSON/编码） |
| `jsoup` | 1.17.2 | HTML 解析（爬虫数据处理） |
| `lombok` | `${lombok.version}` | 编译期代码生成 |
| `knife4j-openapi3-jakarta-spring-boot-starter` | `${knife4j.version}` | Swagger 文档（API 调试） |

### 2.5 测试

| 依赖 | 版本 | 说明 |
|---|---|---|
| `spring-boot-starter-test` | 3.2.5 | JUnit 5 + Mockito |
| `spring-boot-devtools` | 3.2.5 | 热加载（开发阶段） |

## 3. 依赖冲突处理

### 3.1 Spring Boot 3 + Jakarta EE 9+

Spring Boot 3 升级后包名从 `javax.*` 变为 `jakarta.*`，常见冲突：

| 冲突场景 | 解决方式 |
|---|---|
| Swagger/OpenAPI 注解 | 使用 `knife4j-openapi3-jakarta-` 系列 |
| Spring Security 配置 | `javax.security` → `jakarta.security` |
| Servlet API | `javax.servlet` → `jakarta.servlet` |

### 3.2 MyBatis-Plus + Spring Boot 3

必须使用 `mybatis-plus-spring-boot3-starter`（不是 `mybatis-plus-spring-boot-starter`），后者不支持 Spring Boot 3。

### 3.3 Hutool 版本

`${hutool.version}` 由 Spring Boot Parent 统一管理，避免与 `jsoup` 等其他工具库冲突。

## 4. 构建产物

```
mvn clean package -DskipTests
```

生成单个 fat JAR：`colonel-saas-1.0.0.jar`（包含所有依赖，可直接 `java -jar` 运行）。

## 5. Docker 构建

Dockerfile 基于多阶段构建：

```dockerfile
# 第一阶段：Maven 构建
FROM maven:3.9-eclipse-temurin-17 AS builder
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

# 第二阶段：运行
FROM eclipse-temurin:17-jre
COPY --from=builder target/colonel-saas-1.0.0.jar app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

## 6. 相关概念

- [[DDD实战-团长SaaS系统/03-本地与三方调用SOP分离]]（Hutool HttpRequest 用法）
- [[DDD实战-团长SaaS系统/05-认证授权体系]]（JWT 依赖 jjwt）
- [[DDD实战-团长SaaS系统/12-数据库架构概览]]（PostgreSQL 驱动）

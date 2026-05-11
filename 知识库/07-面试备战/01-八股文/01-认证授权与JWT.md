---
title: 认证授权与JWT
tags: [Java, Spring, 认证授权, JWT, 八股文]
created: 2026-05-11
updated: 2026-05-11
sources: [SAAS/docs/02-架构设计, SAAS/docs/05-接口与数据模型]
---

# 认证授权与 JWT

## 一、双令牌机制

### 1.1 双令牌设计

采用 Access Token + Refresh Token 双令牌机制：

- **Access Token**：有效期 2 小时，携带 `type=access` claim，用于接口鉴权
- **Refresh Token**：有效期 7 天，携带 `type=refresh` claim，用于无感续签

```java
// JwtTokenProvider 生成双令牌
public LoginResponse generateTokens(Long userId, String username) {
    Map<String, Object> accessClaims = new HashMap<>();
    accessClaims.put("type", "access");
    accessClaims.put("userId", userId);
    accessClaims.put("username", username);
    String accessToken = createToken(accessClaims, Duration.ofHours(2));

    Map<String, Object> refreshClaims = new HashMap<>();
    refreshClaims.put("type", "refresh");
    refreshClaims.put("userId", userId);
    String refreshToken = createToken(refreshClaims, Duration.ofDays(7));

    return new LoginResponse(accessToken, refreshToken, 7200L, 604800L, ...);
}
```

### 1.2 Token 续签流程

```
请求 → JwtAuthInterceptor 拦截 → 解析 Access Token
    → 检查 Redis 黑名单 → 检查是否过期
    → 过期 → 调用 /auth/refresh 用 Refresh Token 换新 Access Token
    → 未过期 → 继续执行业务逻辑
```

### 1.3 为什么不用单令牌？

| 方案 | 优点 | 缺点 |
|---|---|---|
| 单令牌（短期） | 安全 | 用户需频繁登录，体验差 |
| 单令牌（长期） | 体验好 | 安全风险大，失效粒度粗 |
| **双令牌** | **安全 + 体验平衡** | 实现复杂度略高 |

Refresh Token 用 SHA-256 哈希存储在 Redis，泄漏后可通过删除哈希值立即吊销。

## 二、Token 黑名单机制

### 2.1 登出时两级吊销

```java
// 登出时同时将 Access Token 和 Refresh Token 加入黑名单
public void logout(String accessToken, String refreshToken) {
    // Access Token 黑名单，过期时间 = 剩余有效时间
    long remainingTtl = jwtTokenProvider.getRemainingTtl(accessToken);
    String accessHash = sha256(accessToken);
    redisTemplate.opsForValue().set(
        "auth:blacklist:" + accessHash,
        "1",
        Duration.ofSeconds(remainingTtl)
    );

    // Refresh Token 黑名单，过期时间 = 7天
    String refreshHash = sha256(refreshToken);
    redisTemplate.opsForValue().set(
        "auth:blacklist:" + refreshHash,
        "1",
        Duration.ofDays(7)
    );
}
```

### 2.2 黑名单 key 格式

```
auth:blacklist:{tokenHash}
```

- 使用 token 的 SHA-256 哈希值而非原值，保护 JWT 本身不被泄露
- 设置与 token 剩余有效期相同的 TTL，过期后 Redis 自动清理

### 2.3 JwtAuthInterceptor 校验流程

```java
// JwtAuthInterceptor.preHandle
@Override
public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
    // 1. 提取 Token
    String token = extractToken(request);

    // 2. 解析并校验签名和过期时间
    Claims claims = jwtTokenProvider.parseToken(token);

    // 3. 检查 Redis 黑名单
    String tokenHash = sha256(token);
    if (Boolean.TRUE.equals(redisTemplate.hasKey("auth:blacklist:" + tokenHash))) {
        throw new TokenInvalidException("Token has been revoked");
    }

    // 4. 校验 Token 类型（access vs refresh）
    String type = claims.get("type", String.class);
    if (!"access".equals(type)) {
        throw new TokenInvalidException("Invalid token type");
    }

    // 5. 写入请求上下文，继续执行
    request.setAttribute("userId", claims.get("userId", Long.class));
    return true;
}
```

## 三、数据权限 DataScope

### 3.1 三级数据权限

通过 `@DataScope` 注解 + `DataScopeAspect` AOP 实现行级数据过滤：

| 枚举值 | 说明 | SQL 改写 |
|---|---|---|
| `PERSONAL(1)` | 仅查看本人数据 | `WHERE create_by = #{userId}` |
| `DEPT(2)` | 查看本组数据 | `WHERE dept_id = #{deptId}` |
| `ALL(3)` | 查看全部数据 | 无条件 |

### 3.2 实现原理

```java
@DataScope(deptAlias = "u", userAlias = "u")
public interface SysUserMapper {
    // XML 中使用 ${@DataScope} 动态注入过滤条件
    List<SysUser> selectUserList(SysUserQuery query);
}
```

```java
@Aspect
@Component
public class DataScopeAspect {
    @Around("execution(* com.colonel.saas.mapper.*Mapper.*(..))")
    public Object around(ProceedingJoinPoint point) throws Throwable {
        DataScope scope = getDataScopeAnnotation(point);
        if (scope == null) return point.proceed();

        // 注入数据权限过滤 SQL
        String sql = buildDataScopeSql(scope, getCurrentUser());
        setParameter("dataScope", sql);
        return point.proceed();
    }
}
```

### 3.3 为什么不用 MyBatis-Flex 等框架自带方案？

项目采用 MyBatis-Plus，DataScope 注解 + 切面改写 SQL 是轻量级成熟方案，无需引入额外依赖，且对现有 Mapper 接口零侵入。

## 四、角色权限 @RequireRoles

### 4.1 接口级角色控制

```java
// Controller 层注解
@RequireRoles({"admin", "biz_leader"})
@PostMapping("/orders/sync")
public ApiResult<Void> syncOrders() { ... }

// AOP 切面实现
@Aspect
@Component
public class RoleGuardAspect {
    @Around("@annotation(requireRoles)")
    public Object around(ProceedingJoinPoint point, RequireRoles requireRoles) {
        List<String> allowedRoles = Arrays.asList(requireRoles.value());
        List<String> userRoles = getCurrentUserRoles();

        boolean hasRole = userRoles.stream()
            .anyMatch(allowedRoles::contains);

        if (!hasRole) {
            throw new AccessDeniedException("Insufficient role privileges");
        }
        return point.proceed();
    }
}
```

### 4.2 认证与业务的分离

```
认证层（横切）                          业务层
┌──────────────────────┐    ┌──────────────────────┐
│ JwtAuthInterceptor   │    │ Controller            │
│  - 解析 Token        │ →  │  - 参数校验           │
│  - 检查黑名单         │    │  - 调用 Service       │
│  - 写入 userId       │    │                      │
├──────────────────────┤    │ Service              │
│ RoleGuardAspect      │    │  - 业务编排           │
│  - 校验角色注解       │ →  │  - 调用 Repository    │
├──────────────────────┤    │                      │
│ DataScopeAspect      │    │ Gateway              │
│  - 注入数据权限 SQL   │ →  │  - 第三方接口抽象     │
└──────────────────────┘    └──────────────────────┘
```

认证逻辑**不侵入**业务 Service 层，保持业务代码纯净。

## 五、SecurityConfig 白名单

```java
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
            .authorizeHttpRequests(auth -> auth
                // 公开端点：登录、注册、Swagger 等
                .requestMatchers("/api/auth/login", "/api/auth/register",
                                 "/swagger-ui/**", "/v3/api-docs/**").permitAll()
                // 抖店 Webhook 回调不经过登录校验（第三方回调）
                .requestMatchers("/api/douyin/webhooks/**").permitAll()
                // 其余全部需要认证
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthInterceptor, UsernamePasswordAuthenticationFilter.class)
            .build();
    }
}
```

## 六、面试高频追问

**Q: JWT 为什么不用数据库存储 Session？**
A: JWT 是无状态令牌，验证只需要密钥（对称/非对称签名）即可，无需查库，性能好、适合分布式。代价是令牌一旦签发无法提前撤销，所以用 Redis 黑名单兜底精确控制。

**Q: Refresh Token 为什么用哈希存储？**
A: 防止 Redis 数据泄漏后攻击者拿到有效 Refresh Token 直接续签。哈希后即使数据泄漏，攻击者也无法还原出可用的 Token 字符串。

**Q: Access Token 过期但 Refresh Token 没过期的并发请求如何处理？**
A: 多线程场景下可能出现多个请求同时检测到 Access Token 过期、都去刷新。可以加分布式锁（Redisson）或者在网关层做"刷新锁"（用 userId 做 key，失败则重试）。

**Q: DataScope 和 @RequireRoles 的区别是什么？**
A: `@RequireRoles` 控制的是"谁能调用这个接口"（接口级），`DataScope` 控制的是"调用后能看到哪些数据"（数据级）。两者正交，常配合使用。

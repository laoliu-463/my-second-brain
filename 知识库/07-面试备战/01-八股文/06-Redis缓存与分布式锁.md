---
title: Redis 缓存与分布式锁
tags: [Java, Redis, 分布式锁, 缓存, 八股文]
created: 2026-05-11
updated: 2026-05-11
sources: [SAAS/docs/02-架构设计, SAAS/docs/04-开发进度]
---

# Redis 缓存与分布式锁

## 一、Token 黑名单存储

### 1.1 黑名单设计

登出时将 Token 的 SHA-256 哈希存入 Redis，设置与 Token 剩余有效期相同的 TTL：

```java
public void logout(String accessToken, String refreshToken) {
    // Access Token 黑名单：过期时间 = Token 剩余有效期
    String accessHash = sha256(accessToken);
    long remainingSeconds = jwtTokenProvider.getRemainingTtl(accessToken);
    redisTemplate.opsForValue().set(
        "auth:blacklist:" + accessHash,
        "1",
        Duration.ofSeconds(remainingSeconds)
    );

    // Refresh Token 黑名单：固定 7 天
    String refreshHash = sha256(refreshToken);
    redisTemplate.opsForValue().set(
        "auth:blacklist:" + refreshHash,
        "1",
        Duration.ofDays(7)
    );
}
```

### 1.2 校验时先查黑名单

```java
public boolean isTokenRevoked(String token) {
    String hash = sha256(token);
    return Boolean.TRUE.equals(redisTemplate.hasKey("auth:blacklist:" + hash));
}
```

**为什么用 SHA-256 哈希而不是直接存 Token 原值？**

Token 本身是有效的 JWT，直接存原值等于在 Redis 里存了一个有效凭证。一旦 Redis 数据泄漏，攻击者可以直接用存储的 Token 做接口调用。用哈希后，即使 Redis 数据泄漏，攻击者拿到的只是哈希值，无法反推出可用 Token。

## 二、Redis 缓存策略

### 2.1 Token 缓存（Real Gateway）

```java
// RealDouyinAuthGateway.ensureToken
public DouyinToken ensureToken(String appId) {
    String cacheKey = "douyin:token:" + appId;

    // 先查 Redis 缓存
    DouyinToken cached = redisTemplate.opsForValue().get(cacheKey);
    if (cached != null && !cached.isExpired()) {
        return cached;  // 缓存命中，直接返回
    }

    // 缓存未命中，向抖店请求新 Token
    DouyinToken fresh = fetchTokenFromDouyin(appId);

    // 写入缓存，过期时间比实际提前 5 分钟（留 buffer）
    redisTemplate.opsForValue().set(
        cacheKey,
        fresh,
        Duration.ofMinutes(fresh.getExpiresIn() - 5)
    );

    return fresh;
}
```

**为什么过期时间要减 5 分钟？**

网络延迟和时钟误差可能导致"缓存显示未过期但实际 Token 已失效"的情况。提前 5 分钟失效可以避免用过期 Token 去请求抖店接口导致 401。

### 2.2 业务规则缓存

```java
// BusinessRuleConfigService
private static final String CACHE_PREFIX = "business:rule:";

public String getRuleValue(String configKey) {
    String cacheKey = CACHE_PREFIX + configKey;

    // 缓存优先
    String cached = redisTemplate.opsForValue().get(cacheKey);
    if (cached != null) return cached;

    // 缓存未命中，查数据库
    SystemConfig config = systemConfigMapper.selectByKey(configKey);
    String value = config != null ? config.getConfigValue() : null;

    // 写入缓存，默认 1 小时
    if (value != null) {
        redisTemplate.opsForValue().set(cacheKey, value, Duration.ofHours(1));
    }

    return value;
}

// 配置变更时精确失效缓存
public void updateConfig(String configKey, String value) {
    systemConfigMapper.updateByKey(configKey, value);
    redisTemplate.delete(CACHE_PREFIX + configKey);  // 精确删除，不 flushall
}
```

**为什么用精确删除而不是 flushall？**

`flushall` 会清空所有 Redis 数据，可能把其他业务的缓存也清掉，导致缓存雪崩（大量请求同时打到数据库）。精确删除只删自己相关的 key，影响范围可控。

## 三、Redis 分布式锁

### 3.1 基本实现

```java
public class RedisLockService {
    private final RedisTemplate<String, String> redisTemplate;

    /**
     * 尝试获取锁
     * @return true = 获取成功，false = 已被占用
     */
    public boolean tryLock(String lockKey, Duration ttl) {
        String value = UUID.randomUUID().toString();
        // SET key value NX PX ttl — 原子操作
        Boolean acquired = redisTemplate.opsForValue()
            .setIfAbsent(lockKey, value, ttl);
        return Boolean.TRUE.equals(acquired);
    }

    /**
     * 释放锁 — 必须验证持有者身份，防止误删他人锁
     */
    public void unlock(String lockKey) {
        String script = """
            if redis.call('get', KEYS[1]) == ARGV[1] then
                return redis.call('del', KEYS[1])
            else
                return 0
            end
            """;
        redisTemplate.execute(
            new DefaultRedisScript<>(script, Long.class),
            List.of(lockKey),
            lockValue.get()  // 用 UUID 记录锁持有者
        );
    }
}
```

### 3.2 Lua 脚本的必要性

```java
// ❌ 错误写法：先查再删，非原子操作
public void unlock(String lockKey) {
    if (redisTemplate.opsForValue().get(lockKey).equals(lockValue)) {
        redisTemplate.delete(lockKey);  // 在这两个操作之间，锁可能过期被其他线程获取并写入了新值
    }
}

// ✅ 正确写法：Lua 脚本保证原子性
// Lua 脚本在 Redis 端执行，GET 和 DEL 之间不会有其他命令插入
```

### 3.3 在定时任务中的应用

```java
@Scheduled(cron = "0 30 2 * * ?")  // 每天凌晨 2:30
public void cleanupOldOperationLogs() {
    String lockKey = "job:log-cleanup:cleanup-old";

    // 抢锁，抢不到说明其他实例在执行
    if (!redisLockService.tryLock(lockKey, Duration.ofMinutes(10))) {
        log.info("Another instance is running log cleanup, skip");
        return;
    }

    try {
        // 清理 90 天前的操作日志分区
        operationLogService.cleanupOldPartitions(90);
    } finally {
        redisLockService.unlock(lockKey);
    }
}
```

## 四、缓存常见问题

### 4.1 缓存雪崩

**问题**：大量 key 同时过期 → 大量请求同时打到数据库 → 数据库被打死

**解决方案**：

```java
// 方案一：过期时间加随机偏移
Duration ttl = Duration.ofHours(1).plusMinutes(random.nextInt(30));

// 方案二：热点数据永不过期，定期异步更新
// （适合 Token 这类数据）
```

### 4.2 缓存击穿

**问题**：一个热点 key 过期 → 大量请求同时查数据库

**解决方案**：

```java
// 分布式锁 + 双重检查
public DouyinToken ensureToken(String appId) {
    String cacheKey = "douyin:token:" + appId;

    DouyinToken cached = redisTemplate.opsForValue().get(cacheKey);
    if (cached != null) return cached;

    String lockKey = "lock:token:" + appId;
    if (redisLockService.tryLock(lockKey, Duration.ofSeconds(10))) {
        try {
            // 双重检查
            cached = redisTemplate.opsForValue().get(cacheKey);
            if (cached != null) return cached;

            DouyinToken fresh = fetchTokenFromDouyin(appId);
            redisTemplate.opsForValue().set(cacheKey, fresh, ...);
            return fresh;
        } finally {
            redisLockService.unlock(lockKey);
        }
    } else {
        // 抢不到锁，短暂等待后重试
        Thread.sleep(100);
        return ensureToken(appId);
    }
}
```

### 4.3 缓存穿透

**问题**：查询一个不存在的数据 → Redis 没有 → 数据库也没有 → 每次都打到数据库

**解决方案**：

```java
// 将空结果也缓存起来，过期时间短一些（5 分钟）
String cached = redisTemplate.opsForValue().get(cacheKey);
if (cached == null) {
    String dbValue = dbQuery(key);
    if (dbValue == null) {
        redisTemplate.opsForValue().set(cacheKey, "NULL", Duration.ofMinutes(5));
    } else {
        redisTemplate.opsForValue().set(cacheKey, dbValue, Duration.ofHours(1));
    }
    return dbValue;
}
return "NULL".equals(cached) ? null : cached;
```

## 五、面试高频追问

**Q: Redis 和 Memcached 的区别？什么时候选哪个？**
A: Redis 支持更多数据类型（String/Hash/List/Set/ZSet），支持持久化，支持事务和 Lua 脚本。Memcached 只有 String，内存管理更简单（LRU）。如果只需要存 Token 字符串 + TTL，两 者都行；如果需要缓存结构化数据（Hash存用户信息）或多数据结构，选 Redis。

**Q: Redis 持久化用 RDB 还是 AOF？**
A: 本项目 Redis 主要存 Token 缓存和锁，没有存需要持久化的核心业务数据，所以用默认 RDB 就够了。如果 Redis 重启后 Token 失效，用户重新登录即可，不影响业务。AOF 适合对数据完整性要求高的场景（如分布式锁的数据）。

**Q: 分布式锁为什么不直接用 SETNX 而是用 setIfAbsent？**
A: SETNX 只能设置值，不能设置过期时间。如果加锁后进程崩溃，锁就永远无法释放。用 `setIfAbsent(key, value, ttl)` 可以一次性完成"加锁+设置过期时间"，是原子操作。

**Q: Token 缓存和业务规则缓存的过期时间为什么不一样？**
A: Token 过期时间是抖店接口返回的（2小时），存 Token 时要用这个值减去 buffer（留5分钟）。业务规则缓存是应用自己定的，规则不会频繁变化，可以设长一些（1小时）。过期时间应该根据数据本身的特性来定。

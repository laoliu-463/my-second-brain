---
title: 17-达人数据补全 Provider 体系
tags: [TalentDataProvider, EnrichOrchestrator, 数据源优先级, 字段溯源]
created: 2026-05-10
updated: 2026-05-10
sources: [TalentEnrichOrchestrator.java, TalentDataProvider.java, InternalBusinessTalentProvider.java, ManualTalentProvider.java, ThirdPartyTalentProvider.java, TestTalentProvider.java, TalentFieldSource.java]
---

# 17-达人数据补全 Provider 体系

## 1. 概述

达人数据来自多个来源（手动录入、爬虫抓取、内部业务聚合、第三方接口），各来源优先级不同、数据质量不同。`TalentEnrichOrchestrator` 负责按优先级调度多个 `TalentDataProvider`，用第一个成功返回数据的 Provider 结果填充达人字段，并记录每个字段的来源。

## 2. Provider 架构

### 2.1 接口定义

```java
public interface TalentDataProvider {
    TalentDataSource source();                          // 数据来源标识
    int priority();                                     // 优先级（数字越小越优先）
    boolean supports(TalentEnrichContext context);      // 是否支持该达人
    TalentEnrichResult enrich(TalentEnrichContext ctx); // 执行补全
}
```

### 2.2 调度流程

```
enrich(Talent talent, forceRefresh)
       ↓
遍历 providers（按 priority 升序排列）
       ↓
supports(context) == false → 跳过
       ↓
enrich(context) 返回 null 或无字段 → 跳过
       ↓
applyFields()：将 fields 写入 talent
recordFieldSources()：将每个字段的来源记入 talent_field_source 表
       ↓
return OrchestrateResult.updated()  ← 找到第一个有数据的 Provider，立即返回
```

### 2.3 字段合并策略

**短路优先**：取第一个成功返回数据的 Provider，后续 Provider 不再执行。

这意味着：
- 若爬虫已有数据，就不会用手动录入数据覆盖
- 若第三方接口返回了数据，就不会用更低优先级的 Provider

## 3. 已实现的 Provider

### 3.1 优先级总览

| Provider | Priority | 数据来源 | 说明 |
|---|---|---|---|
| `InternalBusinessTalentProvider` | 20（最高） | 内部业务聚合 | P0 placeholder，尚未实现 |
| `ThirdPartyTalentProvider` | 50 | 第三方接口 | 尚未读 |
| `ManualTalentProvider` | 90 | 手动录入 | 兜底，读取 Talent 已有字段 |
| `TestTalentProvider` | 99（最低） | 测试数据 | 仅测试环境 |

### 3.2 InternalBusinessTalentProvider（优先级 20）

```java
// InternalBusinessTalentProvider.java
@ConditionalOnProperty(prefix = "talent.enrich", name = "mode", havingValue = "real", matchIfMissing = true)
// 仅在 talent.enrich.mode=real 时启用

public TalentEnrichResult enrich(TalentEnrichContext context) {
    // P0 placeholder: internal business aggregate fields can be merged here later.
    return TalentEnrichResult.empty(source(), "internal business provider has no mapping yet");
}
```

目前是占位符，待业务积累后实现。

### 3.3 ManualTalentProvider（优先级 90，兜底）

作为最后一个有实际数据的 Provider，兜底填充 Talent 已有字段：

```java
// ManualTalentProvider.java
public TalentEnrichResult enrich(TalentEnrichContext context) {
    Talent talent = context.talent();
    Map<String, Object> fields = new LinkedHashMap<>();
    if (StringUtils.hasText(talent.getNickname())) fields.put("nickname", ...);
    if (StringUtils.hasText(talent.getAvatarUrl())) fields.put("avatarUrl", ...);
    if (talent.getFans() != null) fields.put("fans", talent.getFans());
    if (talent.getLikesCount() != null) fields.put("likesCount", talent.getLikesCount());
    if (talent.getFollowingCount() != null) fields.put("followingCount", talent.getFollowingCount());
    if (talent.getWorksCount() != null) fields.put("worksCount", talent.getWorksCount());
    if (StringUtils.hasText(talent.getIpLocation())) fields.put("ipLocation", ...);
    return TalentEnrichResult.of(source(), fields, "manual data");
}
```

## 4. 字段来源溯源（TalentFieldSource）

每次 Provider 成功填充字段时，同步将每个字段的来源写入 `talent_field_source` 表：

```java
// TalentEnrichOrchestrator.java:76-93
private void recordFieldSources(UUID talentId, String sourceType, Map<String, Object> fields) {
    for (Map.Entry<String, Object> entry : fields.entrySet()) {
        TalentFieldSource source = new TalentFieldSource();
        source.setTalentId(talentId);
        source.setFieldName(entry.getKey());        // nickname / fans / ...
        source.setSourceType(sourceType);           // INTERNAL_BUSINESS / CRAWLER / MANUAL
        source.setSourceValue(String.valueOf(entry.getValue()));  // 具体值
        source.setVerifiedTime(LocalDateTime.now());
        talentFieldSourceMapper.insert(source);
    }
}
```

作用：后续可追溯"该达人的昵称/粉丝数是从哪个渠道来的"，用于数据质量评估和数据源优先级调整。

## 5. EnrichContext 与 ForceRefresh

```java
// TalentEnrichContext.java
public record TalentEnrichContext(Talent talent, boolean forceRefresh) {}
```

| 参数 | 含义 |
|---|---|
| `talent` | 待补全的达人实体 |
| `forceRefresh` | true = 强制重新补全（忽略本地缓存）；false = 增量补全（只补空字段） |

## 6. Enrich 状态机

```
Talent.create() → enrichStatus = RUNNING
              → Orchestrator 执行
                    ├── 有 Provider 返回数据 → SUCCESS（写 lastEnrichTime）
                    └── 无 Provider 返回数据 → NO_DATA（写 lastEnrichTime）
```

```java
// TalentEnrichOrchestrator.java:44-51
talent.setDataSource(result.source().name());   // 记录数据来源
talent.setEnrichStatus("SUCCESS");
talent.setLastEnrichTime(LocalDateTime.now());
// 或
talent.setEnrichStatus("NO_DATA");
talent.setLastEnrichTime(LocalDateTime.now());
```

## 7. 相关概念

- [[DDD实战-团长SaaS系统/09-达人管理与资格体系]]（TalentEnrichTask 触发链路）
- [[DDD实战-团长SaaS系统/11-爬虫数据采集体系]]（ThirdPartyTalentProvider 可能是爬虫数据源）
- [[DDD实战-团长SaaS系统/12-数据库架构概览]]（TalentFieldSource 表设计）

---
title: PostgreSQL 高级特性与工程实践
tags: [Java, PostgreSQL, MyBatis-Plus, 八股文]
created: 2026-05-11
updated: 2026-05-11
sources: [SAAS/docs/02-架构设计, SAAS/docs/04-开发进度]
---

# PostgreSQL 高级特性与工程实践

## 一、为什么选 PostgreSQL 而不是 MySQL？

| 特性 | MySQL | PostgreSQL |
|---|---|---|
| JSONB 字段 | 5.7 开始支持但功能弱 | 原生支持 JSONB，有丰富 JSON 函数 |
| 数组类型 | 不支持 | 原生支持数组类型 |
| 范围类型 | 不支持 | 支持 Range Types |
| 物化视图 | 不支持 | 支持物化视图 |
| 软删除 | 需手动处理 | 需手动处理（一样） |
| 生态 | 运维成熟 | 近年功能迎头赶上 |

本项目选 PostgreSQL 的核心原因：**JSONB 字段 + 丰富的 JSON 函数**，适合存订单原始数据和动态扩展字段。

## 二、JSONB 字段实践

### 2.1 订单 extra_data 存储

```java
// ColonelsettlementOrder 实体
@TableName("colonelsettlement_order")
public class ColonelsettlementOrder {
    // 固定字段
    private String orderId;
    private Long activityId;
    private Long productId;
    private Long talentId;

    // 动态扩展字段，用 JSONB 存原始订单数据
    @TableField("extra_data")
    private String extraData;  // MyBatis-Plus 会自动映射为 JSONB 列

    // 读取 JSONB 字段的工具方法
    public <T> T readJsonbField(String fieldName, Class<T> type) {
        if (extraData == null) return null;
        Map<String, Object> json = JsonUtil.parse(extraData, Map.class);
        Object value = json.get(fieldName);
        if (value == null) return null;
        return JsonUtil.convert(value, type);
    }

    public String getRawColonelBuyinId() {
        return readJsonbField("colonel_buyin_id", String.class);
    }
}
```

### 2.2 MyBatis-Plus JSONB 映射

```java
// JSONB 字段的 TypeHandler
@MappedTypes(String.class)
public class JsonbStringTypeHandler extends BaseTypeHandler<String> {

    @Override
    public void setNonNullParameter(PreparedStatement ps, int i, String parameter, JdbcType jdbcType)
            throws SQLException {
        ps.setObject(i, JsonUtil.toJson(parameter), Types.OTHER);
    }

    @Override
    public String getNullableResult(ResultSet rs, String columnName) throws SQLException {
        Object obj = rs.getObject(columnName);
        return obj == null ? null : obj.toString();
    }
}
```

```yaml
# application.yml
mybatis-plus:
  type-handlers-package: com.colonel.saas.handler
```

### 2.3 JSONB 查询

```xml
<!-- 用 JSONB 函数查询嵌套字段 -->
<select id="selectUnattributedByColonelMapping" resultType="Order">
    SELECT * FROM colonelsettlement_order
    WHERE deleted = 0
      AND attribution_status = 'UNATTRIBUTED'
      AND extra_data->>'colonel_buyin_id' = #{colonelBuyinId}
      AND extra_data->>'activity_id' = #{activityId}
</select>
```

**`->>` vs `->` 的区别：**

- `->` 返回 JSON 类型（可以继续用 JSON 函数）
- `->>` 返回 text 类型（直接比较字符串）

```sql
-- 返回 JSON: {"a": 1}
SELECT extra_data->'colonel_order_info' FROM orders;

-- 返回 text: "7351155267604218149"
SELECT extra_data->>'colonel_buyin_id' FROM orders;
```

## 三、软删除实现

### 3.1 MyBatis-Plus 逻辑删除

```yaml
# application.yml
mybatis-plus:
  global-config:
    db-config:
      logic-delete-field: deleted
      logic-delete-value: 1      # 删除标记值
      logic-not-delete-value: 0   # 未删除标记值
```

```java
// 实体声明
@TableLogic  // 标注在 deleted 字段上
private Integer deleted;
```

这样所有 Mapper 查询都会自动加上 `WHERE deleted = 0`，所有删除操作都会变成 `UPDATE SET deleted = 1`。

### 3.2 为什么用整数而不是布尔值？

| 方案 | 优点 | 缺点 |
|---|---|---|
| `deleted TINYINT(1)` | 简单直观 | 无法扩展 |
| `deleted TINYINT` | 可扩展为多状态 | 稍复杂 |

本项目用 `deleted INTEGER`：

- `0` = 未删除
- `1` = 已删除
- 未来可以扩展为 `2 = 永久删除`、`3 = 归档` 等状态

## 四、操作日志分区表

### 4.1 为什么按月分区？

操作日志是高频写入场景，历史数据只查询不修改。按月分区可以：

- **快速清理**：删除旧分区比 `DELETE WHERE` 快几十倍（DDL 而非 DML）
- **查询优化**：只扫描相关月份分区，不扫描全表
- **独立索引**：每个分区可以有自己的本地索引

### 4.2 分区创建

```sql
-- 创建主表（自动继承分区规则）
CREATE TABLE operation_log (
    id BIGSERIAL,
    user_id BIGINT,
    action VARCHAR(50),
    module VARCHAR(50),
    biz_id BIGINT,
    detail TEXT,
    create_time TIMESTAMP,
    deleted INTEGER DEFAULT 0
) PARTITION BY RANGE (create_time);

-- 创建月度子分区
CREATE TABLE operation_log_2026_05
    PARTITION OF operation_log
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');

CREATE TABLE operation_log_2026_06
    PARTITION OF operation_log
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
```

### 4.3 定时创建新分区

```java
@Scheduled(cron = "0 0 1 1 * ?")  // 每月1号凌晨1点
public void ensureNextMonthPartition() {
    LocalDate nextMonth = LocalDate.now().plusMonths(1);
    String partitionName = "operation_log_" + nextMonth.format(DateTimeFormatter.ofPattern("yyyy_MM"));

    // 查询 start_time 当月分区是否已存在
    String startTime = nextMonth.withDayOfMonth(1).atStartOfDay().format(
        DateTimeFormatter.ofPattern("yyyy-MM-dd"));
    String endTime = nextMonth.plusMonths(1).withDayOfMonth(1).atStartOfDay().format(
        DateTimeFormatter.ofPattern("yyyy-MM-dd"));

    // 不存在则创建
    if (!partitionExists(partitionName)) {
        jdbcTemplate.execute(String.format(
            "CREATE TABLE IF NOT EXISTS %s PARTITION OF operation_log " +
            "FOR VALUES FROM ('%s') TO ('%s')",
            partitionName, startTime, endTime));
    }
}
```

### 4.4 清理旧分区

```java
public void cleanupOldPartitions(int retentionDays) {
    LocalDate cutoff = LocalDate.now().minusDays(retentionDays);

    // 找出需要删除的月份分区
    List<String> partitionsToDrop = getMonthlyPartitionsBefore(cutoff);

    for (String partition : partitionsToDrop) {
        // DROP TABLE 是 DDL，极快，不记 undo log
        jdbcTemplate.execute("DROP TABLE IF EXISTS " + partition);
        log.info("Dropped old partition: {}", partition);
    }
}
```

**为什么用 DROP TABLE 而不是 DELETE？**

DELETE 是 DML，要写 undo log、触发触发器、记录 redo。百万级数据可能需要几十分钟。DROP TABLE 是 DDL，秒级完成。操作日志按月分区，直接 DROP 掉最老的分区即可。

## 五、批量查询优化

### 5.1 MyBatis-Plus 批量查询

```java
// 批量根据 ID 列表查询
List<Long> ids = products.stream().map(Product::getId).toList();
List<Product> snapshots = productSnapshotMapper.selectBatchIds(ids);

// 转换为 Map 供后续快速查找
Map<Long, ProductSnapshot> snapshotMap = snapshots.stream()
    .collect(Collectors.toMap(ProductSnapshot::getId, s -> s));
```

### 5.2 分页优化

```java
// ❌ 内存分页（N+1 问题）
List<Product> all = productMapper.selectList(null);
List<Product> page = all.stream()
    .skip((pageNum - 1) * pageSize)
    .limit(pageSize)
    .toList();

// ✅ 数据库分页
IPage<Product> page = productMapper.selectPage(
    new Page<>(pageNum, pageSize),
    new LambdaQueryWrapper<Product>()
        .eq(Product::getDeleted, 0)
        .like(StringUtils.hasText(keyword), Product::getName, keyword)
        .orderByDesc(Product::getCreateTime)
);
```

### 5.3 批量聚合替代逐条查询

```java
// ❌ 逐条聚合（N+1）
for (Talent talent : talents) {
    long orderCount = orderMapper.countByTalentId(talent.getId());
    long sampleCount = sampleMapper.countByTalentId(talent.getId());
    talent.setOrderCount(orderCount);
    talent.setSampleCount(sampleCount);
}

// ✅ 批量 IN 查询
List<Long> talentIds = talents.stream().map(Talent::getId).toList();
Map<Long, Long> orderCountMap = orderMapper.countGroupByTalentIds(talentIds);
Map<Long, Long> sampleCountMap = sampleMapper.countGroupByTalentIds(talentIds);

for (Talent talent : talents) {
    talent.setOrderCount(orderCountMap.getOrDefault(talent.getId(), 0L));
    talent.setSampleCount(sampleCountMap.getOrDefault(talent.getId(), 0L));
}
```

## 六、面试高频追问

**Q: JSONB 和 JSON 有什么区别？**
A: JSON 存储为 text，查询时需要解析；JSONB 存储为二进制，解析一次后可以快速比较和查询。JSONB 不保留原始格式（空格/顺序），但查询更快。本项目选 JSONB 因为要频繁查询 `extra_data->>'colonel_buyin_id'` 这类字段。

**Q: 软删除用逻辑删除有什么缺点？**
A: 所有查询都自动加 `WHERE deleted = 0`，但如果忘记加 `@TableLogic`，就会查到已删除数据。另外，索引也要注意：唯一索引必须包含 deleted 字段，否则重复插入会报错（MySQL 会自动处理，PostgreSQL 不会）。

**Q: 分区表有什么缺点？**
A: 全表查询（如 `SELECT COUNT(*) FROM operation_log`）在分区表上会扫描所有分区，性能可能反而差。需要针对分区键做查询才能利用分区裁剪。另外，分区管理（创建/删除分区）需要额外维护逻辑。

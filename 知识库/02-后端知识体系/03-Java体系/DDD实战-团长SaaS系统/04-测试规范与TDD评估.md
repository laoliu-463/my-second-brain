---
title: 04-测试规范与TDD评估
tags: [TDD, 单元测试, JaCoCo, JUnit5, Mockito, 抖店SaaS]
created: 2026-05-10
updated: 2026-05-10
sources: [pom.xml, AttributionServiceTest.java, PickSourceMappingServiceTest.java, ProductServiceTest.java]
---

# 04-测试规范与 TDD 评估

## 1. 测试基础设施

### 技术栈

| 组件 | 选型 | 说明 |
|---|---|---|
| 测试框架 | JUnit 5 (`junit-jupiter`) | Spring Boot Starter Test 默认带入 |
| Mock 框架 | Mockito (`mockito-junit-jupiter`) | `@ExtendWith(MockitoExtension.class)` |
| 断言库 | AssertJ | `assertThat(...).isEqualTo(...)` 流式风格 |
| 覆盖率 | JaCoCo `0.8.11` | `mvn verify` 时强制检查 80% LINE 覆盖率 |
| 测试环境 | `@SpringBootTest`（Controller 层） + 纯单元（Service 层） | Service 层不加载 Spring Context |

### 依赖（来自 pom.xml）

```xml
<!-- spring-boot-starter-test 默认带入 -->
<!-- JUnit 5 + Mockito + AssertJ + Spring Test -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>

<!-- 覆盖率强制检查 -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
</plugin>
```

---

## 2. 测试规范

### 2.1 命名与结构

测试方法命名：`{methodName}_should{ExpectedBehavior}_when{Condition}`

```java
@Test
void resolveAttribution_shouldUseExclusiveMerchantFirst() { ... }

@Test
void resolveAttribution_shouldFallbackToActivityProductMappingForNativeOrder() { ... }
```

测试类命名：`{Service名}Test`，放在同名包下的 `src/test/java/`：

```
src/test/java/com/colonel/saas/
├── service/
│   ├── AttributionServiceTest.java      ← 纯单元，@ExtendWith(MockitoExtension)
│   ├── PickSourceMappingServiceTest.java
│   ├── ProductServiceTest.java
│   └── OrderAttributionReplayServiceTest.java
├── controller/
│   └── ProductControllerTest.java       ← @WebMvcTest 或 @SpringBootTest
├── douyin/api/
│   ├── DouyinApiClientTest.java
│   ├── PromotionApiTest.java
│   └── OrderApiTest.java
└── gateway/douyin/
    └── RealDouyinOrderGatewayTest.java
```

### 2.2 单元测试规范（Service 层）

使用 `@ExtendWith(MockitoExtension.class)`，**不加载 Spring 上下文**，通过构造函数手动注入 mock 依赖：

```java
@ExtendWith(MockitoExtension.class)
class AttributionServiceTest {

    @Mock
    private PickSourceMappingMapper pickSourceMappingMapper;
    @Mock
    private ProductOperationStateMapper productOperationStateMapper;
    @Mock
    private ExclusiveTalentService exclusiveTalentService;
    @Mock
    private ExclusiveMerchantService exclusiveMerchantService;

    private AttributionService service;

    @BeforeEach
    void setUp() {
        service = new AttributionService(
                pickSourceMappingMapper,
                productOperationStateMapper,
                talentMapper,
                exclusiveTalentService,
                exclusiveMerchantService
        );
    }
}
```

**原则**：
- 每个 `@Mock` 对应一个真实依赖
- `@BeforeEach setUp()` 重新初始化被测对象
- 用 `lenient().when(...)` 处理可选依赖的默认行为
- 不使用 `@InjectMocks`（隐式注入掩盖依赖关系）

### 2.3 Given-When-Then 注释

每个测试明确标注三段：

```java
@Test
void resolveAttribution_shouldUseNativeColonelBuyinMappingWhenPickSourceMissing() {
    // given
    UUID mappingUser = UUID.randomUUID();
    ProductOperationState state = new ProductOperationState();
    state.setAssigneeId(UUID.randomUUID());
    PickSourceMapping mapping = new PickSourceMapping();
    mapping.setUserId(mappingUser);
    when(productOperationStateMapper.selectOne(any())).thenReturn(state);
    when(pickSourceMappingMapper.selectList(any())).thenReturn(List.of(mapping));

    // when
    AttributionService.AttributionResult result = service.resolveAttribution(
            order,
            Map.of("colonel_buyin_id", "7351155267604218149",
                   "colonel_activity_id", "3916506")
    );

    // then
    assertThat(result.userId()).isEqualTo(mappingUser);
    assertThat(result.attributionStatus()).isEqualTo(AttributionService.STATUS_ATTRIBUTED);
    assertThat(result.attributionRemark()).isEqualTo(AttributionService.REASON_COLONEL_ORDER_INFO);
}
```

### 2.4 ArgumentCaptor 的使用

用 `ArgumentCaptor` 验证写入数据库的对象内容：

```java
@Test
void ensureFromOrder_shouldInsertWhenShortIdCanBeExtracted() {
    // given
    ColonelsettlementOrder order = makeOrder("usr_ABC12345_1712000000");
    when(pickSourceMappingMapper.selectOne(any())).thenReturn(null);

    // when
    service.ensureFromOrder(order);

    // then
    ArgumentCaptor<PickSourceMapping> captor =
            ArgumentCaptor.forClass(PickSourceMapping.class);
    verify(pickSourceMappingMapper).insert(captor.capture());
    PickSourceMapping saved = captor.getValue();
    assertThat(saved.getShortId()).isEqualTo("ABC12345");
    assertThat(saved.getPickSource()).isEqualTo(order.getPickSource());
}
```

### 2.5 防御性测试（内部类匿名覆盖）

用匿名子类覆写 protected 方法，验证行为约束：

```java
@Test
void resolveAttribution_shouldNotUseShortIdLookupForNativeColonelBuyinId() {
    AttributionService serviceRejectingShortIdLookup =
        new AttributionService(...) {
            @Override
            protected PickSourceMapping findPickSourceMappingByShortId(
                    String colonelsBuyinId) {
                throw new AssertionError(
                    "colonel_buyin_id must not be queried through short_id");
            }
        };

    // when
    AttributionService.AttributionResult result =
        serviceRejectingShortIdLookup.resolveAttribution(order, extraData);

    // then
    assertThat(result.attributionRemark())
        .isEqualTo(AttributionService.REASON_COLONEL_ORDER_INFO);
}
```

---

## 3. JaCoCo 覆盖率规则

### 3.1 强制门槛

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <configuration>
        <rules>
            <rule>
                <element>CLASS</element>
                <limits>
                    <limit>
                        <counter>LINE</counter>
                        <value>COVEREDRATIO</value>
                        <minimum>0.80</minimum>  <!-- 80% LINE 覆盖率 -->
                    </limit>
                </limits>
            </rule>
        </rules>
    </configuration>
</plugin>
```

执行 `mvn verify` 时自动检查。未达标则构建失败。

### 3.2 覆盖范围

| 包 | 是否检查 | 豁免类 |
|---|---|---|
| `com.colonel.saas.service.*` | ✅ | `ExclusiveTalentService`、`ExclusiveMerchantService`、`OrderDecryptService` |
| `com.colonel.saas.controller.*` | ✅ | `SampleController`、`DataController`、`DouyinActivityTestController` |
| `com.colonel.saas.auth.*` | ✅ | — |
| `com.colonel.saas.douyin.*` | ✅ | — |
| `com.colonel.saas.security.*` | ✅ | `JwtAuthInterceptor` |
| `com.colonel.saas.config.*` | ✅ | `CustomMetaObjectHandler` |
| `com.colonel.saas.aspect.*` | ✅ | `DataScopeAspect` |
| `com.colonel.saas.job.*` | ✅ | `SampleLifecycleJob`、`ExclusiveEvaluateJob`、`OrderSyncJob` |
| `com.colonel.saas.crawler.*` | ✅ | `CrawlerBase`、`DouyinTalentCrawler` |

---

## 4. TDD 成熟度评估

### 4.1 现状：不支持 TDD

| 特征 | 预期（真 TDD） | 项目现状 |
|---|---|---|
| 测试时机 | 先写测试（Red）→ 实现（Green）→ 重构 | 测试在源码**之后**，纯验证性质 |
| 测试驱动 | 测试**定义**接口契约和行为 | 测试**服从**已有实现 |
| 覆盖率 | 主动写测试达到目标 | JaCoCo **检查**是否达到 80%（被动） |
| 重构信心 | 测试保障重构安全 | 重构往往意味着重写测试 |
| 失败先知 | 通过测试理解需求边界 | 源码写完才知道边界在哪里 |

### 4.2 证据

`AttributionServiceTest.java` 的测试用例与 `AttributionService.resolveAttribution()` 的 if-else 分支存在**精确的对应关系**：

```
源码分支                              测试用例
─────────────────────────────────────────────────────────
exclusiveMerchant → 有值              → shouldUseExclusiveMerchantFirst
exclusiveTalent   → 有值              → shouldUseExclusiveTalentWhenMerchantNotMatched
colonelBuyinId 有值 + 精确命中 1 条  → shouldUseNativeColonelBuyinMappingWhenPickSourceMissing
colonelBuyinId 有值 + 命中 0 条      → shouldRemainUnattributedWhenColonelBuyinIdHasNoMapping
colonelBuyinId 有值 + 命中 >1 条     → shouldNotFallbackWhenActivityProductMappingIsAmbiguous
second_colonel_buyin_id 兜底        → shouldUseSecondColonelOrderInfoWhenPrimaryActivityMissing
pickSource 兜底                      → shouldFallbackToPickSourceMapping
```

这是**读懂代码后补测试**的典型模式——不是用测试发现设计问题，而是验证已知逻辑。

### 4.3 为什么不是 TDD

真正的 TDD 要求：

```
1. 拿到需求描述（归因优先级：独家商家 > 独家达人 > 抖店原生 > 渠道 > 自然流量）
2. 先写测试：传入独家商家订单，验证归因到对应达人
3. 运行测试 → 红（服务未实现）
4. 实现独家商家归因逻辑
5. 运行测试 → 绿
6. 写下一个测试（独家达人场景）→ 红
7. 实现独家达人归因逻辑 → 绿
8. ...依次实现抖店原生、渠道归因
```

项目实际流程：

```
1. 实现 AttributionService.resolveAttribution() 全部逻辑
2. 逐条补测试覆盖每个分支
3. 运行 JaCoCo 检查覆盖率
4. 覆盖率 < 80% → 补缺失测试用例
```

---

## 5. 改进建议

### 5.1 短期（立即可做）

**1. 覆盖率豁免的白名单不要继续扩大**

目前已有 18 个类/包被豁免。继续豁免会导致覆盖率数字虚高，但核心业务仍是测试盲区。

**2. Service 层测试补充 `ArgumentCaptor` 验证写入内容**

现有测试多验证返回值，少有验证 `mapper.insert(...)` 写入的完整对象内容。建议对 `saveOrUpdate` 系列方法补充写入内容校验。

**3. 为 Bug fix 补充回归测试**

每次 P1-5.2 级别的 Bug 修复后，要求必须补充对应的回归测试用例（写到测试方法的 comment 中标注 `// regression for P1-5.2`）。

### 5.2 中期（推荐）

**4. JaCoCo 检查从 `mvn verify` 前移到 `mvn package`**

目前覆盖率只在 CI 的 `verify` 阶段检查。可以考虑在 `package` 阶段也执行，让本地 `mvn package` 也能感知覆盖率变化。

**5. Controller 层用 `@WebMvcTest` 替代 `@SpringBootTest`**

`@WebMvcTest` 只加载 Web 层，Mock 所有 Service，比 `@SpringBootTest` 快 10x。

**6. 为 Gateway 层补充 Contract Test**

抖店 API Gateway（`DouyinPromotionGateway`、`RealDouyinOrderGateway`）已有 `DouyinContractFixtureProvider`，可补充基于 Provider 的 Contract Test，验证 Gateway 响应格式变化不会破坏本地处理逻辑。

### 5.3 长期（TDD 改造）

**7. 新功能先写测试**

团长 SaaS 下一阶段预计新增「佣金结算」功能。建议：

- 在 `SettlementService` 实现前，先在 `src/test/java/.../service/SettlementServiceTest.java` 中写测试
- 从最简单的"已归因订单生成结算记录"场景开始
- 每次只实现一个测试用例覆盖的场景

**8. 重构前先写测试**

如果未来需要重构 `AttributionService.resolveAttribution()` 的 5 层 if-else（拆成独立策略类），先补充足够的测试用例保障重构后行为不变。

**9. 覆盖率提升到 85%**

当前 80% 为最低门槛。核心业务类（`AttributionService`、`PickSourceMappingService`、`ProductService`）建议提升到 90%，用更高门槛驱动更完整的测试覆盖。

---

## 6. 相关概念

- [[DDD实战-团长SaaS系统/01-战略设计-限界上下文划分]]
- [[DDD实战-团长SaaS系统/02-核心领域模型详解]]
- [[DDD实战-团长SaaS系统/03-本地与三方调用SOP分离]]
- [[DDD实战-团长SaaS系统/index]]

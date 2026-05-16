---
title: Gateway 设计与环境解耦
tags: [Java, Spring, 设计模式, Gateway, 八股文]
created: 2026-05-11
updated: 2026-05-16
sources: [SAAS/docs/02-架构设计, SAAS/docs/03-Test与Real网关契约, SAAS/docs/06-部署与对接计划]
---

# Gateway 设计与环境解耦

## 一、核心问题：环境差异不该侵入业务代码

接入第三方 SDK（抖店、微信、支付宝等）最常见的问题是：

- 测试环境用 Mock 数据，真实环境用真实接口
- 切换环境时业务代码里出现大量 `if (test) {...} else {...}`
- 第三方接口字段格式与业务 DTO 不一致，到处转换

本项目的解法：**Gateway 模式 + 依赖注入切换**。

## 二、Gateway 契约模式

### 2.1 三层结构

```
Controller / Service（业务层）
    ↓ 只依赖接口，不感知实现
Gateway 接口（契约层）
    ↓
Test Gateway 实现 / Real Gateway 实现（实现层）
```

### 2.2 代码示例

**契约接口（不感知环境差异）**

```java
// 抖店活动网关接口
public interface DouyinActivityGateway {
    /**
     * 查询团长活动列表
     * @return 统一封装的业务 DTO，不直接暴露第三方原始字段
     */
    List<ColonelActivityDTO> listActivities(String appId, ActivityQuery query);

    /**
     * 查询活动详情
     */
    ColonelActivityDetailDTO getActivityDetail(String appId, Long activityId);
}
```

**Test 实现（返回本地构造的拟真数据）**

```java
@Component
@Profile("test")
public class TestDouyinActivityGateway implements DouyinActivityGateway {
    @Override
    public List<ColonelActivityDTO> listActivities(String appId, ActivityQuery query) {
        // 模拟随机性：不同请求返回不同数量
        int count = ThreadLocalRandom.current().nextInt(10, 50);
        return IntStream.range(0, count)
            .mapToObj(i -> buildMockActivity(i))
            .collect(Collectors.toList());
    }
}
```

**Real 实现（真实抖店 SDK）**

```java
@Component
@Profile("real")
public class RealDouyinActivityGateway implements DouyinActivityGateway {
    private final DouyinApiClient apiClient;

    @Override
    public List<ColonelActivityDTO> listActivities(String appId, ActivityQuery query) {
        // 调用真实抖店 SDK，吸收字段差异，转换为业务 DTO
        Map<String, Object> raw = apiClient.post("alliance.instituteColonelActivityList", params);
        return parseActivityList(raw); // 字段映射逻辑只在这里
    }
}
```

### 2.3 注入切换（零侵入）

```java
// Service 层只声明接口类型，Spring 根据激活的 Profile 注入对应实现
@Service
public class ActivityService {
    private final DouyinActivityGateway activityGateway;  // 不写 if-test

    public List<ColonelActivityDTO> getActivities(ActivityQuery query) {
        // 不关心是 Test 还是 Real Gateway
        return activityGateway.listActivities(appId, query);
    }
}
```

```yaml
# application-test.yml
spring:
  profiles:
    active: test

# application-real.yml
spring:
  profiles:
    active: real
```

**切换环境 = 换 Profile，业务代码零改动。**

## 三、Gateway 职责边界

### 3.1 Gateway 必须做的

| 职责 | 说明 |
|---|---|
| 吸收第三方字段差异 | 第三方返回 `data.data[].activity_id`，业务用 `activityId` |
| 统一错误处理 | 第三方 400/429/500 统一转换为业务异常 |
| 字段映射与转换 | 第三方原始对象 → 业务 DTO |
| 协议适配 | REST API → 方法调用、签名、加密等 |

### 3.2 Gateway 禁止做的

| 禁止 | 原因 |
|---|---|
| 直接把第三方对象上抛到 Service | 污染业务层，字段名不一致时层层传染 |
| 在 Service 里写 `if (test)` | 违反依赖倒置，Gateway 抽象毫无意义 |
| 直接透传第三方异常 | 暴露实现细节，业务无法统一处理 |

### 3.3 契约转换示意

```
第三方原始返回                    业务 DTO
┌─────────────────────┐    ┌─────────────────────┐
│ data: {              │    │ ColonelActivityDTO { │
│   data: [{           │ →  │   activityId: Long   │
│     activity_id: str │    │   activityName: str  │
│     status: int      │    │   status: Enum       │
│     colon_buyin_id   │    │   colonelBuyinId     │
│   }]                 │    │ }                    │
│ }                    │    └─────────────────────┘
└─────────────────────┘
```

## 四、当前项目 Gateway 覆盖

| 接口 | Test 实现 | Real 实现 | 状态 |
|---|---|---|---|
| `DouyinAuthGateway` | ✅ | ✅ | 已完成 |
| `DouyinProductGateway` | ✅ | ✅ | 已完成 |
| `DouyinActivityGateway` | ✅ | ✅ | 已完成 |
| `DouyinOrderGateway` | ✅ | ✅ | 已完成 |
| `DouyinPromotionGateway` | ✅ | ✅ | 已完成 |
| `LogisticsGateway` | ✅ | ❌ | 待对接 |

## 五、环境双轨设计

> 注：`local-mock` 已于 2026-05-15 收敛为历史参考，当前只保留 `test` / `real-pre` 双轨。

| 环境 | 用途 | Profile | 数据 |
|---|---|---|---|
| `test` | 功能/权限测试/Mock联调/自动化 | `test` | Mock 数据，`saas_test` / Redis DB 1 |
| `real-pre` | 真实SDK联调 | `real-pre` | 真实抖店数据，`saas_real_pre` / Redis DB 0 |

**单活设计**：同一时间只允许启动一套环境，统一 project name `saas-active`，通过 `.env.test` / `.env.real-pre` 切换。

```
┌─────────────────────────────────────────────────┐
│  同一套 Controller / Service / 前端              │
│           ↓ 依赖注入切换                         │
│  ┌─────────────────────────────────────────┐    │
│  │ Test Gateway (test profile)              │    │
│  │ Real Gateway (real profile)              │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

## 六、为什么不用 Mock Server / WireMock？

| 方案 | 优点 | 缺点 |
|---|---|---|
| WireMock / Mock Server | 独立进程，可视化 | 需要额外启动，接口变更要同步更新 |
| **Gateway + Profile 切换** | **零额外进程，代码内聚，接口变更自动同步** | 需要维护两套实现 |

本项目选 Gateway 方案，优点是**接口契约在编译期就有类型安全**，Mock Server 则依赖运行时配置，容易漂移。

## 七、面试高频追问

**Q: Gateway 模式和 Adapter 模式有什么区别？**
A: 本质都是"适配器"，但 Gateway 更强调"对业务层隐藏第三方差异"这一职责。Adapter 模式更通用，Gateway 是针对"外部系统调用"这一场景的专用 Adapter。

**Q: 如果第三方接口字段经常变，Gateway 层要怎么应对？**
A: Gateway 内部用"字段映射配置化"或"JSON Path 提取"减少硬编码。另外，第三方字段变化不应影响业务 DTO——这是 Gateway 最重要的价值。

**Q: 为什么不允许在 Service 里写 if-test？**
A: 如果 Service 层开始判断环境，Gateway 抽象就失效了。一旦开始写 `if (test) return mockData`，业务逻辑就开始被环境差异污染，后续切 Real 时改不动。

**Q: 怎么保证 Test Gateway 和 Real Gateway 返回的数据结构一致？**
A: 两者都实现同一个接口，返回同一个 DTO 类型。这是编译期约束——如果字段不一致，编译直接报错，比运行时调试快得多。

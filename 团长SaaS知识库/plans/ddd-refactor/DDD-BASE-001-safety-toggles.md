# DDD-BASE-001 — 重构安全开关与报告入口

> 任务编号：DDD-BASE-001
> 阶段：Phase 0（基础准备）
> 文档编码：UTF-8
> 路径说明：用户原指引路径 `plans-重构计划与路线图/ddd-refactor-plan.md` 在当前文件系统中并不存在；实际已有的重构计划目录为 `plans/ddd-refactor/`，本文件落位该目录下作为 DDD-BASE-001 的任务说明。

## 一、目标

建立 DDD 渐进式重构所需的安全开关（feature toggles）与报告入口，
**不改变任何线上行为**，为后续领域级重构（用户域、订单域、业绩域、商品域、寄样域）提供可灰度的开关基础。

## 二、不变量（必须遵守）

- 禁止删除旧代码和旧 Service。
- 禁止修改任何 API 接口的入参和出参。
- 禁止执行破坏性的数据库操作。
- 任意一个 `ddd.refactor.*` 子开关关闭时，对应领域的实现路径必须回退到重构前的旧实现。
- `ddd.refactor.*` 子开关开启后，对外可见行为必须与旧实现完全一致（仅内部结构变更）。

## 三、开关结构

新增的 YAML 配置项位于 `application.yml`、`application-test.yml`、`application-real-pre.yml`，统一前缀 `ddd.refactor`：

```yaml
ddd:
  refactor:
    enabled: ${DDD_REFACTOR_ENABLED:false}                  # 总开关
    user-scope:
      enabled: ${DDD_REFACTOR_USER_SCOPE_ENABLED:false}     # 用户域 self/group/all
    order-attribution:
      enabled: ${DDD_REFACTOR_ORDER_ATTRIBUTION_ENABLED:false}  # 订单/业绩归属
    performance-calc:
      enabled: ${DDD_REFACTOR_PERFORMANCE_CALC_ENABLED:false}   # 业绩域提成/双轨
    product-display:
      enabled: ${DDD_REFACTOR_PRODUCT_DISPLAY_ENABLED:false}    # 商品域转链/展示
    sample-policy:
      enabled: ${DDD_REFACTOR_SAMPLE_POLICY_ENABLED:false}      # 寄样域策略
```

### 3.1 开关语义

| 开关 | 默认 | 作用 | 启用条件 |
| --- | --- | --- | --- |
| `ddd.refactor.enabled` | false | 总开关；关闭时所有子开关均不生效 | 由 ADR 评审通过后由人工开启 |
| `ddd.refactor.user-scope.enabled` | false | 用户域数据范围（self/group/all）走新 DDD 实现 | `DDD-FACADE-USER-001` 验收通过 |
| `ddd.refactor.order-attribution.enabled` | false | 订单/业绩归属走新 DDD 实现 | `DDD-FACADE-ORDER-001` 验收通过 |
| `ddd.refactor.performance-calc.enabled` | false | 业绩域提成/双轨金额计算走新 DDD 实现 | `DDD-TEST-PERFORMANCE-CALC-001` 验收通过 |
| `ddd.refactor.product-display.enabled` | false | 商品域转链/展示走新 DDD 实现 | `DDD-FACADE-CONFIG-001` 验收通过 |
| `ddd.refactor.sample-policy.enabled` | false | 寄样域策略/状态机走新 DDD 实现 | `DDD-TEST-SAMPLE-LIFECYCLE-001` 验收通过 |

### 3.2 类型安全绑定

通过 `com.colonel.saas.config.DddRefactorProperties`（`@ConfigurationProperties(prefix = "ddd.refactor")`）将上述 YAML
绑定为 Spring Bean。嵌套子配置（`UserScope`、`OrderAttribution`、`PerformanceCalc`、`ProductDisplay`、`SamplePolicy`）以
静态内部类形式承载，每个子类的 `enabled` 默认值均为 `false`。

## 四、回归测试

- `com.colonel.saas.config.DddRefactorPropertiesTest`
  - 断言 `DddRefactorProperties` 字段默认值：`enabled` 与各子开关 `enabled` 全部为 `false`。
  - 断言五个嵌套子类的 `enabled` 默认值均为 `false`。
- 本测试 **不依赖 Spring 上下文**，不读取真实 YAML，目的是把"默认值被改成 true"这个错误
  钉死在 CI 阶段。

## 五、回滚策略

| 层级 | 回滚动作 | 触发条件 |
| --- | --- | --- |
| L1 进程内 | 关闭对应 `DDD_REFACTOR_*_ENABLED` 环境变量并重启 | 任意领域开启后出现回归 |
| L2 配置层 | 将 `application*.yml` 中 `ddd.refactor.*.enabled` 改回 `false` 并回退 commit | 配置文件被误改 |
| L3 代码层 | 删除本任务引入的 YAML 段、`DddRefactorProperties.java`、`DddRefactorPropertiesTest.java` 三处变更并回退 commit | 需要彻底撤回本任务 |

由于本任务**不引入新的业务代码路径**（旧 Controller / Service / Repository 全部保留未动），
回滚到 HEAD 即可完全恢复线上行为。

## 六、与上下游任务的关系

- 上游：本任务（DDD-BASE-001）本身无前置任务，是 Phase 0 的入口。
- 下游：每个领域重构子任务在 `docs/决策/ADR-002-V1范围优先级.md` 通过后，
  由对应子任务评审并提交 ADR，再人工开启对应子开关。
- 兼容：与 `app.test.*` 现有测试模式开关完全独立；test 模式可单独打开，无需联动本任务开关。

## 七、变更清单

| 文件 | 动作 | 备注 |
| --- | --- | --- |
| `backend/src/main/resources/application.yml` | 新增 | `ddd.refactor.*` 段，默认全 false |
| `backend/src/main/resources/application-test.yml` | 新增 | `ddd.refactor.*` 段，默认全 false |
| `backend/src/main/resources/application-real-pre.yml` | 新增 | `ddd.refactor.*` 段，默认全 false |
| `backend/src/main/java/com/colonel/saas/config/DddRefactorProperties.java` | 新建 | `@ConfigurationProperties` 类型安全绑定 |
| `backend/src/test/java/com/colonel/saas/config/DddRefactorPropertiesTest.java` | 新建 | 默认值回归测试 |
| `plans/ddd-refactor/DDD-BASE-001-safety-toggles.md` | 新建 | 本说明文档 |

## 八、未做的事项（明确列出）

- 未删除任何旧 Service / Controller / Repository。
- 未改动任何 API 入参/出参。
- 未引入任何新数据库变更或迁移脚本。
- 未在 default profile 下默认启用任何子开关。
- 未把 `DddRefactorProperties` 注入到任何业务路径（`grep -R DddRefactorProperties backend/src/main` 当前仅在配置类本体内出现）。

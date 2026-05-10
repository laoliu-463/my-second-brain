---
title: 03-本地与三方调用SOP分离
tags: [DDD, 本地操作, 三方API, 抖音开放平台, SOP]
created: 2026-05-10
updated: 2026-05-10
sources: [ProductService.java, AttributionService.java, PickSourceMappingService.java, ProductBizStatus.java]
---

# 03-本地与三方调用 SOP 分离

## 概述

团长 SaaS 系统在每个业务阶段，本地数据库操作和抖音第三方 API 调用严格分开。这么做有三个目的：可测试性（本地逻辑不依赖外部网络）、容错性（API 调用失败不阻断主流程）、可追溯性（每层数据来源清晰）。本篇按阶段梳理完整 SOP。

## 责任边界总表

| 阶段 | 本地写 | 本地读 | 抖音 API |
|---|---|---|---|
| 一、活动创建 | colonel_activity INSERT | — | activityApi.detail |
| 二、商品入库 | product_snapshot INSERT、product_operation_state INSERT | — | — |
| 三、转链（核心） | promotion_link INSERT、pick_source_mapping UPSERT | colonel_activity、product_snapshot、product_operation_state | promotionLink.generate、activityApi.detail（兜底） |
| 四、订单同步 | colonelsettlement_order INSERT/UPDATE | — | orderApi.list |
| 五、订单归因 | colonelsettlement_order UPDATE | pick_source_mapping、独家协议表 | — |
| 六、结算 | 结算记录表 | 归因订单 | — |

---

## 阶段一：活动创建

**输入**：抖店活动 ID（商家在抖店后台创建的活动）
**输出**：`colonel_activity` 表记录

```
商家          系统                      抖音平台
  │            │                           │
  │ 提交活动ID  │                           │
  │ ──────────→ │                           │
  │            │                            │
  │            │ INSERT活动记录（colonel_buyin_id=null）
  │            │ ───────────────────────────→ 本地DB
  │            │                             │
  │            │  activityApi.detail(id)    │
  │            │ ──────────────────────────→│
  │            │ ←──────────────────────────│  返回活动详情JSON
  │            │                             │
  │            │ UPSERT colonel_activity     │
  │            │ （colonel_buyin_id 主字段   │
  │            │  + extra_data JSONB）      │
  │            │ ───────────────────────────→ 本地DB
  │            │                             │
  ←─────────── │ 返回创建成功                 │
```

### 本地操作

| 操作 | 表 | 说明 |
|---|---|---|
| INSERT | colonel_activity | 初始 colonel_buyin_id = null |
| UPSERT | colonel_activity | activityApi.detail 返回后，colonel_buyin_id 回填到主字段和 extra_data |

### 抖音 API 调用

| API | 方法 | 说明 |
|---|---|---|
| enterprise.marketing.promotion.activity.detail | ActivityApi.detail() | 查询活动详情，获取 colonel_buyin_id |

### 容错策略

`activityApi.detail()` 失败 → 异常被吞，不阻断活动创建流程
原因：活动详情属于"附加信息"，主流程是让商家尽快建活动

---

## 商品业务状态机（ProductBizStatus）

理解 SOP 阶段二和三的前提：商品在活动中有一个业务状态机，限制了每个阶段允许的操作。

```
PENDING_AUDIT (待审核)
    ↓ auditProduct(approved=true)
APPROVED (已通过)
    ↓ assignProduct(assigneeId)
ASSIGNED (已分配)
    ↓ generatePromotionLink()
LINKED (已转链)
    ↓ 转链失败
PENDING_AUDIT (回退) / ASSIGNED (回退)
```

| 状态 | 含义 | 允许的操作 |
|---|---|---|
| `PENDING_AUDIT` | 待审核 | `auditProduct` |
| `APPROVED` | 已通过 | `assignProduct` |
| `ASSIGNED` | 已分配 | `generatePromotionLink`（首次转链） |
| `LINKED` | 已转链 | `generatePromotionLink`（重新转链） |

转链的前置条件：`state.bizStatus` 必须为 `ASSIGNED`（首次）或 `LINKED`（重新）。

---

## 阶段二：商品入库

**输入**：活动 ID + 抖店商品 ID
**输出**：`product_snapshot` 表记录 + `product_operation_state` 表记录

```
运营           系统                        抖店平台
  │             │                             │
  │ 添加商品    │                             │
  │ ──────────→ │                             │
  │             │                              │
  │             │ INSERT product_snapshot      │
  │             │ （raw_payload 存原始JSON，   │
  │             │  含 extra_data.colonel_buyin_id）│
  │             │ ────────────────────────────→│ 本地DB
  │             │                              │
  │             │ INSERT product_operation_state│
  │             │ （audit_payload 存审核原始数据）│
  │             │ ────────────────────────────→│ 本地DB
  │             │                              │
  ←──────────── │ 返回入库成功                   │
```

### 本地操作

| 操作 | 表 | 说明 |
|---|---|---|
| INSERT | product_snapshot | 存商品静态信息快照，raw_payload 含抖店原始 JSON（含 extra_data.colonel_buyin_id） |
| INSERT | product_operation_state | 存商品审核状态，audit_payload 含抖店原始 JSON（含 extra_data.colonel_buyin_id） |

### 抖音 API 调用

无（纯本地操作，商品信息由运营手动录入或从抖店后台复制）

---

## 阶段三：推广链接生成（核心）

**输入**：activityId、productId、userId
**输出**：推广链接 + pick_source_mapping（native mapping）
**关键**：这是两条归因通道的起点

### 3a. 本地查询（不调抖音）

```
步骤1  ensureSnapshotExists(activityId, productId)
        ├─ 查 product_snapshot 表
        └─ 返回 ProductSnapshot

        源码：ProductService.java:897
        ProductSnapshot snapshot = ensureSnapshotExists(activityId, productId);

步骤2  resolveColonelBuyinIdForNativeMapping(activityId, productId)
        ├─ ① 查 product_snapshot.raw_payload.extra_data.colonel_buyin_id    ← 本地读
        ├─ ② 查 product_operation_state.audit_payload.extra_data            ← 本地读
        ├─ ③ 查 colonel_activity 主字段 colonel_buyin_id                   ← 本地读
        │       + extra_data JSONB（patch 新增 fallback）                 ← 本地读
        └─ ④ hydrateColonelActivityMeta() 返回 null（不触发 API）

        源码：ProductService.java:898
        NativeColonelBuyinResolution nativeColonelBuyin =
            resolveColonelBuyinIdForNativeMapping(
                snapshot.getActivityId(), snapshot.getProductId());

        源码（分层策略）：ProductService.java:1101-1119
        源码（第3层修复点）：ProductService.java:1121-1141

步骤3  判断 colonelBuyinId 是否有值
        ├─ 有值 → 写 native mapping（source_type=NATIVE）
        └─ 无值 → 跳过 native mapping，打 warn 日志

        源码：ProductService.java:956-1003
        if (nativeColonelBuyin.resolved()) {
            pickSourceMappingService.saveOrUpdate(..., colonelBuyinId,
                    PickSourceMappingService.SOURCE_TYPE_NATIVE);
        } else {
            pickSourceMappingService.saveOrUpdate(..., null);  // 无 colonelBuyinId
        }
```

### 3b. 抖音 API 调用

```
步骤4  douyinPromotionGateway.generateLink()
        接口：buyin.promotionLink.generate
        输入：externalUniqueId、promotionScene、商品列表、needShortLink
        输出：promoteLink、shortLink、pickSource、shortId、pickExtra

        源码：ProductService.java:916-933
        DouyinPromotionGateway.PromotionLinkResult result =
            douyinPromotionGateway.generateLink(
                new DouyinPromotionGateway.PromotionLinkCommand(
                        finalExternalId,          // 抖店 API 必填
                        finalPromotionScene,      // 推广场景，4=商品详情页
                        List.of(snapshot.getProductId()),
                        needShortLink,
                        new DouyinPromotionGateway.PromotionContext(
                                userId, deptId,
                                snapshot.getProductId(),
                                snapshot.getActivityId(),
                                snapshot.getDetailUrl(),
                                finalScene, talentId,
                                desiredPickExtra   // 达人标识
                        )
                )
        );
```

### 3c. 本地写（基于 API 结果）

```
步骤5  保存 promotion_link 表（INSERT）

        源码：ProductService.java:935-953
        PromotionLink link = new PromotionLink();
        link.setId(UUID.randomUUID());
        link.setProductId(snapshot.getProductId());
        link.setActivityId(snapshot.getActivityId());
        link.setTalentId(talentId);
        link.setChannelUserId(userId);
        link.setChannelUserName(user.getRealName());
        link.setOriginalProductUrl(snapshot.getDetailUrl());
        link.setPromotionUrl(result.promoteLink());
        link.setShortUrl(result.shortLink());
        link.setPickSource(result.pickSource());   // 抖店返回
        link.setPickExtra(result.pickExtra());     // 达人标识
        link.setLinkStatus("ACTIVE");
        link.setOperatorId(userId);
        link.setOperatorName(user.getRealName());
        link.setCreatedAt(LocalDateTime.now());
        link.setUpdatedAt(LocalDateTime.now());
        promotionLinkMapper.insert(link);
```

### 3d. 条件触发：API 补水（colonelBuyinId 仍为 null 时）

```
步骤6  如果 3a.步骤2 的 colonelBuyinId 仍为 null
        调用 hydrateColonelActivityMeta()

        源码：ProductService.java:1143-1175
        // 第4层兜底：调抖音 API 回填
        private String hydrateColonelActivityMeta(String activityId) {
            try {
                Map<String, Object> response = activityApi.detail(null, activityId);
                Map<String, Object> data = readPrimaryDataNode(response);
                Long colonelBuyinId = readLong(data,
                        "colonel_buyin_id", "colonelBuyinId");
                if (colonelBuyinId == null || colonelBuyinId <= 0L) return null;

                // UPSERT 到 colonel_activity 表（含 extra_data JSONB）
                colonelActivityMapper.upsertRealActivityMeta(...);
                return String.valueOf(colonelBuyinId);
            } catch (Exception ex) {
                // 不阻断转链主流程
                log.warn("Hydrate colonel activity meta failed, activityId={}",
                        activityId, ex);
                return null;
            }
        }
```

### 3e. 条件触发：写 native mapping（colonelBuyinId 有值时）

```
步骤7  if (nativeColonelBuyin.resolved())

        源码：ProductService.java:956-980
        pickSourceMappingService.saveOrUpdate(
                userId,
                user != null ? user.getRealName() : "unknown",
                deptId,
                talentId,
                null,
                result.shortId(),
                null,
                result.pickSource(),          // 抖店返回的 pickSource
                snapshot.getProductId(),
                snapshot.getActivityId(),
                snapshot.getDetailUrl(),
                result.promoteLink(),
                link.getId(),
                finalScene,
                result.pickExtra(),
                nativeColonelBuyin.colonelBuyinId(),   // ← colonelBuyinId 写入
                PickSourceMappingService.SOURCE_TYPE_NATIVE  // ← sourceType
        );

        saveOrUpdate 内部逻辑：
        ├─ existing == null → INSERT 新记录
        ├─ existing != null → UPDATE（更新 userId、validUntil）
        └─ DuplicateKeyException → 并发保护，skip

        源码：PickSourceMappingService.java（核心 upsert 逻辑）
```

### 完整时序图

```
达人    ProductService    PromotionGateway   ActivityMapper    PickSourceMappingService
  │          │                   │                │                  │
  │──转链请求─→│                   │                │                  │
  │          │──查snapshot────────→│                │                  │
  │          │←─snapshot──────────│                │                  │
  │          │                                     │                  │
  │          │──resolveColonelBuyinId────────────→│                  │
  │          │  ├─snapshot.raw_payload.extra_data.buyinId            │
  │          │  ├─operationState.audit_payload                      │
  │          │  ├─activity主字段（null）                           │
  │          │  └─activity.extra_data（null）────→│ UPSERT返回null  │
  │          │←─返回NativeColonelBuyinResolution.unresolved()─────│
  │          │                                     │                  │
  │          │──generateLink─────────────────────→│  抖音API         │
  │          │←─返回promoteLink/pickSource─────────────────────────│
  │          │                                     │                  │
  │          │──upsertRealActivityMeta───────────────────────────────→│
  │          │           UPSERT(colonel_buyin_id+extra_data)        │
  │          │←─UPSERT成功────────────────────────────────────────│
  │          │                                     │                  │
  │          │──resolveColonelBuyinId（重试）─────→│                  │
  │          │  └─activity.extra_data（有值）────→│ UPSERT成功     │
  │          │←─返回NativeColonelBuyinResolution(COLONEL_ACTIVITY)──│
  │          │                                     │                  │
  │          │──saveOrUpdate(NATIVE)────────────────────────────────→│
  │          │               INSERT native mapping                      │
  │          │  (source_type='NATIVE', colonelBuyinId有值)            │
  │          │←─成功────────────────────────────────────────────────│
  │←─返回链接──│                                     │                  │
```

---

## 阶段四：订单同步

**输入**：抖音订单事件（webhook 推送 or 轮询）
**输出**：`colonelsettlement_order` 表记录

```
抖店        系统                    抖音API         本地DB
  │          │                       │              │
  │ webhook  │                       │              │
  │ ───────→│                       │              │
  │          │                       │              │
  │          │ orderApi.list()（轮询备选）│           │
  │          │ ───────────────────────→│            │
  │          │ ←───────────────────────│ 返回订单列表 │
  │          │                         │              │
  │          │ INSERT/UPDATE order                   │
  │          │ （extra_data 存完整原始JSON，          │
  │          │  含 colonel_buyin_id 等归因字段）      │
  │          │ ────────────────────────────────→    │
  │          │                         │              │
  │←─────────│ ACK                     │              │
```

### 本地操作

| 操作 | 表 | 说明 |
|---|---|---|
| INSERT/UPDATE | colonelsettlement_order | 存订单原始数据，extra_data 包含抖店原始 JSON（含 colonel_order_info.colonel_buyin_id） |

### 抖音 API 调用

| API | 方法 | 说明 |
|---|---|---|
| 抖店 webhook | DouyinWebhookController | 抖店主动推送订单事件 |
| buyin.order.list | OrderApi.list() | 主动轮询拉取订单（备用） |

---

## 阶段五：订单归因（纯本地）

**输入**：`colonelsettlement_order` 记录（含 extra_data）
**输出**：更新 `colonelsettlement_order.attribution_status`、`user_id`、`dept_id` 等字段

**特点**：此阶段不调用任何抖音 API，纯本地数据库查询和内存计算

```
系统              Order实体       AttributionService     PickSourceMapping表
  │                  │                   │                    │
  │ 触发归因          │                   │                    │
  │ ────────────────→│                   │                    │
  │                  │                   │                    │
  │ 读取extraData    │                   │                    │
  │ 提取colonelBuyinId                  │                    │
  │ ────────────────────────────────→   │                    │
  │                  │                   │                    │
  │ 独家商家归因       │                   │                    │
  │ ───────────────────────────────────→│ 查exclusive表     │
  │                  │                   │←─存在独家商家─────│
  │                  │                   │  → 返回attributed  │
  │                  │                   │                    │
  │ 独家达人归因       │                   │                    │
  │ ───────────────────────────────────→│ 查exclusive表     │
  │                  │                   │←─存在独家达人─────│
  │                  │                   │  → 返回attributed  │
  │                  │                   │                    │
  │ 抖店原生归因       │                   │                    │
  │ （extraData有     │                   │                    │
  │  colonelBuyinId） │                   │                    │
  │                  │                   │ 精确查询：          │
  │                  │                   │ WHERE              │
  │                  │                   │   colonel_buyin_id │
  │                  │                   │   = colonelsBuyinId│
  │                  │                   │   AND activity_id   │
  │                  │                   │   = activityId     │
  │                  │                   │   AND product_id   │
  │                  │                   │   = productId      │
  │                  │                   │   AND source_type  │
  │                  │                   │   = 'NATIVE'       │
  │                  │                   │   AND status = 1   │
  │                  │                   │←─1条记录───────────│
  │                  │                   │  → attribution     │
  │                  │                   │    (REASON_COLONEL_│
  │                  │                   │    ORDER_INFO)     │
  │                  │                   │                    │
  │                  │  UPDATE order      │                    │
  │                  │  (attribution_status│                    │
  │                  │   = ATTRIBUTED)   │                    │
  │                  │ ────────────────────────────────→ 本地DB│
  │←─归因完成──────────│                   │                    │
```

### 归因结果判定表

| 条件 | 归因状态 | reason | 说明 |
|---|---|---|---|
| 独家商家命中 | ATTRIBUTED | ATTRIBUTED | 商家独家优先 |
| 独家达人命中 | ATTRIBUTED | ATTRIBUTED | 达人独家其次 |
| NATIVE mapping 精确命中 1 条 | ATTRIBUTED | COLONEL_ORDER_INFO | 抖店原生归因成功 |
| NATIVE mapping 精确命中 0 条 | UNATTRIBUTED | COLONEL_MAPPING_NOT_FOUND | **Gap 根因** |
| NATIVE mapping 精确命中 >1 条 | UNATTRIBUTED | COLONEL_MAPPING_AMBIGUOUS | 多个达人操作同一商品 |
| PICK_SOURCE mapping 命中 | ATTRIBUTED | ATTRIBUTED | 渠道归因成功 |
| PICK_SOURCE mapping 未命中 | UNATTRIBUTED | MAPPING_NOT_FOUND | 渠道映射缺失 |
| 无 colonel_order_info 也无 pick_source | UNATTRIBUTED | NO_PICK_SOURCE | 自然流量 |

---

## 阶段六：结算（纯本地）

**输入**：归因完成的订单（attribution_status = ATTRIBUTED）
**输出**：`settlement` 表记录

```
系统              结算服务           订单表          结算表
  │                 │               │               │
  │ 结算周期触发     │               │               │
  │ ──────────────→│               │               │
  │                │               │               │
  │ 查归因订单      │               │               │
  │ ──────────────→│               │               │
  │←─订单列表──────│               │               │
  │                │               │               │
  │ 计算分成        │               │               │
  │ (佣金率×金额)   │               │               │
  │                │               │               │
  │ INSERT settlement              │               │
  │ (merchant_share,               │               │
  │  talent_share,                │               │
  │  colonel_share)               │               │
  │ ─────────────────────────────────────────────→│
  │                │               │               │
```

### 本地操作

| 操作 | 表 | 说明 |
|---|---|---|
| SELECT | colonelsettlement_order | 查归因成功的订单 |
| INSERT | settlement | 写入结算记录（商家/达人/团长三方分成） |
| INSERT | settlement_cycle | 结算周期记录 |

---

## 抖店 API 清单（Integration Context）

| API | 归属上下文 | 调用时机 | 容错策略 |
|---|---|---|---|
| enterprise.marketing.promotion.activity.detail | Activity | 活动创建、活动补水 | 失败不阻断主流程 |
| buyin.promotionLink.generate | Promotion Channel | 达人转链 | 失败则链路失败 |
| buyin.order.list | Order | 订单同步（轮询） | 失败可重试 |
| 抖店 webhook | Order | 订单同步（推送） | 幂等处理 |
| buyin.materialsProductStatusCheck | Admin（已删除） | 商品物料状态查询 | — |

---

## 相关概念

- [[DDD实战-团长SaaS系统/01-战略设计-限界上下文划分]]
- [[DDD实战-团长SaaS系统/02-核心领域模型详解]]
- [[DDD实战-团长SaaS系统/index]]

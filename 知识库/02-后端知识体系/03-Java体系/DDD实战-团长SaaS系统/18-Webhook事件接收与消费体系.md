---
title: 18-Webhook 事件接收与消费体系
tags: [Webhook, 抖店, 事件接收, 幂等, SHA-256, 事件重放]
created: 2026-05-10
updated: 2026-05-10
sources: [DouyinWebhookEventService.java, DouyinWebhookEvent.java]
---

# 18-Webhook 事件接收与消费体系

## 1. 概述

抖店开放平台通过 Webhook 推送事件（订单状态变更、达人状态变更等），团长 SaaS 接收后存入 `douyin_webhook_event` 表，按类型消费。核心矛盾：**幂等接收**（抖店会重试推送）+ **安全消费**（失败不丢消息，可重放）。

## 2. Webhook 接收流程

```
抖店平台 POST /api/douyin/webhook
       ↓
DouyinWebhookEventService.captureColonelOpenEvent(rawBody)
       ↓
① parse(body) → ParsedPayload
② buildEventKey(eventType, payload, body) → 唯一键
③ findByEventKey(eventKey) → 查重
       ├── 已存在 → return CaptureResult(duplicate=true)  ← 幂等返回
       └── 不存在
            ├── insert → 成功 → consume(event)
            └── DuplicateKeyException → findByEventKey → 二次确认
```

## 3. 事件唯一键（eventKey）构建

```java
// DouyinWebhookEventService.java:149-165
String eventKey = buildEventKey(eventType, payload, body);

// 优先级：event_id > msg_id > order_id（抖店平台的事件标识字段）
// 都找不到 → SHA-256(body) 作为 fallback
if (StringUtils.hasText(explicitId)) {
    return eventType + ":" + explicitId;  // 如 "doudian_alliance_colonelOpenEvent:123456"
}
return eventType + ":" + sha256(body);    // 如 "doudian_alliance_colonelOpenEvent:a3f1b2..."
```

**幂等设计**：相同 eventKey 的重复推送会命中已存在记录，直接返回，不再重复插入。

## 4. 事件状态机

```
RECEIVED  →  CONSUMED（消费成功）
         →  IGNORED（JSON 非法 / 不支持的 eventType）
         →  FAILED（消费过程异常）
```

| 状态 | 含义 | 后续动作 |
|---|---|---|
| `RECEIVED` | 刚入库，等待消费 | 立即被 `consume()` 处理 |
| `CONSUMED` | 消费成功 | 无 |
| `IGNORED` | 已知不支持，忽略 | 无 |
| `FAILED` | 消费异常 | 可被 `replayUnfinished()` 重放 |

## 5. 消费逻辑（consume）

```java
// DouyinWebhookEventService.java:103-120
private void consume(DouyinWebhookEvent event) {
    try {
        ParsedPayload parsed = parse(event.getRawPayload());

        if (!parsed.validJson()) {
            mark(event, STATUS_IGNORED, "INVALID_JSON");
            return;
        }
        if (COLONEL_OPEN_EVENT.equals(parsed.eventType())) {
            mark(event, STATUS_CONSUMED, "COLONEL_OPEN_EVENT_CAPTURED");
            return;
        }
        mark(event, STATUS_IGNORED, "UNSUPPORTED_EVENT");
    } catch (Exception ex) {
        log.warn("Douyin webhook consume failed, eventId={}, eventType={}",
                event.getId(), event.getEventType(), ex.getClass().getSimpleName());
        mark(event, STATUS_FAILED, ex.getClass().getSimpleName());
    }
}
```

**当前只处理 `doudian_alliance_colonelOpenEvent`（团长开通事件）**，其他 eventType 统一标记 `IGNORED`。

## 6. 失败重放（replayUnfinished）

```java
// DouyinWebhookEventService.java:83-101
@Transactional
public ReplayResult replayUnfinished(int limit) {
    // 查 RE/CEIVED 和 FAILED 状态的记录（按创建时间顺序）
    List<DouyinWebhookEvent> events = eventMapper.selectList(
            .in(DouyinWebhookEvent::getStatus, STATUS_RECEIVED, STATUS_FAILED)
            .eq(DouyinWebhookEvent::getDeleted, 0)
            .orderByAsc(DouyinWebhookEvent::getCreateTime)
            .last("limit " + safeLimit));

    for (DouyinWebhookEvent event : events) {
        consume(event);  // 重新走一遍消费逻辑
        if (STATUS_FAILED.equals(event.getStatus())) failed++ else consumed++;
    }
    return new ReplayResult(scanned, consumed, failed);
}
```

## 7. Payload 完整性校验

```java
// DouyinWebhookEventService.java:60
event.setPayloadHash(sha256(body));  // 存原始 body 的 SHA-256
event.setBodyLength(body.length());   // 存长度

// 用于后续比对：body 是否被篡改
```

## 8. 安全防护

| 防护项 | 实现方式 |
|---|---|
| 重复推送 | eventKey 唯一键 + findByEventKey 查重 |
| 篡改 payload | 存 SHA-256 供比对 |
| JSON 非法 | validJson 标记，非法则 IGNORED |
| 异常不丢失 | try-catch 捕获，异常标记 FAILED，可重放 |
| 并发插入 | DuplicateKeyException 二次确认 |

## 9. 与订单同步的区别

| 维度 | Webhook | 订单滑动窗口同步 |
|---|---|---|
| 触发方式 | 抖店主动推送 | SaaS 主动轮询 |
| 实时性 | 更高（有新订单即推送） | 可能有分钟级延迟 |
| 可靠性 | 依赖抖店重试机制 | 自主控制拉取频率 |
| 用途 | 团长开通事件、订单状态变更通知 | 全量订单数据同步 |

## 10. 相关概念

- [[DDD实战-团长SaaS系统/06-抖店开放平台集成]]（抖店 Webhook 配置）
- [[DDD实战-团长SaaS系统/16-操作审计日志体系]]（OperationLog 的幂等写入模式）

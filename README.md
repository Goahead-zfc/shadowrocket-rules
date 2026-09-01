# Shadowrocket Rules

适用于 Shadowrocket 的社交应用规则集，覆盖网页端与 App 流量。

## 推荐：社交软件合集

包含 Facebook、Messenger、Instagram、Threads、Discord、WhatsApp 和 X/Twitter：

```text
https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/social-media-ruleset.list
```

## 单独规则

| 平台 | RULE-SET 链接 |
| --- | --- |
| Facebook / Messenger | `https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/facebook-ruleset.list` |
| Instagram / Threads | `https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/instagram-ruleset.list` |
| Discord | `https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/discord-ruleset.list` |
| WhatsApp | `https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/whatsapp-ruleset.list` |
| X / Twitter | `https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/x-twitter-ruleset.list` |

## Shadowrocket 使用方法

在配置的 `[Rule]` 部分加入（把 `PROXY` 换成你的代理策略组名称）：

```ini
RULE-SET,https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/social-media-ruleset.list,PROXY
```

此规则应放在 `FINAL` 或 `MATCH` 规则之前。合集内的 `IP-ASN,32934` 用于补充 Meta 系 App 的媒体、通话和直接 IP 连接，因此 Facebook、Instagram、WhatsApp 等 Meta 流量会使用同一策略。

## 规则来源与维护说明

规则按各平台官方主域名整理，并参考社区维护的 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) Shadowrocket 规则进行核对。为减少误匹配，没有采用宽泛的 `DOMAIN-KEYWORD`，也没有加入会覆盖大量无关 AWS 流量的旧 WhatsApp IP 段。

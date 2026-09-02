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

## 完整配置：Goahead

整理后的 Shadowrocket 完整配置：

```text
https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/refs/heads/main/goahead.conf
```

在 Shadowrocket 中通过“从 URL 下载配置”添加这个地址。配置里的 `update-url` 已指向同一个 GitHub Raw 文件，因此多台设备都使用这个链接时，可以从同一份云端配置更新。

各个远程 `RULE-SET` 设置了 `update-interval=86400`，Shadowrocket 会每 24 小时检查一次规则集更新。完整配置本身发生变化后，在 Shadowrocket 的配置页面对该远程配置执行更新即可拉取最新版。

> 安全提示：公开配置不能包含 `ca-p12`、`ca-passphrase`、订阅地址、节点密码、Token 或其他密钥。MITM 证书应仅在设备本地生成和安装。

## 规则来源与维护说明

规则按各平台官方主域名整理，并参考社区维护的 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) Shadowrocket 规则进行核对。为减少误匹配，没有采用宽泛的 `DOMAIN-KEYWORD`，也没有加入会覆盖大量无关 AWS 流量的旧 WhatsApp IP 段。

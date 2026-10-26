# Shadowrocket Rules

适用于 Shadowrocket 的社交应用规则与国内 App 直连合集。

## 国内 App 直连合集

根据 2026-10-26 的四张截图整理。包含电商、支付、地图、音乐、短视频、聊天、智能家居、出行及金融 App 的公开域名、客户端 API、媒体 CDN 和专用 IP 补充。逐项覆盖情况、缺口和官方证据见 [App 覆盖表](domestic-apps/COVERAGE.md)。

文件：[domestic-apps-ruleset.list](domestic-apps-ruleset.list)。在 Shadowrocket 配置的 `[Rule]` 中使用：

```ini
RULE-SET,https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/domestic-apps-ruleset.list,DIRECT,update-interval=86400
```

规则订阅地址：[domestic-apps-ruleset.list](https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/domestic-apps-ruleset.list)。仓库中的完整配置已加入该引用；已使用该配置的设备更新一次配置，再更新规则集即可。

规则顺序建议：局域网/必要自定义规则 → 广告拦截 → 本合集 → 应用与通用代理规则 → GEOIP/FINAL。采用明确的 `DIRECT` 策略，不受“全球直连”策略组手动选择影响。已有更早的规则仍然优先；如果某个必需业务被广告表误拦，应单独核验并添加精确放行。

国内 App 不等于其全部网络连接都属于国内服务。HHJ 按用户要求排除；Hypic、Xmind、Chatbox、汇丰香港和欧易保留原有分流。Picsew、SenPlayer、LocalSend 等本地/局域网工具，以及用户自行设置的远程服务器，均在覆盖表中说明。不加入整朵腾讯云、阿里云、AWS 的泛域名或整 ASN，也不依赖 iOS 无法可靠实现的进程分流或 HTTPS User-Agent 匹配。

本合集是**已列来源中可获得规则的受控合并**，没有真机抓取全部 App 流量，不能称为“互联网上所有规则”或“所有版本 100% 覆盖”。部分小众 App 目前只能确认官方服务域名，这些条目均标为“部分覆盖”，没有把官网/隐私政策当成完整客户端端点表。

### 后续添加和更新

新增 App、补充域名与证据，修改 [manifest.json](domestic-apps/manifest.json)，然后执行：

```sh
python3 scripts/build_domestic_apps.py
python3 -m unittest discover -s tests -v
```

重新下载当前列入的上游规则并生成合集：

```sh
python3 scripts/build_domestic_apps.py --refresh
```

更新会保留本地人工补充。任意上游下载失败时整次刷新报错，不会悄悄把失败来源删掉或退回旧版本。更新源数据后，需要把合集、快照及审计文件一并发布到 GitHub，手机才会收到新规则；手机的 24 小时更新不会替你刷新源仓库。详细步骤见 [维护说明](domestic-apps/MAINTENANCE.md)。

原始快照位于 [upstream/](domestic-apps/upstream/)，SHA-256 位于 [sources.lock.json](domestic-apps/sources.lock.json)，每条规则的来源行号和未采用原因位于 [audit.json](domestic-apps/audit.json)。

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
| YouTube | `https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/refs/heads/main/youtube-ruleset.list` |

## Shadowrocket 使用方法

在配置的 `[Rule]` 部分加入（把 `PROXY` 换成你的代理策略组名称）：

```ini
RULE-SET,https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/social-media-ruleset.list,PROXY
```

此规则应放在 `FINAL` 或 `MATCH` 规则之前。合集内的 `IP-ASN,32934` 用于补充 Meta 系 App 的媒体、通话和直接 IP 连接，因此 Facebook、Instagram、WhatsApp 等 Meta 流量会使用同一策略。

## 完整配置：Goahead

整理后的 Shadowrocket 完整配置：

```text
https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/refs/heads/main/goahead-shadowrocket.conf
```

在 Shadowrocket 中通过“从 URL 下载配置”添加这个地址。配置里的 `update-url` 已指向同一个 GitHub Raw 文件，因此多台设备都使用这个链接时，可以从同一份云端配置更新。

各个远程 `RULE-SET` 设置了 `update-interval=86400`，Shadowrocket 会每 24 小时检查一次规则集更新。完整配置本身发生变化后，在 Shadowrocket 的配置页面对该远程配置执行更新即可拉取最新版。

> 安全提示：公开配置不能包含 `ca-p12`、`ca-passphrase`、订阅地址、节点密码、Token 或其他密钥。MITM 证书应仅在设备本地生成和安装。

## 规则来源与维护说明

规则按各平台官方主域名整理，并参考社区维护的 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) Shadowrocket 规则进行核对。为减少误匹配，没有采用宽泛的 `DOMAIN-KEYWORD`，也没有加入会覆盖大量无关 AWS 流量的旧 WhatsApp IP 段。

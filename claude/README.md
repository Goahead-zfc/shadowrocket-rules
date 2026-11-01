# Claude / Shadowrocket 单链接完整规则

更新日期：2026-11-01。所有规则已合并，**只添加一个链接即可**。

```text
https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/claude-ruleset.list
```

## 覆盖范围

共 33 条有效规则：19 条 Claude 服务及扩展域名，8 条验证码、Artifacts 字体和脚本主机，6 条 Google / Apple 登录常见端点。覆盖 App、网页、API、认证、文件与用户内容、Artifacts、MCP 组件，以及对应共享依赖。

按域名匹配，DOMAIN-SUFFIX 同时覆盖根域和所有子域，不依赖 iOS 进程名称、Bundle ID、User-Agent 或 HTTPS 解密，不需要 MITM。

## 使用方法

在配置的 `[Rule]` 中添加下面一行，策略名称换成自己已有的节点或策略组：

```ini
RULE-SET,https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/claude-ruleset.list,🇺🇸 美国节点,update-interval=86400
```

本仓库完整配置已使用这个单链接，沿用美国节点策略。已使用该配置的设备更新配置和规则集即可，全局路由选择“配置”。旧补充文件仅为兼容保留，不需要另外添加。

规则放在可能抢先匹配的广告、Google、Apple、AI 通用规则及最终兜底之前。共享验证码、CDN 和身份服务也会影响其他 App 对相同主机的分流。建议 Claude 相关请求使用同一个固定出口；测速组可能切换，需要时在设备上选择具体节点。

## 来源与边界

- [v2fly Anthropic 域名表](https://github.com/v2fly/domain-list-community/blob/master/data/anthropic)：18 个后缀和 1 个精确 CDN 主机。
- [Claude 官方网络文档](https://code.claude.com/docs/en/network-config#network-access-requirements)：认证、API、资源、用户内容、MCP 和 Artifacts 的字体/脚本说明；该文档不代表完整 iOS 抓包清单。
- [MetaCubeX Anthropic 规则](https://github.com/MetaCubeX/meta-rules-dat/blob/meta/geo/geosite/classical/anthropic.yaml)：社区交叉参考。
- Google / Apple 登录与 Turnstile 是常见共享依赖，不是逐一抓包证实的 Claude 专属主机。未启用 Fathom 统计脚本。

不接管整朵云服务、整个 Apple / Google 域名或固定 CDN IP 段。App Store、应用内购买、推送、外部连接器和生成内容访问的任意外站仍依赖其他分流规则。

已检查格式、去重、关键域名和配置引用，并通过仓库原有 6 项测试。未在 iPhone/iPad 上逐项抓包实测，不保证未来新增功能 100% 覆盖，也不替代账号、地区和出口可用性条件。

## 设备验证

更新后在 Shadowrocket 连接记录确认请求命中所选策略，依次测试登录、对话、上传图片/PDF、下载文件和 Artifacts。新增主机依据连接记录与归属证据补充。

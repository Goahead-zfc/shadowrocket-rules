# Claude / Shadowrocket 规则

整理日期：2026-11-01。适用于 Shadowrocket 外部 RULE-SET。

## 文件与链接

| 文件 | 有效规则数 | 用途 |
| --- | ---: | --- |
| [claude-ruleset.list](../claude-ruleset.list) | 19 | 推荐启用：Claude 服务域名与社区扩展域名 |
| [claude-extra-ruleset.list](../claude-extra-ruleset.list) | 8 | 可选：验证码、Artifacts 字体和脚本 CDN |
| [claude-login-ruleset.list](../claude-login-ruleset.list) | 6 | 可选：Google / Apple 登录常见端点 |

主规则：

```text
https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/claude-ruleset.list
```

功能补充：

```text
https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/claude-extra-ruleset.list
```

登录补充：

```text
https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/claude-login-ruleset.list
```

## 接入配置

在现有配置的 `[Rule]` 段添加以下内容，将 `Claude` 换成已有的策略组或节点名称。两份可选补充默认注释，按需启用。

```ini
RULE-SET,https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/claude-ruleset.list,Claude,update-interval=86400
# RULE-SET,https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/claude-extra-ruleset.list,Claude,update-interval=86400
# RULE-SET,https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/claude-login-ruleset.list,Claude,update-interval=86400
```

仓库的 [完整配置](../goahead-shadowrocket.conf) 接入主规则，沿用 `🇺🇸 美国节点`，两份补充默认注释。完整配置地址：

```text
https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/goahead-shadowrocket.conf
```

Shadowrocket 全局路由选“配置”。已使用本仓库完整配置的设备，先更新配置，再更新规则集。每天检查仅下载已发布的文件，不会自动合并上游。

规则按顺序匹配。主规则位于广告、AI 通用规则和兜底规则之前；已有更早的自定义规则仍然优先。功能补充和登录补充使用共享主机，启用后也会影响其他 App 对同一主机的分流。

主规则与启用的补充建议使用同一个固定节点。现有美国节点组可能测速切换；需要固定出口时，在设备上改用具体节点或手动选择组。

## 覆盖范围

| 功能 | 匹配依据 | 边界 |
| --- | --- | --- |
| 网页、官方 App 服务请求 | claude.ai、claude.com、anthropic.com 全部子域名 | 按域名分流，不依赖 iOS 进程或 User-Agent |
| API、控制台、认证 | api.anthropic.com、platform.claude.com、sso.claude.com | 已由后缀覆盖 |
| 资源、文件与生成内容 | Anthropic 域名以及 claudeusercontent.com 等 | 覆盖这些域名下的上传下载，不保证任意外部链接 |
| Artifacts、浏览器桥接 | *.frame.claudeusercontent.com、bridge.claudeusercontent.com | 主规则覆盖 |
| MCP 交互组件 | claudemcpcontent.com 等 | 外部连接器自身的服务另行分流 |
| 字体与脚本库 | 功能补充中的 7 个 CDN/字体主机 | 官方文档列出，可选 |
| Turnstile 验证码 | challenges.cloudflare.com | 常见共享验证依赖，按连接记录确认 |
| Google / Apple 登录 | 登录补充中的 6 个主机 | 通用身份端点，不是所有登录流程的完整清单 |
| 周边入口和开发域名 | 主规则第三组 | 社区域名表收录，并非所有 App 都访问 |

`DOMAIN-SUFFIX,claude.ai` 同时匹配根域及全部子域，不需要写 `*.claude.ai`，也不会匹配 `claude.ai.example.org`。

不加入整朵 AWS、Google Cloud、Cloudflare、Apple / Google 域名、固定 CDN IP 段或宽泛关键词。App Store 下载、应用内购买、推送和用户访问的外站遵循现有服务规则。普通域名分流不需要 MITM、HTTPS 解密证书或重写。

## 来源与核验界限

1. [v2fly Anthropic 域名表](https://github.com/v2fly/domain-list-community/blob/master/data/anthropic)：主规则 18 个后缀及 1 个精确 CDN 主机，2026-11-01 重新核对。
2. [MetaCubeX Anthropic 规则](https://github.com/MetaCubeX/meta-rules-dat/blob/meta/geo/geosite/classical/anthropic.yaml)：前一轮交叉参考。
3. [Claude 官方网络文档](https://code.claude.com/docs/en/network-config#network-access-requirements)：认证、资源、用户内容、MCP、Artifacts 第三方字体与脚本说明。文档同时介绍 Desktop 与网页额外域名，不能把 CLI 清单当成完整 iOS 流量清单。
4. [blackmatrix7 Claude 规则](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/Claude/Claude.list)：前一轮对比为两个核心后缀及 Fathom；Fathom 在本规则中只保留为注释。

第三方登录和 Turnstile 是通用依赖补充，与有来源的 Claude 主规则分开；没有声称经过逐一抓包证实。

制作时已检查格式、去重、关键子域匹配和完整配置引用，并运行仓库原有检查。未在 iPhone/iPad 逐项抓包实测，不承诺未来版本和新增功能 100% 覆盖；分流也不能替代服务的账号、地区及出口可用性条件。

## 设备验证

1. 更新配置和规则集，确认全局路由为“配置”。
2. 在连接记录中确认 Claude 域名命中所选策略。
3. 检查登录、对话、上传图片/PDF、下载生成文件和 Artifacts。
4. 验证码、生成页面或第三方登录异常时，按需要启用对应补充。
5. 依据连接记录与归属证据补充新主机，避免直接扩大到整个云服务域名。

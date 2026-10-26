# 截图国内 App 覆盖表

来源快照日期：2026-10-26。去重后 **851** 条规则。

“社区规则”表示已合并公开规则，不等于真机全功能验证；“部分覆盖”表示只有经证实的端点/域名，尚缺交易、P2P 或第三方服务。域名后缀会匹配其全部子域，能够覆盖 API 与媒体连接，不局限于网页。

| App / 公共服务 | 覆盖状态 | 本组规则 / 新增 | 说明 |
| --- | --- | ---: | --- |
| 京东 | 社区规则 | 122 / 122 | 含商城、支付、图片和客户端 API；排除集团泛云服务，未把京东云全域加入直连。 |
| 淘宝 | 社区规则 | 34 / 34 | 从阿里总表筛出淘宝、天猫及客户端公共域名；不整包直连阿里云。 |
| 拼多多 | 社区规则 | 7 / 7 | 含 API、即时消息、用户内容与图片 CDN。 |
| 闲鱼 | 社区规则 | 16 / 16 | 闲鱼独立域名加淘宝共享登录、图片服务；共享部分由淘宝组覆盖。 |
| 美团 | 社区规则 | 10 / 10 | 包括美团、大众点评、图片和配送接口。 |
| 支付宝 | 社区规则 | 24 / 23 | 支付、登录、安全校验与资源域名；不覆盖支付宝香港。 |
| 高德地图 | 社区规则 | 11 / 11 | 定位、导航、地图瓦片与客户端接口。 |
| 小红书 | 社区规则 | 8 / 8 | 含笔记图片、视频、短链及风控服务；社区总表包含第三方风控域名。 |
| 夸克 | 社区规则 | 41 / 41 | 夸克与 UC 客户端共享服务；浏览器访问的第三方站点仍按站点分流。 |
| 网易云音乐 | 社区规则 | 49 / 49 | 含 music.163.com 子域、专用视频节点与公开 IP 补充；不是仅官网。 |
| 抖音 | 社区规则 | 78 / 78 | 抖音国内版 API、视频、图片和直播；不加入 TikTok 海外域名。 |
| 哔哩哔哩 | 社区规则 | 119 / 119 | 含 API、直播、音视频、第三方 CDN 专用主机与 IP；剔除海外版独立域名。 |
| QQ | 社区规则 | 20 / 20 | 腾讯公共域名同时供微信、QQ、游戏使用；不整包直连腾讯云或腾讯 ASN。 |
| 钉钉 | 社区规则 | 14 / 14 | 含消息、登录、文件、会议域名；实时通话 P2P 目的 IP 需按日志补充。 |
| 微信 | 社区规则 | 38 / 35 | 含消息、媒体、支付和部分直接 IP；微信小程序的第三方域名不等于微信域名。 |
| 微信输入法 | 社区规则 | 1 / 1 | 专用服务 wetype.weixin.qq.com，腾讯公共基础设施由 QQ、微信组补充。 |
| 企业微信 | 部分覆盖，待日志核验 | 6 / 1 | 企业微信客户端主域与腾讯共享域名；未找到独立且完整的官方端点清单。 |
| 米家 | 社区规则 | 46 / 46 | 筛选小米账号、IoT API、MQTT、设备资源及智能家居商城域名；不整包导入小米金融/笔记/游戏和集团 IP。 |
| 中国银行 | 社区规则 | 18 / 18 | 使用中国银行公开域名表，剔除已标记的境外分支独立域名；交易直连 IP 未获官方完整清单。 |
| 中国移动 | 社区规则 | 50 / 50 | 含营业厅、认证、内容资源与公开专用 IP；不加入全运营商地址段。 |
| 豆包 | 社区规则 | 32 / 32 | 豆包、语音和资源域名；字节国内共享服务由公共组补充。 |
| 红果短剧 | 部分覆盖，待日志核验 | 34 / 34 | App Store 官方协议指向 reading.snssdk.com；视频资源依赖番茄/字节国内共享 CDN。 |
| 抖音 / 豆包 / 红果共享服务 | 社区规则 | 34 / 32 | 仅选国内业务所用公共 API/CDN；共享域名仍可能被其他字节 App 使用，不能做到进程隔离。 |
| 王者荣耀 | 部分覆盖，待日志核验 | 10 / 10 | 已核对官方游戏入口及腾讯客户端 SDK 域名；动态 UDP 对局和 P2P IP 尚无完整公开清单，不能保证全局游戏加速流量直连。 |
| ToDesk | 部分覆盖，待日志核验 | 1 / 1 | 已确认官方服务主域；控制连接/中继在其子域时可命中，P2P 对端任意 IP 不可由固定域名规则穷举。 |
| 九号出行 | 部分覆盖，待日志核验 | 3 / 3 | 已确认九号服务域名，覆盖其 API 子域；车辆云服务、固件下载和第三方地图仍需连接日志核验。 |
| DREAME | 部分覆盖，待日志核验 | 1 / 1 | 追觅服务协议与公开客户端集成确认 dreame.tech 为服务域；MQTT、机器人连接随区域/机型变化，待真机核验。 |
| LynkCo / 领克 | 部分覆盖，待日志核验 | 4 / 4 | 领克和公开车联网域名；不导入整个吉利/沃尔沃集团，远程车控第三方节点待日志核验。 |
| 像素蛋糕 | 部分覆盖，待日志核验 | 2 / 2 | 官方 iOS 协议直接位于 api.pixcakeai.com，含下载域；其他上传桶、推理域尚无完整公开清单。 |
| 江苏智慧人社 | 部分覆盖，待日志核验 | 1 / 1 | App Store 官方隐私政策位于 rs.jshrss.jiangsu.gov.cn/mobile/legal；覆盖该业务子树，电子社保卡/人脸核验供应商需日志核验。 |
| 江苏·农商行 | 部分覆盖，待日志核验 | 3 / 3 | 截图为江苏农商行，非中国农业银行；官方域名与江苏农信域名，交易直连 IP 待日志补充。 |
| 华安基金 | 部分覆盖，待日志核验 | 1 / 1 | 官方主域可覆盖下属交易/API 子域，但尚无完整公开交易 IP 清单。 |
| 华宝智投 | 部分覆盖，待日志核验 | 2 / 2 | 官方 App 说明确认 touker.com；同时覆盖华宝证券主域，行情直连 IP 待补。 |
| 同花顺 | 部分覆盖，待日志核验 | 2 / 2 | 官方 App 协议确认 10jqka.com.cn；补充公开 myhexin.com。动态行情 TCP/直连 IP 尚未真机核验。 |
| 京东钱包 | 社区规则 | 7 / 0 | 支付、网银和金融域名，京东公共 API 由京东组覆盖。 |
| ES 文件浏览器 | 部分覆盖，待日志核验 | 3 / 3 | 官方 App 说明与协议可确认服务域，用户配置的 SMB/WebDAV/Google Drive/OneDrive 目的地分别分流，不能整 App 强制直连。 |
| iCost | 部分覆盖，待日志核验 | 2 / 2 | 官方帮助、隐私与客服域；账本 iCloud 同步沿用苹果/iCloud 原策略，不全局直连苹果域名。 |
| 国内 App 共用一键登录 | 社区规则 | 16 / 15 | 仅列运营商一键登录端点；第三方 SDK 共享域名也会影响其他使用该 SDK 的 App。 |

## 未加入默认直连的截图 App

| App | 原因 |
| --- | --- |
| HHJ | 用户明确不需要。 |
| Hypic、Xmind、Chatbox | 按用户选择保留原有分流，不因国内公司出品就强制境外服务直连。 |
| 汇丰香港、欧易 | 香港/境外金融服务保留现有分流；配置已有欧易直连规则不在本次修改范围。 |
| Picsew、SenPlayer、LocalSend | 本地处理/局域网传输或用户自行指定媒体服务器，未找到需强制直连的已确认国内客户端服务；现有 LAN 规则继续适用。 |
| Typeless | 未确认其依赖国内服务，不强制直连。 |
| Instagram、Facebook、WhatsApp、X、Telegram、TikTok、YouTube、Gemini、ChatGPT、Grok、Notion、Unsplash、Lightroom、Chrome、Windows、AdGuard、Shadowrocket、TestFlight | 境外服务、系统/浏览器/代理工具不属于国内服务合集；保持原有分流。 |
| 电话、信息、Safari | 系统电话/短信不以普通 App 域名规则处理；Safari 按所访问站点分流。 |

## 每组来源

原始来源文件均保留在 upstream/；完整逐条来源、行号和剔除原因见 audit.json。仅删除完全重复的规则，保留便于追溯的子域规则。

### 京东

- [blackmatrix7-rule-Shadowrocket-JingDong-JingDong](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/JingDong/JingDong.list)
- [v2fly-data-jd](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/jd)
- [ACL4SSR-Clash-Ruleset-JD](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/JD.list)
- [LM-Firefly-Domestic-Services-JingDong](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/JingDong.list)

### 淘宝

- [blackmatrix7-rule-Shadowrocket-Alibaba-Alibaba_Domain](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Alibaba/Alibaba_Domain.list)
- [v2fly-data-alibaba](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/alibaba)
- [ACL4SSR-Clash-Ruleset-Alibaba](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Alibaba.list)
- [LM-Firefly-Domestic-Services-Alibaba](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/Alibaba.list)

### 拼多多

- [blackmatrix7-rule-Shadowrocket-Pinduoduo-Pinduoduo](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Pinduoduo/Pinduoduo.list)
- [v2fly-data-pinduoduo](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/pinduoduo)
- [ACL4SSR-Clash-Ruleset-PDD](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/PDD.list)

### 闲鱼

- [blackmatrix7-rule-Shadowrocket-XianYu-XianYu](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/XianYu/XianYu.list)
- [LM-Firefly-Domestic-Services-XianYu](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/XianYu.list)

### 美团

- [blackmatrix7-rule-Shadowrocket-MeiTuan-MeiTuan](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/MeiTuan/MeiTuan.list)
- [v2fly-data-meituan](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/meituan)
- [LM-Firefly-Domestic-Services-MeiTuan](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/MeiTuan.list)

### 支付宝

- [blackmatrix7-rule-Shadowrocket-AliPay-AliPay](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/AliPay/AliPay.list)
- [v2fly-data-alibaba](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/alibaba)
- [LM-Firefly-Domestic-Services-AliPay](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/AliPay.list)

### 高德地图

- [blackmatrix7-rule-Shadowrocket-GaoDe-GaoDe](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/GaoDe/GaoDe.list)
- [v2fly-data-amap](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/amap)
- [LM-Firefly-Domestic-Services-GaoDe](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/GaoDe.list)

### 小红书

- [blackmatrix7-rule-Shadowrocket-XiaoHongShu-XiaoHongShu](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/XiaoHongShu/XiaoHongShu.list)
- [v2fly-data-xiaohongshu](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/xiaohongshu)

### 夸克

- [blackmatrix7-rule-Shadowrocket-UC-UC](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/UC/UC.list)
- [v2fly-data-uc](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/uc)
- [v2fly-data-alibaba](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/alibaba)
- [LM-Firefly-Domestic-Services-UC](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/UC.list)

### 网易云音乐

- [blackmatrix7-rule-Shadowrocket-NetEaseMusic-NetEaseMusic](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/NetEaseMusic/NetEaseMusic.list)
- [ACL4SSR-Clash-Ruleset-NetEaseMusic](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/NetEaseMusic.list)
- [LM-Firefly-Domestic-Services-NeteaseMusic](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/NeteaseMusic.list)

### 抖音

- [blackmatrix7-rule-Shadowrocket-DouYin-DouYin](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/DouYin/DouYin.list)
- [v2fly-data-douyin](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/douyin)

### 哔哩哔哩

- [blackmatrix7-rule-Shadowrocket-BiliBili-BiliBili](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/BiliBili/BiliBili.list)
- [v2fly-data-bilibili](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/bilibili)
- [v2fly-data-bilibili-cdn](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/bilibili-cdn)
- [ACL4SSR-Clash-Ruleset-Bilibili](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Bilibili.list)
- [LM-Firefly-Domestic-Services-BiliBili](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/BiliBili.list)

### QQ

- [v2fly-data-tencent](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/tencent)
- [LM-Firefly-Domestic-Services-Tencent](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/Tencent.list)

### 钉钉

- [blackmatrix7-rule-Shadowrocket-DingTalk-DingTalk](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/DingTalk/DingTalk.list)
- [v2fly-data-dingtalk](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/dingtalk)
- [LM-Firefly-Domestic-Services-DingTalk](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/DingTalk.list)

### 微信

- [blackmatrix7-rule-Shadowrocket-WeChat-WeChat](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/WeChat/WeChat.list)
- [ACL4SSR-Clash-Ruleset-Wechat](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Wechat.list)

### 微信输入法

- [blackmatrix7-rule-Shadowrocket-WeType-WeType](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/WeType/WeType.list)

### 企业微信

- [v2fly-data-tencent](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/tencent)
- [官方/端点证据](https://work.weixin.qq.com/)

### 米家

- [blackmatrix7-rule-Shadowrocket-XiaoMi-XiaoMi](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/XiaoMi/XiaoMi.list)
- [v2fly-data-xiaomi](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/xiaomi)
- [v2fly-data-xiaomi-iot](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/xiaomi-iot)
- [ACL4SSR-Clash-Ruleset-MI](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/MI.list)
- [LM-Firefly-Domestic-Services-XiaoMi](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/Xiaomi.list)

### 中国银行

- [blackmatrix7-rule-Shadowrocket-BOC-BOC](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/BOC/BOC.list)
- [v2fly-data-boc](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/boc)
- [LM-Firefly-Domestic-Services-BOC](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/BOC.list)

### 中国移动

- [blackmatrix7-rule-Shadowrocket-ChinaMobile-ChinaMobile](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/ChinaMobile/ChinaMobile.list)
- [v2fly-data-chinamobile](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/chinamobile)
- [LM-Firefly-Domestic-Services-ChinaMobile](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/ChinaMobile.list)

### 豆包

- [v2fly-data-doubao](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/doubao)

### 红果短剧

- [v2fly-data-fqnovel](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/fqnovel)
- [官方/端点证据](https://apps.apple.com/cn/app/id6451407032)
- [官方/端点证据](https://reading.snssdk.com/wap-hongguo/dr-privacy-v3.html)

### 抖音 / 豆包 / 红果共享服务

- [blackmatrix7-rule-Shadowrocket-ByteDance-ByteDance](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/ByteDance/ByteDance.list)
- [LM-Firefly-Domestic-Services-ByteDance](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/ByteDance.list)

### 王者荣耀

- [v2fly-data-tencent-games](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/tencent-games)
- [官方/端点证据](https://pvp.qq.com/)
- [官方/端点证据](https://github.com/v2fly/domain-list-community/blob/master/data/tencent-games)

### ToDesk

- [官方/端点证据](https://apps.apple.com/cn/app/id1519407428)

### 九号出行

- [官方/端点证据](https://apps.apple.com/cn/app/id1458698038)
- [官方/端点证据](https://hero.ninebot.com/)
- [官方/端点证据](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/ChinaMax/ChinaMax_Domain.list)

### DREAME

- [官方/端点证据](https://apps.apple.com/cn/app/id1564419343)
- [官方/端点证据](https://protocol.dreame.tech/p2177/zh/general_privacyPolicy.html)
- [官方/端点证据](https://github.com/Tasshack/dreame-vacuum/blob/master/custom_components/dreame_vacuum/dreame/protocol.py)

### LynkCo / 领克

- [blackmatrix7-rule-Shadowrocket-Geely-Geely](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Geely/Geely.list)
- [LM-Firefly-Domestic-Services-Geely](https://raw.githubusercontent.com/LM-Firefly/Rules/master/Domestic-Services/Geely.list)
- [官方/端点证据](https://apps.apple.com/cn/app/id1305517667)
- [官方/端点证据](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/ChinaMax/ChinaMax_Domain.list)

### 像素蛋糕

- [官方/端点证据](https://apps.apple.com/cn/app/id6743614900)
- [官方/端点证据](https://api.pixcakeai.com/static/protocol/cake_privacy.html)
- [官方/端点证据](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/ChinaMax/ChinaMax_Domain.list)

### 江苏智慧人社

- [官方/端点证据](https://apps.apple.com/cn/app/id1463539099)
- [官方/端点证据](https://rs.jshrss.jiangsu.gov.cn/mobile/legal)

### 江苏·农商行

- [官方/端点证据](https://apps.apple.com/cn/app/id555257605)
- [官方/端点证据](http://www.js96008.com)
- [官方/端点证据](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/ChinaMax/ChinaMax_Domain.list)

### 华安基金

- [v2fly-data-category-securities-cn](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/category-securities-cn)
- [官方/端点证据](https://apps.apple.com/cn/app/id501236714)
- [官方/端点证据](https://www.huaan.com.cn/)

### 华宝智投

- [v2fly-data-category-securities-cn](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/category-securities-cn)
- [官方/端点证据](https://apps.apple.com/cn/app/id993077954)

### 同花顺

- [官方/端点证据](https://apps.apple.com/cn/app/id303191318)
- [官方/端点证据](https://m.10jqka.com.cn/)
- [官方/端点证据](https://github.com/blackmatrix7/ios_rule_script/blob/master/rule/Shadowrocket/ChinaMax/ChinaMax_Domain.list)

### 京东钱包

- [v2fly-data-jd](https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/jd)

### ES 文件浏览器

- [官方/端点证据](https://apps.apple.com/cn/app/id1441621965)
- [官方/端点证据](https://page.xdplt.com/es/ESFileExplorerTermsofService.html)

### iCost

- [官方/端点证据](https://apps.apple.com/cn/app/id1484262528)
- [官方/端点证据](https://help.icostapp.com/guide/law/privacy.html)

### 国内 App 共用一键登录

- [ACL4SSR-Clash-Ruleset-ChinaOneKeyLogin](https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/ChinaOneKeyLogin.list)

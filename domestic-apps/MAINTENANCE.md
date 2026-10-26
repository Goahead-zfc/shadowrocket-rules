# 国内 App 直连合集维护说明

该合集面向 Shadowrocket 的 `RULE-SET`。生成的 `.list` 仅包含匹配条件，最终策略由配置中的 `RULE-SET,...,DIRECT` 指定；文件不是可直接替换整份配置的 `.conf`。

## 文件结构

| 文件 | 用途 |
| --- | --- |
| `manifest.json` | 截图 App 清单、人工补充、来源选择、排除域名与证据 |
| `upstream/` | 原始公开规则快照，保留原作者头部信息 |
| `sources.lock.json` | 快照下载日期、原始 URL 与文件 SHA-256 |
| `official-evidence.json` | App Store 身份信息及官方文档链接证据，不是运行时抓包结果 |
| `audit.json` | 每条输出规则的来源行号、所属组、未采用条目及原因 |
| `COVERAGE.md` | 自动生成的逐 App 覆盖表 |
| `../domestic-apps-ruleset.list` | 导入手机的合集 |
| `../scripts/build_domestic_apps.py` | 只使用 Python 标准库的生成、刷新与校验工具 |

## 添加一个 App

在 `manifest.json` 的 `groups` 数组追加一项。下面是结构示例，示例域名不要直接加入实际配置：

```json
{
  "id": "example-app",
  "apps": ["示例 App"],
  "coverage": "partial",
  "note": "仅确认官方 API 与图片域；实时通话需连接日志验证。",
  "uses": [],
  "rules": [
    "DOMAIN-SUFFIX,api.example.com",
    "DOMAIN,images.example.net"
  ],
  "evidence": ["https://example.com/official-network-document"]
}
```

如果是已有 App，在它的 `rules` 数组追加规则，在 `evidence` 记录官方端点文档或公开来源。`DOMAIN-SUFFIX,example.com` 会匹配 `api.example.com`、`media.example.com` 等全部子域；不要为了显示数量而重复列出已被后缀覆盖的每个主机。

`uses` 可以引用 `sources` 中的上游来源 ID，也可以加 `only_suffixes` 只选择该 App 的业务域。添加新远程来源时，在 `sources` 中填写 `id`、`url`、`format`、`cache`、`license`，然后执行 `--refresh` 创建快照。支持 `shadowrocket`、`domain-list` 和 `v2fly` 三种格式。

v2fly 分类里的 `include:` **不会自动整包展开**。需要哪个子分类，就将对应数据文件显式添加到 `sources` 并在组中引用。这可避免把字节分类内的 TikTok、海外 AI 或整个云服务加入国内直连。上游 `@!cn` 标记会同时阻止同一境外域名从其他源重新进入；`@ads` 独立条目不单独导入，广告仍由原配置拦截。

所有新增规则要有依据。官方隐私政策中的 SDK 厂商官网只是依赖证据，不能直接推导为运行时 API；未验证的 IP 不要根据域名当前 DNS 解析结果长期固定。

## 更新和检查

修改本地清单后生成：

```sh
python3 scripts/build_domestic_apps.py
```

从列入的公开上游重新下载全部源并生成：

```sh
python3 scripts/build_domestic_apps.py --refresh
```

任一下载失败都会停止，保留原有快照。只生成一次的快照不等于持续追踪整个互联网；新增来源、上游新增类别与官方端点需要另行维护。刷新只负责下载已列来源，不会自动发现新 App。该脚本不需要 GitHub Token。

检查生成文件与源文件是否一致，并验证客户端端点和误匹配边界：

```sh
python3 scripts/build_domestic_apps.py --check
python3 -m unittest discover -s tests -v
```

仓库 GitHub Actions 会在相关文件变更时执行离线检查；没有设置周期更新，也不会自动提交/推送。

发布时将 `manifest.json`、快照、锁文件、审计表、覆盖表与 `.list` 一并提交并推送到 `main`。确认 GitHub Raw 地址可访问，再在 Shadowrocket 更新配置/规则集。首次导入整份配置后，已有配置仍需主动更新一次才能取得新增 `RULE-SET` 引用。

## 根据手机连接日志补全

1. 在 Shadowrocket 开启连接记录，记录当前 App 名、版本、使用地区，以及出问题的功能。
2. 分别测试冷启动/登录、刷新、上传下载、媒体播放、语音视频、交易或车辆控制等实际功能；不要只打开官网测试。
3. 查看没有命中本合集的目标主机或直接 IP，核验它的归属及是否为业务必需。对第三方云存储使用该 App 实际的专用主机或存储桶，不放行整朵云。
4. 添加最小范围的规则，重建并重新导入，在连接日志确认策略为 `DIRECT`。没有域名的连接需要确认目标 IP 归属及稳定性；不要因多个连接共用端口就按端口全局直连。

分享日志前移除账号、Cookie、Token、请求正文、完整私人 URL、设备标识和其他个人信息。补齐域名通常只需要脱敏后的主机、IP、端口、App/功能和匹配策略，不需要启用 HTTPS MITM。

ToDesk 的 P2P 对端、王者荣耀动态 UDP 对局、第三方小程序、浏览器任意网页和自建 WebDAV 不存在一份可穷举的固定 App 域名表。此合集不能在 iPhone 上按进程保证这些 App 的所有连接直连。Apple 推送、iCloud、Firebase 等系统/境外公共依赖沿用原有策略。

## 规则范围与优先级

合集包含社区 App 专属规则中的公开 IP 条目。部分 IP 范围属于厂商或历史服务节点，可能同时承载同厂其他业务，也可能随时间迁移；它们是公开补充规则，未经本机逐项验证。对固定 IP 有严格要求时，请根据 `audit.json` 找到原始来源后复核。

`DOMAIN-SUFFIX,qq.com` 等共享业务域名不能只匹配一个 App。国内 App 的公开域名也可能托管在境外节点；“国内服务”是按业务归属选择，不是所有目的 IP 的地理位置保证。本次默认不加入整个集团的所有境外产品，明确排除的独立域名见 `manifest.json`。

合集保留各组中完全不同的子域规则，方便追踪来源；只去掉完全相同的规则，不将主机合并成更宽泛的根域。现有配置中更早的自定义规则与广告规则优先于本合集。欧易原有直连引用没有改动，但欧易没有被纳入新合集。

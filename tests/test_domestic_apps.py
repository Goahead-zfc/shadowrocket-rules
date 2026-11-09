import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("builder", ROOT / "scripts/build_domestic_apps.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class DomesticAppsTests(unittest.TestCase):
    def test_client_api_media_and_direct_ip_coverage(self):
        manifest = json.loads((ROOT / "domestic-apps/manifest.json").read_text())
        rendered = builder.render(manifest)
        rules = set(rendered[builder.OUTPUT].splitlines())
        for rule in [
            "DOMAIN-SUFFIX,music.163.com", "DOMAIN-SUFFIX,acgvideo.com",
            "DOMAIN-SUFFIX,bilivideo.com", "DOMAIN-SUFFIX,amemv.com",
            "DOMAIN-SUFFIX,snssdk.com", "DOMAIN-SUFFIX,weixin.qq.com",
            "DOMAIN,wetype.weixin.qq.com", "DOMAIN-SUFFIX,dreame.tech",
            "DOMAIN-SUFFIX,pixcakeai.com", "DOMAIN-SUFFIX,jshrss.jiangsu.gov.cn",
            "IP-CIDR,101.32.104.4/32,no-resolve",
        ]:
            self.assertIn(rule, rules)
        active = [r for r in rules if r and not r.startswith("#")]
        self.assertTrue(all(builder.normalize(r) == r for r in active))

    def test_foreign_services_and_clouds_do_not_match(self):
        manifest = json.loads((ROOT / "domestic-apps/manifest.json").read_text())
        text = builder.render(manifest)[builder.OUTPUT]
        rules = [line.split(",") for line in text.splitlines() if line and not line.startswith("#")]
        for host in [
            "api.tiktok.com", "v16.tiktokcdn.com", "p16.byteoversea.com",
            "api.bilibili.tv", "api.biliintl.com", "api.jd.hk", "www.jd.id",
            "www.bochk.com", "www.alipay.hk", "www.capcut.com",
            "example.amazonaws.com", "example.myqcloud.com", "example.aliyuncs.com",
            "unrelated.jdcloud.com", "unrelated.jcloud.com", "www.cloud-beijing.com",
            "chatgpt.com", "gemini.google.com", "api.typeless.com", "api.xmind.app",
        ]:
            self.assertFalse(any(
                (r[0] == "DOMAIN" and host == r[1]) or
                (r[0] == "DOMAIN-SUFFIX" and builder.suffix_match(host, r[1]))
                for r in rules
            ), host)

    def test_domain_boundary_prevents_false_matches(self):
        self.assertTrue(builder.suffix_match("api.todesk.com", "todesk.com"))
        self.assertFalse(builder.suffix_match("not-todesk.com", "todesk.com"))
        self.assertFalse(builder.suffix_match("todesk.com.example.org", "todesk.com"))

    def test_v2fly_attributes_and_include_are_not_silently_imported(self):
        for line in ["overseas.example @!cn", "tracker.example @ads", "include:tiktok", "regexp:.*"]:
            rule, reason = builder.parse_line(line, "v2fly")
            self.assertIsNone(rule)
            self.assertTrue(reason)
        self.assertEqual(builder.parse_line("full:api.example.com # comment", "v2fly")[0], "DOMAIN,api.example.com")

    def test_invalid_rules_and_embedded_policies_fail(self):
        for rule in ["DOMAIN-SUFFIX,example.com,DIRECT", "DOMAIN-SUFFIX,*.example.com", "DOMAIN-SUFFIX,https://example.com", "IP-CIDR,192.168.0.0/16", "IP-CIDR,1.1.1.1/32,PROXY", "FINAL,DIRECT", "IP-CIDR,1.1.1.1/24"]:
            with self.assertRaises(ValueError, msg=rule):
                builder.normalize(rule)
        self.assertEqual(builder.normalize("IP-CIDR,2400:b200::/32"), "IP-CIDR6,2400:b200::/32,no-resolve")

    def test_config_preserves_adblocking_and_uses_direct_policy(self):
        config = (ROOT / "goahead-shadowrocket.conf").read_text()
        entry = "RULE-SET,https://raw.githubusercontent.com/Goahead-zfc/shadowrocket-rules/main/domestic-apps-ruleset.list,DIRECT,update-interval=86400"
        self.assertEqual(config.count(entry), 1)
        self.assertLess(config.index("BanProgramAD.list"), config.index(entry))
        self.assertLess(config.index(entry), config.index("# > 社交与 AI"))
        self.assertLess(config.index(entry), config.index("ChinaDomain.list"))


if __name__ == "__main__":
    unittest.main()

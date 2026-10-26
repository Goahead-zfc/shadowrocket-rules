#!/usr/bin/env python3
"""Build the audited Shadowrocket list using only the Python standard library."""
import argparse
import concurrent.futures
import datetime
import hashlib
import ipaddress
import json
import re
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "domestic-apps"
OUTPUT = ROOT / "domestic-apps-ruleset.list"
TYPES = {"DOMAIN", "DOMAIN-SUFFIX", "IP-CIDR", "IP-CIDR6"}


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def atomic_write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temp:
        temp.write(value.encode("utf-8") if isinstance(value, str) else value)
        name = temp.name
    Path(name).replace(path)


def normalize(rule):
    parts = [p.strip() for p in rule.split(",")]
    kind = parts[0].upper()
    if kind not in TYPES:
        raise ValueError("unsupported type: " + kind)
    if len(parts) < 2 or not parts[1]:
        raise ValueError("missing rule value")
    if kind in {"DOMAIN", "DOMAIN-SUFFIX"}:
        if len(parts) != 2:
            raise ValueError("domain rule must not contain a policy")
        name = parts[1].rstrip(".").lower().encode("idna").decode("ascii")
        if len(name) > 253 or any(
            not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
            for label in name.split(".")
        ):
            raise ValueError("invalid domain: " + name)
        return f"{kind},{name}"
    if any(p != "no-resolve" for p in parts[2:]):
        raise ValueError("IP rule contains a policy or unknown option")
    net = ipaddress.ip_network(parts[1], strict=True)
    if not net.is_global:
        raise ValueError("non-public IP range")
    kind = "IP-CIDR6" if net.version == 6 else "IP-CIDR"
    return f"{kind},{net},no-resolve"


def suffix_match(name, suffix):
    return name == suffix or name.endswith("." + suffix)


def parse_line(raw, fmt):
    """Return (normalized rule or None, reason). Never execute source content."""
    text = raw.split("#", 1)[0].strip()
    if not text:
        return None, None
    if fmt == "v2fly":
        words = text.split()
        token, attrs = words[0], words[1:]
        if "@!cn" in attrs:
            return None, "境外业务属性 @!cn"
        if "@ads" in attrs:
            return None, "独立广告/遥测条目；沿用原有拦截"
        if token.startswith("include:"):
            return None, "分类引用未自动展开；需要的子分类已显式列入 manifest"
        if token.startswith("regexp:"):
            return None, "域名正则不能无损转换为本合集格式"
        if token.startswith("full:"):
            text = "DOMAIN," + token[5:]
        elif token.startswith("domain:"):
            text = "DOMAIN-SUFFIX," + token[7:]
        elif ":" in token:
            return None, "不支持的上游语法"
        else:
            text = "DOMAIN-SUFFIX," + token
    elif fmt == "domain-list":
        text = ("DOMAIN-SUFFIX," + text[1:]) if text.startswith(".") else "DOMAIN," + text
    elif fmt != "shadowrocket":
        raise ValueError("unknown source format: " + fmt)
    kind = text.split(",", 1)[0].upper()
    if kind not in TYPES:
        return None, "不采用 " + kind + "：USER-AGENT/进程规则不可靠，关键词/整 ASN 会误伤其他服务"
    return normalize(text), None


def filter_rule(rule, binding, manifest):
    kind, value, *_ = rule.split(",")
    selected = binding.get("only_suffixes")
    if selected and (kind not in {"DOMAIN", "DOMAIN-SUFFIX"} or not any(
        suffix_match(value, s) for s in selected
    )):
        return "不属于该 App 选定的业务域名"
    if kind.startswith("DOMAIN"):
        if any(value.split(".")[0].startswith(prefix) for prefix in binding.get("excluded_domain_prefixes", [])):
            return "集团云服务域名；没有证据表明整域专供该 App"
        if value in manifest.get("blocked_exact", []):
            return "境外服务独立主机"
        if value not in manifest.get("allowed_shared_cdn_hosts", []):
            if any(suffix_match(value, s) for s in manifest["blocked_suffixes"]):
                return "境外业务或整朵共享云/CDN，不能全局直连"
    return None


def refresh(manifest):
    """Fetch every source before replacing any cache; no silent stale fallback."""
    def fetch(source):
        last = None
        for attempt in range(3):
            try:
                request = urllib.request.Request(source["url"], headers={"User-Agent": "domestic-apps-rules-builder/1"})
                with urllib.request.urlopen(request, timeout=45) as response:
                    body = response.read()
                text = body.decode("utf-8")
                if not text.strip() or "<html" in text[:500].lower():
                    raise ValueError("source is empty or HTML")
                parsed = [parse_line(line, source["format"])[0] for line in text.splitlines()]
                if not any(parsed):
                    raise ValueError("source contains no usable rules")
                return source, body
            except Exception as exc:
                last = exc
                time.sleep(attempt + 1)
        raise RuntimeError(f"{source['id']}: {last}")

    results = []
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(fetch, source) for source in manifest["sources"]]
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as exc:
                failures.append(str(exc))
    if failures:
        raise RuntimeError("refresh failed; caches were not changed:\n" + "\n".join(failures))
    lock = {"fetched_on": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date().isoformat(), "sources": {}}
    for source, body in sorted(results, key=lambda item: item[0]["id"]):
        atomic_write(ROOT / source["cache"], body)
        lock["sources"][source["id"]] = {"url": source["url"], "sha256": hashlib.sha256(body).hexdigest()}
    atomic_write(DATA / "sources.lock.json", json_text(lock))


def render(manifest):
    lock = json.loads((DATA / "sources.lock.json").read_text())
    sources = {s["id"]: s for s in manifest["sources"]}
    # A foreign marker must apply across sources, not just the v2fly copy.
    # Otherwise the same overseas domain could re-enter through another list.
    manifest = dict(manifest)
    manifest["blocked_suffixes"] = list(manifest["blocked_suffixes"])
    manifest["blocked_exact"] = list(manifest.get("blocked_exact", []))
    for source in manifest["sources"]:
        if source["format"] != "v2fly":
            continue
        for line in (ROOT / source["cache"]).read_text().splitlines():
            words = line.split("#", 1)[0].split()
            if len(words) < 2 or "@!cn" not in words[1:]:
                continue
            token = words[0]
            if token.startswith("full:"):
                manifest["blocked_exact"].append(token[5:])
            elif token.startswith("domain:"):
                manifest["blocked_suffixes"].append(token[7:])
            elif ":" not in token:
                manifest["blocked_suffixes"].append(token)
    parsed = {}
    skipped = []
    provenance = {}
    for source in manifest["sources"]:
        body = (ROOT / source["cache"]).read_bytes()
        if source["url"] != lock["sources"][source["id"]]["url"]:
            raise ValueError("source URL changed without refreshing: " + source["id"])
        if hashlib.sha256(body).hexdigest() != lock["sources"][source["id"]]["sha256"]:
            raise ValueError("source snapshot checksum mismatch: " + source["id"])
        parsed[source["id"]] = []
        for number, line in enumerate(body.decode("utf-8").splitlines(), 1):
            rule, reason = parse_line(line, source["format"])
            if rule:
                parsed[source["id"]].append((number, rule))
            elif reason:
                skipped.append({"source": source["id"], "line": number, "text": line, "reason": reason})
    emitted = set()
    sections = []
    coverage = []
    for group in manifest["groups"]:
        own = set()
        for binding in group["uses"]:
            for number, rule in parsed[binding["source"]]:
                reason = filter_rule(rule, binding, manifest)
                if reason:
                    skipped.append({"group": group["id"], "source": binding["source"], "line": number, "text": rule, "reason": reason})
                    continue
                own.add(rule)
                record = provenance.setdefault(rule, {"groups": [], "sources": []})
                if group["id"] not in record["groups"]:
                    record["groups"].append(group["id"])
                origin = {"source": binding["source"], "line": number}
                if origin not in record["sources"]:
                    record["sources"].append(origin)
        for raw in group["rules"]:
            rule = normalize(raw)
            reason = filter_rule(rule, {}, manifest)
            if reason:
                raise ValueError("manual rule violates policy: " + rule + ": " + reason)
            own.add(rule)
            record = provenance.setdefault(rule, {"groups": [], "sources": []})
            if group["id"] not in record["groups"]:
                record["groups"].append(group["id"])
            origin = {"manual_group": group["id"], "evidence": group["evidence"]}
            if origin not in record["sources"]:
                record["sources"].append(origin)
        if not own:
            raise ValueError("group has no matching rules: " + group["id"])
        new = sorted(own - emitted, key=lambda rule: (rule.startswith("IP-"), rule))
        sections.extend(["", "# > " + " / ".join(group["apps"]), "# " + group["note"]])
        sections.extend(new or ["# 此组规则已由前面的共享域名覆盖。"])
        emitted.update(own)
        coverage.append({"id": group["id"], "apps": group["apps"], "coverage": group["coverage"], "candidate_rules": len(own), "new_rules": len(new), "note": group["note"]})
    counts = {kind: sum(rule.startswith(kind + ",") for rule in emitted) for kind in sorted(TYPES)}
    header = ["# 国内 App 直连合集 / Shadowrocket RULE-SET", "# Updated: " + lock["fetched_on"], "# Modified compilation by Goahead; generated from upstream snapshots and manual evidence.", "# Third-party rules retain their licenses; see domestic-apps/NOTICE.md and licenses/.", "# Total: " + str(len(emitted)), "# " + ", ".join(f"{k}: {v}" for k, v in counts.items()), "# Policy is assigned by RULE-SET,...,DIRECT in the configuration.", "# No USER-AGENT, PROCESS-NAME, DOMAIN-KEYWORD, or whole-cloud ASN rules.", "# Coverage and limitations: domestic-apps/COVERAGE.md"]
    report = {"fetched_on": lock["fetched_on"], "total_rules": len(emitted), "counts": counts, "groups": coverage, "rules": dict(sorted(provenance.items())), "excluded": skipped}
    md = ["# 截图国内 App 覆盖表", "", f"来源快照日期：{lock['fetched_on']}。去重后 **{len(emitted)}** 条规则。", "", "“社区规则”表示已合并公开规则，不等于真机全功能验证；“部分覆盖”表示只有经证实的端点/域名，尚缺交易、P2P 或第三方服务。域名后缀会匹配其全部子域，能够覆盖 API 与媒体连接，不局限于网页。", "", "| App / 公共服务 | 覆盖状态 | 本组规则 / 新增 | 说明 |", "| --- | --- | ---: | --- |"]
    for row in coverage:
        label = "社区规则" if row["coverage"] == "community" else "部分覆盖，待日志核验"
        md.append(f"| {'、'.join(row['apps'])} | {label} | {row['candidate_rules']} / {row['new_rules']} | {row['note']} |")
    md.extend(["", "## 未加入默认直连的截图 App", "", "| App | 原因 |", "| --- | --- |"])
    md.extend(f"| {'、'.join(entry['apps'])} | {entry['reason']} |" for entry in manifest["excluded_apps"])
    md.extend(["", "## 每组来源", "", "原始来源文件均保留在 upstream/；完整逐条来源、行号和剔除原因见 audit.json。仅删除完全重复的规则，保留便于追溯的子域规则。", ""])
    for group in manifest["groups"]:
        md.append("### " + "、".join(group["apps"]))
        md.append("")
        md.extend(f"- [{binding['source']}]({sources[binding['source']]['url']})" for binding in group["uses"])
        md.extend(f"- [官方/端点证据]({url})" for url in group["evidence"])
        md.append("")
    return {OUTPUT: "\n".join(header + sections) + "\n", DATA / "audit.json": json_text(report), DATA / "COVERAGE.md": "\n".join(md).rstrip() + "\n"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="download latest upstream snapshots, fail if any fetch fails")
    parser.add_argument("--check", action="store_true", help="verify deterministic generated files without writing")
    args = parser.parse_args()
    if args.refresh and args.check:
        parser.error("--refresh and --check cannot be combined")
    manifest = json.loads((DATA / "manifest.json").read_text())
    if args.refresh:
        refresh(manifest)
    outputs = render(manifest)
    stale = []
    for path, text in outputs.items():
        if args.check:
            if not path.exists() or path.read_text() != text:
                stale.append(str(path.relative_to(ROOT)))
        else:
            atomic_write(path, text)
    if stale:
        sys.exit("generated files are stale: " + ", ".join(stale))
    report = json.loads(outputs[DATA / "audit.json"])
    print(f"{'Verified' if args.check else 'Built'} {report['total_rules']} rules, {len(report['groups'])} groups; source date {report['fetched_on']}")


if __name__ == "__main__":
    main()

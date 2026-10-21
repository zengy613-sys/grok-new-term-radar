#!/usr/bin/env python3
"""大站内页更新监听：抓 sitemap，和上次快照对比，列出新增/删除的页面。

用法：python3 big-site-watch/check.py [--init]
输出：JSON 到 stdout（每个站的 added / removed），并更新 snapshots/<domain>.txt。
只用公开 sitemap，不登录。
"""
import gzip, json, re, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = "Mozilla/5.0 (compatible; new-term-radar/1.0)"
LOCALE = re.compile(r"^/[a-z]{2}(-[a-zA-Z]{2,4})?(/|$)")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data.decode("utf-8", "replace")


def collect(url, depth=0):
    xml = fetch(url)
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
    if "<sitemapindex" in xml and depth < 3:
        out = set()
        for sub in locs:
            out |= collect(sub, depth + 1)
        return out
    return set(locs)


def keep(u, domain, drop_locale):
    path = re.sub(r"^https?://[^/]+", "", u) or "/"
    if drop_locale and LOCALE.match(path):
        return False
    return domain in u


def main():
    init = "--init" in sys.argv
    cfg = json.loads((HERE / "sites.json").read_text())
    result = []
    for s in cfg["sites"]:
        snap = HERE / "snapshots" / f"{s['domain']}.txt"
        try:
            urls = {u.rstrip("/") or u for u in collect(s["sitemap"]) if keep(u, s["domain"], s.get("exclude_locale_prefixes"))}
        except Exception as e:
            result.append({"site": s["domain"], "error": str(e)})
            continue
        old = set(snap.read_text().split()) if snap.exists() else set()
        added = sorted(urls - old) if old and not init else []
        removed = sorted(old - urls) if old and not init else []
        snap.write_text("\n".join(sorted(urls)) + "\n")
        result.append({"site": s["domain"], "total": len(urls), "baseline": not old or init,
                       "added": added, "removed": removed})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

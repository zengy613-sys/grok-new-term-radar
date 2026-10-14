"""config.json: what to watch. If config.json is missing, config.example.json is used.

The defaults are the free monitor: Hugging Face, GitHub breakouts and the sitemaps in the
example file run with no key. Paid signals stay off (usecases and review per_day 0, weekly
signals on weekday -1, which never matches) until you opt in. Secrets are never read from
this file; they come from the environment.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import i18n, terms

DEFAULTS = {
    "lang": "en",
    "x_accounts": {"labs": [], "bloggers": []},
    "sitemaps": {},
    "topics": {},
    "known_terms": [],
    "stop_words": [],
    "judge": {"model": "local", "min_score": 0.5},
    "breakout": {"window_days": 14, "min_stars": 300, "velocity_min": 200, "delta_min": 400},
    "new_sites": {"queries": {"ai": "%ai%"}, "weekday": -1, "window_days": 90, "min_etv": 1000, "min_keywords": 20},
    "review": {"after_days": 14, "per_day": 0},
    "usecases": {"per_day": 0, "model": "claude-sonnet-4-6", "min_volume": 50, "trends_max": 10, "recheck_days": 3,
                 "location_code": 2840, "benchmark": "gpts", "min_daily": 300, "related": True, "related_geo": "US",
                 "country_trends": True, "country_min_volume": 1000, "country_max": 8},
    "competition": {"max_rows": 8, "weak_dr": 30, "location_code": 2840},
    "revenue": {"weekday": -1, "pages_growth": 3, "pages_new": 3, "min_revenue_usd": 500, "category": "", "max_leads": 10},
    "asks": {"weekday": -1, "time": "week", "min_score": 2, "model": "gpt-4.1-mini", "min_volume": 50, "max_leads": 12,
             "location_code": 2840, "patterns": [
                 '"is there an ai tool"', '"is there an ai that"', '"is there a tool that"', '"any ai tool for"',
                 '"looking for an ai tool"', '"i wish there was a tool"', '"is there a way to automatically"',
                 '"how do i automate"', '"tool that can automatically"', '"recommend an ai"', '"best ai tool for"',
                 '"ai tool that can"']},
    "pains": {"model": "gpt-4.1-mini", "extensions": 5, "review_pages": 2, "max_stars": 3, "reddit_time": "year", "videos": 3,
              "reddit_queries": ["{k} alternative", "{k} frustrating", '"{k}" "doesn\'t work"', "{k} wish there was"]},
    "tutorials": {"max_leads": 0, "videos": 3, "model": "gpt-4.1-mini"},
    "gsc": {},
}


def load(path: Path) -> dict:
    path = Path(path)
    # The free daily command works from a fresh clone: no config.json required.
    if not path.exists() and path.name == "config.json":
        example = path.with_name("config.example.json")
        if example.exists():
            path = example
    if not path.exists():
        raise SystemExit(f"{path} not found: copy config.example.json to {path.name} and edit it")
    raw = json.loads(path.read_text())
    cfg = {}
    for k, default in DEFAULTS.items():
        v = raw.get(k, default)
        cfg[k] = {**default, **v} if isinstance(default, dict) and default and isinstance(v, dict) else v
    cfg["_dir"] = path.resolve().parent
    i18n.set_lang(cfg["lang"])
    terms.add_stop(cfg["stop_words"])
    return cfg


def known(cfg: dict, term: str) -> str:
    """The entry of known_terms that already covers this term, if any: what you have a
    page for, or never want reported."""
    for k in cfg["known_terms"]:
        k = k.lower()
        if k and (k in term or term in k):
            return k
    return ""

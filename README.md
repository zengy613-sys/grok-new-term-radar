# new-term-radar

[中文说明](README.zh-CN.md)

A free daily report of names that are starting to surge in AI: new models, products, tools and repos, caught from public pages. No paid API key.

This repository is a fork of [zhuyansen/new-term-radar](https://github.com/zhuyansen/new-term-radar) by Yansen Zhu. The upstream project can also read X, Google Trends, domain data and a keyword table through paid APIs. Those paths are still in the code and **off by default**. This fork runs without them.

## Free daily run

Python 3.10 or newer. The radar uses only the standard library.

```bash
git clone https://github.com/zengy613-sys/grok-new-term-radar
cd grok-new-term-radar
python -m radar daily --out report.md
```

No `config.json` is required. When it is missing, the radar reads `config.example.json`. No `AISA_API_KEY`, `GOANYAPI_API_KEY`, `TRUSTMRR_API_KEY` or Resend key.

The first run builds snapshots (yesterday's Hugging Face list, star counts and sitemap URLs do not exist yet), so it reports GitHub breakouts and little else. From the second run on, every free signal reports what changed. `daily` also writes `report.json` beside the Markdown.

## What is on

| Signal | What it catches | Needs |
|---|---|---|
| Hugging Face | Models and Spaces new to the trending top 50. Quantised copies and a model's own demo are grouped under the base name | nothing |
| GitHub breakout | A repo under 14 days old averaging 200+ stars a day, or +400 since yesterday, plus the search variants people use ("niko strata") | nothing (optional `GITHUB_TOKEN` raises the rate limit) |
| Sitemaps | Words that several new URLs on a site share and its older URLs rarely carried | the sitemaps in the example config |
| Name judge | A local heuristic: drop stop words, `known_terms`, common words, and long fine-tune titles | nothing |

The example config watches these directories: toolify, ai-bot.cn, futurepedia, aixploria, opentools, dang.ai, clipfly, aitoptools, glama, mcp.so, and lobehub (MCP and skills).

Paid paths stay off and are skipped, they do not fail the run:

| Path | Default |
|---|---|
| X posts, new-site whois, Reddit asks, TrustMRR revenue | `weekday` is `-1` (never matches a day) or `x_accounts` is empty. X with handles but no `AISA_API_KEY` is skipped |
| Keyword table (`usecases`) and the 14-day Trends review | `per_day` is `0` |
| Tutorial-comment lookup | `tutorials.max_leads` is `0` |

Search Console stays off until you set `gsc.site` and a token. It does not need a paid key.

## The local name judge

`judge.model` is `"local"`. Each term is scored without a model:

- a phrase made only of stop words (`claude code`) scores 0
- a term you listed in `known_terms` scores 0 and is not kept for later
- a phrase made only of common words (`dashboard`, `video generator`, `today`) scores under `min_score` (0.5) and is listed as an other rising term
- a long fine-tune title (six or more words, or four or more with a quantisation or fine-tune marker such as `gguf`, `uncensored`, `lora`, `q4`) is suppressed the same way
- what remains (`strata`, `krea 2`, `claude opus 5.5`) leads the report

Set `judge.model` to a chat model name and export `AISA_API_KEY` if you want the upstream model judge instead. `--skip judge` lists every term unsorted.

## config.json

Copy `config.example.json` when you want to change the watch list. Secrets never go in this file.

| Key | What it is |
|---|---|
| `lang` | `"en"` or `"zh"` |
| `sitemaps` | Sites whose new pages you want. `index` is a sitemap or a sitemap index; `shards` (a regex) picks sub-sitemaps; `pause` is the seconds between requests; `strip_locale` drops `/en/` and `/zh-CN/` so one entry in many languages counts once |
| `topics` | Name and regex. Each topic gets a section of matching leads and repos |
| `known_terms` | Terms you already cover. A lead that contains one, or is contained in one, is marked and not kept |
| `stop_words` | Extra everyday words, added to the built-in list |
| `judge` | `"local"` and `min_score` (0.5), or a paid chat model |
| `breakout` | `window_days`, `min_stars`, `velocity_min` (stars a day), `delta_min` (stars since yesterday) |
| `x_accounts`, `new_sites`, `revenue`, `asks`, `review`, `usecases` | Paid. Leave the example values (`per_day` 0, `weekday` -1, empty X accounts) to keep them off |

Please read each site's robots.txt before you add its sitemap, and keep `pause` at or above its crawl-delay.

## Run it on GitHub Actions

`.github/workflows/radar.yml` runs `python -m radar daily --out report.md` once a day. It is off until you opt in:

1. Fork the repository (a private fork is fine). You do not need to commit a `config.json`.
2. Settings → Secrets and variables → Actions → Variables. Set `RADAR_ENABLED` to `true`.
3. No secrets. The workflow uses the automatic `GITHUB_TOKEN` only, so the breakout search has a higher rate limit.

State (`state/radar.db` and the snapshots) is restored and saved with the Actions cache. The report is written to the run summary and uploaded as the `radar-daily-<run id>` artifact (`report.md`, `report.json`, `state/radar.db`) for 30 days. Download the artifact now and then if you care about the history in the database: a missing cache only means the next run builds new snapshots.

You can also run it by hand from the Actions tab (`workflow_dispatch`).

## Optional paid signals

The upstream signals are still here. Turn one on only when you have the key it needs, then run again. A missing key is skipped; the rest of the report is still written.

- **X.** Put handles in `x_accounts.labs` and `x_accounts.bloggers` and set `AISA_API_KEY`.
- **Keyword table and review.** Set `usecases.per_day` and `review.per_day` above 0. Both call AIsa. `GOANYAPI_API_KEY` adds related queries. See upstream for what the table contains.
- **New sites, Reddit asks, TrustMRR revenue.** Set `weekday` to `0`–`6` (Monday is 0) or pass `--new-sites`, `--asks`, `--revenue`. New sites and asks need `AISA_API_KEY`. Revenue needs `TRUSTMRR_API_KEY`.
- **Mail.** `--mail` with `RESEND_API_KEY`, `EMAIL_FROM` and `RADAR_EMAIL_TO`.

`python -m radar pains "ai headshot"` and `python -m radar keywords "name"` are the paid lookups. They are not part of the free daily run.

## Development

```bash
pip install pytest
python -m pytest -q tests
```

The tests cover the logic and call no network.

## Thanks and license

Upstream project: [zhuyansen/new-term-radar](https://github.com/zhuyansen/new-term-radar). Copyright (c) 2026 Yansen Zhu.

- [子木 @CoderJeffLee](https://x.com/CoderJeffLee) for the idea behind the keyword table.
- [饭特稀 | Fentix @fantexi997](https://x.com/fantexi997) for GoAnyAPI, the optional source of related queries.

The diagram in `docs/` is drawn by `docs/make_diagram.py`.

MIT. See [LICENSE](LICENSE). The copyright notice and this permission notice stay with the upstream author.

<!-- mcp-name: io.github.zhuyansen/new-term-radar -->

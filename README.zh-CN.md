# new-term-radar（新词雷达）

[English](README.md)

一份免费的日报，列出 AI 领域里刚开始冒头的名字：新模型、新产品、新工具、新仓库。数据来自公开页面，不需要任何付费 API key。

本仓库 fork 自 Yansen Zhu 的 [zhuyansen/new-term-radar](https://github.com/zhuyansen/new-term-radar)。上游还可以用付费接口读 X、Google Trends、域名数据和新词表。这些路径仍在代码里，**默认关闭**。这个 fork 不依赖它们就能跑。

## 免费日报

需要 Python 3.10 或更新版本。雷达只用标准库。

```bash
git clone https://github.com/zengy613-sys/grok-new-term-radar
cd grok-new-term-radar
python -m radar daily --out report.md
```

不需要 `config.json`。文件不存在时，雷达读取 `config.example.json`。不需要 `AISA_API_KEY`、`GOANYAPI_API_KEY`、`TRUSTMRR_API_KEY`，也不需要 Resend。

第一次运行只建立快照（还没有昨天的 Hugging Face 榜单、星数和 sitemap 网址），所以当天主要报出 GitHub 爆发仓库。从第二次开始，每个免费信号报告变化。`daily` 还会在 Markdown 旁边写一份 `report.json`。

## 默认打开的信号

| 信号 | 抓什么 | 需要 |
|---|---|---|
| Hugging Face | 新进热门榜前 50 的模型和 Space。量化版、微调版和模型自己的 demo 归到同一个基础名下 | 无 |
| GitHub 爆发 | 创建不到 14 天、平均每天涨 200 星以上，或比昨天多 400 星的仓库，并附上大家会搜的写法（「niko strata」） | 无（可选 `GITHUB_TOKEN`，提高接口限额） |
| Sitemap | 某个站新增的几个网址共用、而它的旧网址里很少出现的词 | 示例配置里的 sitemap |
| 名字判断 | 本地规则：丢掉停用词、`known_terms`、普通词，以及很长的微调标题 | 无 |

示例配置盯着这些目录：toolify、ai-bot.cn、futurepedia、aixploria、opentools、dang.ai、clipfly、aitoptools、glama、mcp.so，以及 lobehub（MCP 和 skills）。

付费路径默认关闭，会干净地跳过，不会让这次运行失败：

| 路径 | 默认 |
|---|---|
| X 帖子、新站 whois、Reddit 求助、TrustMRR 收入 | `weekday` 为 `-1`（对不上任何一天），或 `x_accounts` 为空。写了 X 账号但没有 `AISA_API_KEY` 时也会跳过 |
| 新词表（`usecases`）和 14 天后的 Trends 复盘 | `per_day` 为 `0` |
| 教程评论 | `tutorials.max_leads` 为 `0` |

Search Console 在你设置 `gsc.site` 和 token 之前关闭。它不需要付费 key。

## 本地名字判断

`judge.model` 是 `"local"`。每个词不调用模型：

- 只由停用词组成的短语（`claude code`）得 0 分
- 写在 `known_terms` 里的词得 0 分，并且不会被留下来
- 只由普通词组成的短语（`dashboard`、`video generator`、`today`）低于 `min_score`（0.5），列在「其他上升词」里
- 很长的微调标题也会被压下去：六个词及以上，或者四个词及以上且带量化、微调标记（`gguf`、`uncensored`、`lora`、`q4`）
- 剩下的（`strata`、`krea 2`、`claude opus 5.5`）排在报告前面

如果改用上游的模型判断，把 `judge.model` 设成聊天模型名，并设置 `AISA_API_KEY`。`--skip judge` 则不做筛选，所有词都列出来。

## config.json

要改监控名单时，复制 `config.example.json`。密钥不要写进这个文件。

| 键 | 含义 |
|---|---|
| `lang` | `"en"` 或 `"zh"` |
| `sitemaps` | 要看新增页面的站。`index` 是 sitemap 或索引；`shards`（正则）挑选子 sitemap；`pause` 是请求间隔秒数；`strip_locale` 去掉 `/en/`、`/zh-CN/`，同一种语言的多份只算一次 |
| `topics` | 名称和正则。每个主题单独一节，列出匹配的线索和仓库 |
| `known_terms` | 你已经覆盖的词。线索包含它，或被它包含，会被标出且不保留 |
| `stop_words` | 额外的日常用词，加到内置列表上 |
| `judge` | `"local"` 和 `min_score`（0.5），或者一个付费聊天模型 |
| `breakout` | `window_days`、`min_stars`、`velocity_min`（每天星数）、`delta_min`（比昨天多的星） |
| `x_accounts`、`new_sites`、`revenue`、`asks`、`review`、`usecases` | 付费。保持示例里的值（`per_day` 为 0、`weekday` 为 -1、X 账号为空）就是关闭 |

添加 sitemap 之前请先看该站的 robots.txt，`pause` 不要低于它的 crawl-delay。

## 在 GitHub Actions 上每天跑

`.github/workflows/radar.yml` 每天运行一次 `python -m radar daily --out report.md`。默认不启用，需要你打开：

1. Fork 这个仓库（私有 fork 也可以）。不必提交 `config.json`。
2. Settings → Secrets and variables → Actions → Variables，把 `RADAR_ENABLED` 设为 `true`。
3. 不需要添加任何 secret。工作流只用自动的 `GITHUB_TOKEN`，给爆发仓库搜索更高的接口限额。

状态（`state/radar.db` 和各快照）通过 Actions cache 恢复和保存。报告会写进该次运行的摘要，并作为产物 `radar-daily-<运行 id>` 上传（`report.md`、`report.json`、`state/radar.db`），保留 30 天。如果在意数据库里的历史，请不时下载这个产物：缓存丢失只表示下一次会重新建快照。

也可以在 Actions 页面手动运行（`workflow_dispatch`）。

## 可选的付费信号

上游的信号还在。只有当你有对应的 key 时再打开，然后重新运行。缺 key 会跳过，报告的其余部分照常写出。

- **X。** 在 `x_accounts.labs` 和 `x_accounts.bloggers` 里写账号，并设置 `AISA_API_KEY`。
- **新词表和复盘。** 把 `usecases.per_day` 和 `review.per_day` 设成大于 0。两者都调用 AIsa。`GOANYAPI_API_KEY` 会补上相关查询。表里有什么，见上游说明。
- **新站、Reddit 求助、TrustMRR 收入。** 把 `weekday` 设成 `0`–`6`（周一是 0），或加上 `--new-sites`、`--asks`、`--revenue`。新站和求助需要 `AISA_API_KEY`。收入需要 `TRUSTMRR_API_KEY`。
- **邮件。** `--mail`，并设置 `RESEND_API_KEY`、`EMAIL_FROM`、`RADAR_EMAIL_TO`。

`python -m radar pains "ai headshot"` 和 `python -m radar keywords "名字"` 是付费查询，不属于免费日报。

## 开发

```bash
pip install pytest
python -m pytest -q tests
```

测试覆盖逻辑，不访问网络。

## 致谢与许可

上游项目：[zhuyansen/new-term-radar](https://github.com/zhuyansen/new-term-radar)。Copyright (c) 2026 Yansen Zhu。

- [子木 @CoderJeffLee](https://x.com/CoderJeffLee)：新词表的想法来自他的建议。
- [饭特稀 | Fentix @fantexi997](https://x.com/fantexi997)：GoAnyAPI，相关查询这个可选数据源。

`docs/` 里的图由 `docs/make_diagram.py` 生成。

MIT。见 [LICENSE](LICENSE)。版权声明和许可声明保留给上游作者。

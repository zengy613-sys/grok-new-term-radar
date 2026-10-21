# 新词监听方法论 SOP

维护人：view（Yvette 的新词助手）。每次跑完任何一个监听任务，如果方法有变化或学到新东西，就更新本文件末尾的「经验日志」，并和当天的记录一起推到 main。

通用规则
- 只用公开信息，不登录，不编造；查不到就写"未发现"或说明报错原因。
- 不用付费 X API、不打印或提交任何令牌。
- 所有模块之间去重：同一个工具或新词只推一次（查最近的聊天记录和 findings）。
- 提交只动本模块相关的文件，作者用 zengy613-sys，直接推 main。

## 模块总览

| 模块 | 时间（北京时间） | 数据来源 | 记录位置 |
|---|---|---|---|
| 新词雷达日报 | 每天 07:17 左右 | `run_local.sh` 跑 radar：Hugging Face 热榜、GitHub 新仓库飙星、导航站 sitemap 新词 | `/workspace/radar-reports/日期.md`（本地） |
| AI 生成玩法简报 | 工作日 08:51 | X 搜索：图片/视频生成新玩法、提示词、TikTok 爆款格式 | 聊天里的简报 |
| 导航站上新与新词提醒 | 工作日 09:52 | Toolify、TAAFT、Futurepedia、AI-bot.cn、Product Hunt 新收录 + X 新词 | 聊天里的提醒 |
| 大站内页更新监听 | 工作日 11:00 左右 | 大站公开 sitemap，比对新增/删除页面 | `big-site-watch/` |
| 站长监听 | 工作日 14:30 左右 | 站长指纹（文案、模板、素材路径）+ 证书透明日志 + 新梗词域名 | `site-owner-watch/` |

## 1. 新词雷达日报
1. 跑 `./run_local.sh`（约 4–5 分钟，先 pull 再 `python -m radar daily --state state`）。
2. 读当天报告，挑 4–6 条最值得导航站收录的新工具/新模型/新词，优先 AI 图片和视频。
3. 跳过 NSFW、站点地图杂项、前几天和 09:52 提醒里发过的。每条附链接和上站理由。
4. 失败时报告卡在哪一步和 .log 关键报错。

## 2. AI 生成玩法简报
1. X 上搜过去 24 小时（周一含周末）的图片/视频生成新玩法、新模型、提示词技巧、TikTok 爆款 AI 内容。
2. 优先互动高、有可复用方法或示例的帖子；去广告、去重。
3. 按「图片生成 / 视频生成 / TikTok 内容技巧」分组，每条一两句加原帖链接。

## 3. 导航站上新与新词提醒
1. 看主流导航站最近 24 小时新收录或热度上升的工具；X 上搜新发布、热议的工具和新词。
2. 和之前提醒、当天雷达日报去重。
3. 推荐 5–10 个上站工具（每个一句话 + 官网或来源链接）、列新关键词，结尾督促上站。

## 4. 大站内页更新监听
1. `git pull` 后跑 `python3 big-site-watch/check.py`：抓 `sites.json` 里每个站的 sitemap（支持 sitemap 索引和 .gz），去掉 /zh/、/ja/ 等多语言重复页，和 `snapshots/<域名>.txt` 比对。
2. 新增页面从路径推测新工具/新模型/新玩法词，必要时打开页面看标题确认；写进 `findings.md`。
3. 加站：往 `sites.json` 加一条，先跑一次建基线（首次不算新增）。
4. 注意：很多站 sitemap 的 lastmod 是统一构建时间，没参考价值，只比 URL。

## 5. 站长监听
1. 读 `site-owner-watch/watchlist.md` 的监听对象、指纹和手段。
2. 搜标志性文案；certspotter 查新域名（crt.sh 有限流）；新梗词 + "ai generator"/"ai video" 找精确匹配新域名。
3. 至少匹配 1 条强指纹才算"确认"，只匹配中/弱指纹算"疑似"。写进 `findings.md`。
4. 发现指纹不独特（被无关站共用）就降级并在 watchlist 注明原因。

## 经验日志
- 2026-10-21：supermaker.ai、kimg.ai 的 sitemap lastmod 全是同一构建时间，只能比 URL 集合；pixomi.ai 用 sitemap 索引（static + 多个 landing 子文件）。
- 2026-10-21：站长监听首跑发现 "Credits back if a render fails" 被无关站（popstarai.video、iwannaloveyouai.video）共用，已从强指纹降为中。
- 2026-10-21：梗视频站的新梗词可以参考 Know Your Meme 本周热门；跟风站多（≥5 个）的梗适合在导航站做"梗视频生成器"合集。

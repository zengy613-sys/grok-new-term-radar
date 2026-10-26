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
5. .md 报告里图片/视频条目少时，去同名 .json 的 `sitemap.sites.*.sample` 看各导航站新收录的 URL（dang、aitoptools、glama 常有新视频工具），必要时打开页面确认再推荐。

## 2. AI 生成玩法简报
1. X 上搜过去 24 小时（周一含周末）的图片/视频生成新玩法、新模型、提示词技巧、TikTok 爆款 AI 内容。
2. 优先互动高、有可复用方法或示例的帖子；去广告、去重。
3. 按「图片生成 / 视频生成 / TikTok 内容技巧」分组，每条一两句加原帖链接。
4. X 搜索 API 不支持 min_faves，会被自动去掉；用 sort_order=relevancy 并自己看 public_metrics（收藏数、浏览量）筛，名人仿妆类 Nano Banana 提示词帖互动高但不算玩法，跳过。

## 3. 导航站上新与新词提醒
1. 看主流导航站最近 24 小时新收录或热度上升的工具；X 上搜新发布、热议的工具和新词。
2. 和之前提醒、当天雷达日报去重。
3. 推荐 5–10 个上站工具（每个一句话 + 官网或来源链接）、列新关键词，结尾督促上站。
4. 最好用的来源是 TAAFT 的 `https://theresanaiforthat.com/just-released/`（WebFetch 能读，带发布时间和趋势排名）；Product Hunt 的 AI 话题页只有老牌产品，没有每日新品。X 上用「launch/introducing + AI video/video model」按 relevancy 搜，最容易抓到新模型名。

## 4. 大站内页更新监听
1. `git pull` 后跑 `python3 big-site-watch/check.py`：抓 `sites.json` 里每个站的 sitemap（支持 sitemap 索引和 .gz），去掉 /zh/、/ja/ 等多语言重复页，和 `snapshots/<域名>.txt` 比对。
2. 新增页面从路径推测新工具/新模型/新玩法词，必要时打开页面看标题确认；写进 `findings.md`。
3. 加站：往 `sites.json` 加一条，先跑一次建基线（首次不算新增）。
4. 注意：很多站 sitemap 的 lastmod 是统一构建时间，没参考价值，只比 URL。

## 5. 站长监听
1. 读 `site-owner-watch/watchlist.md` 的监听对象、指纹和手段。
2. 搜标志性文案；certspotter 查新域名（crt.sh 有限流）；新梗词 + "ai generator"/"ai video" 找精确匹配新域名；#2 再查 Startup Fame 投稿页和已确认站页脚外链。
3. 至少匹配 1 条强指纹才算"确认"，只匹配中/弱指纹算"疑似"。写进 `findings.md`。复合强指纹（如 studio-console + sc-step-card）缺一不可；单句免责声明（independent tool / independent fan tool）很多跟风站都写，不够确认。
4. 发现指纹不独特（被无关站共用）就降级并在 watchlist 注明原因。

## 经验日志
- 2026-10-21：supermaker.ai、kimg.ai 的 sitemap lastmod 全是同一构建时间，只能比 URL 集合；pixomi.ai 用 sitemap 索引（static + 多个 landing 子文件）。
- 2026-10-21：站长监听首跑发现 "Credits back if a render fails" 被无关站（popstarai.video、iwannaloveyouai.video）共用，已从强指纹降为中。
- 2026-10-21：梗视频站的新梗词可以参考 Know Your Meme 本周热门；跟风站多（≥5 个）的梗适合在导航站做"梗视频生成器"合集。
- 2026-10-21：深挖 popstarai.video 时最有用的线索是导航站的投稿人主页：Startup Fame 站点页上的 rel="author" 链接直接列出同一账号的 18 个站。之后用"`p.<域名>` 自建 Plausible + Zoho MX + 固定 Cloudflare NS 对"三件套批量核对，再顺着页脚友链和"共用支持邮箱的同页面站"（z-image-ai.com 写着 support@gptimage-2.com）把另外两个 CF 账号连了进来。注意友链里也有别的团队（飞书邮箱 + GA 那一伙），不能见链接就算。
- 2026-10-22：雷达 .md 的候选词表偏文本模型/GitHub，今天 4 条图片视频推荐全部来自 .json 里 sitemap 的新 URL 样本（Seedance 3.0、ManyMotions、aiMakeVideo、AIRAP）；toolify 的 sitemap 读不到 URL，待查。ai-bot.cn 一次冒出 681 个"新"URL 多是老条目重新进 sitemap，别当新货。
- 2026-10-22：X 搜索的 min_faves 过滤无效（API 直接删掉），玩法简报改为 relevancy 排序 + 看收藏/浏览量人工筛；中文搜「提示词/玩法 + 豆包/Seedance」比英文搜更容易出可复用技巧。
- 2026-10-22：导航站提醒里，TAAFT 单个工具页（`/ai/<slug>/`）从盒子 curl 会 403，没有官网域名的工具先链到 TAAFT just-released 列表页；Product Hunt AI 话题页没有当日新品，别指望它。今天的新模型词（Topview T1、VideoGen Model 1）都来自 X 的发布帖。
- 2026-10-22：大站内页监听首次正式比对，supermaker.ai 一天上 4 页，全是梗/节日词（Female Malfoy、GTA 风、万圣节换装、厄齐尔进球）；从盒子 curl 页面 `<title>` 和 meta description 就能确认新词，不用开浏览器。
- 2026-10-22：站长监听拼梗名域名时，imageat.com/tiktok-ai-trends（每月 TikTok AI 趋势表）是好用的梗词来源；用 dns.google 的 DoH 接口批量查 NS/MX 比 dig 方便（盒子上没有 dig）。抓页面要加 `--compressed`，grep 加 `-a`，不然很多页面被当成二进制漏判。"independent tool" 这类免责声明句很多跟风站都写，不能当强指纹。
- 2026-10-23：雷达 .md「AI video」专题又是空的，候选词仍偏文本/GitHub；图片视频仍靠 .json sitemap sample（dang 全量新 3 条、aitoptools 全量新 4 条、ai-bot.cn 只给 new[:8]）。ai-bot.cn 再次冒出 689「新」URL，只跟样本里当天页（BaoCut 等），其余按 10-22 经验当重刷。dang/aitoptools 的成人向工具（DeepSwapFace 列表图带 nsfw、CelebMakerAI 自述 porn）直接跳过。snapshot 跑完就被覆盖，当天若要挖 ai-bot 全量 new，得在 run 结束立刻从 sample/new 另存，否则只剩 sample 8 条。
- 2026-10-23：导航站提醒里，Canva Craft 这类大厂首发模型词比导航站收录早半天到一天，优先跟 X 官宣帖 + 新闻稿；Toolify 的 `/new`（Just launched）在 sitemap 读不到 URL 时仍可用 WebFetch 扫一遍，能补到 Say It Again、Prolifik、CreateVision（Kling 4.0 Online）这类视频工具。
- 2026-10-23：大站同日上「模型页」比梗页更值得跟——今天 supermaker 上 PixVerse V6 Max、pixomi 上 FLUX 3 Klein，都是可直接占模型词条的信号；两站还同日上了 /video/ai-prompt-generator，提示词工具页可当弱信号。梗/节日页（南瓜头、Sorry I Lied、Charme Dance、Plug Walk）仍可记，但优先级低于新模型名。
- 2026-10-23：站长监听例行无新站。"independent fan tool" 被 jeanphil / closedonsunday / burningbridges 等多家无关跟风站共用，已从 #2 强指纹组拆出降为弱；确认 #2 梗站仍以 studio-console + sc-step-card + p.<域名> Plausible + Zoho + 固定 NS 对为准。新梗词继续用 imageat 趋势表 + 当天 big-site-watch 新增页（Charme Dance、Plug Walk、Malfoid 等）拼域名，dns.google DoH 批量查 A/NS/MX。
- 2026-10-24：雷达 .md「AI video」仍空；图片视频继续靠 .json sitemap sample（dang 9 新/样本 8：BudgetPixel、BeautyPlus 等；aitoptools 1 新：Image To 3D→imageto3d.studio；ai-bot.cn 又报 685「新」URL，样本多为旧条目重刷，勿整表当新货）。MiniMax M3.1 Flash 在 HF 再上榜但 10-20 已发过，换脸类 Space（ltx2 faceswap）直接跳过。GitHub 飙星里 wesbos/3d-model-anything（LiDAR→Three.js）比电视桌面/解密类更值得导航站跟。toolify sitemap 仍读不到 URL。
- 2026-10-25：雷达 .md「AI video」仍空；图片视频继续靠 .json sitemap sample（dang 4 新全进样本：DemoRiff 等；aixploria 18 新/样本 8：Arting、FreeMaker、Any Video Converter 等；aitoptools 0 新）+ HF 热榜（从 state/hf_top.json.gz 可见 LTX-2.5、Drama-3，.md 候选词表只写了 DeepSeek 文本向）。DemoRiff 官网是 demoriff.com（dang 页无直链时可用常见域名探测）。ai-bot.cn 又报 687「新」URL，样本仍是旧条目重刷。toolify sitemap 仍读不到 URL。
- 2026-10-26：雷达 .md「AI video」仍空；图片视频继续靠 .json sitemap sample（dang 7 新全进样本：Nano Banana 3 等；opentools 3 新：Plimo/Agentik/Panzoe；ai-bot.cn 仅 2 新且含 Hy-Nomas，今天可整表采信，不像前几天 680+ 重刷）+ HF 热榜（state/hf_top：FLUX 3 Klein、SAM 3、LTX-2.5 等，.md 候选词只写了 Nanbeige4.3 文本向）。「Nano Banana 3」官网 nanobanana3.design 是第三方在线站，Google 官方线仍是 Nano Banana 2.1/Pro，上站勿写成官方三代。FLUX 3 Image Klein 开源权重可本地，大站内页 10-23 已见但雷达日报此前未推。toolify sitemap 仍读不到 URL；aixploria/aitoptools 今天 0 新。
- 2026-10-26：周一玩法简报覆盖周末（since 周五 00:00 UTC）。中文「提示词/工作流/玩法 + Seedance/Kling/Nano Banana」仍比英文泛搜更容易出可复用方法；英文 relevancy 里工具清单/广告帖噪声大，优先看有具体步骤的帖（Skill OS、Draft 样片、区域编辑、工具栈清单）。跳过纯模型对比（周末大量 Seedance vs Kling 复读）与 NSFW/仿妆提示词。

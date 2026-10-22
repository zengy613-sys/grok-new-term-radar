# 监听对象

## #1 梗视频站长（身份未公开）
- 来源：需求分析 bot 交接，2026-10-21
- 身份：无公司名、无社媒；推测是国内独立开发者（弱）
- 打法：TikTok「一张照片变成我」类梗一火，几天内注册梗名精确匹配域名，一天内上线；同一套模板复制；一次性点数包约 $9/条；靠梗关键词自然搜索。

### 已确认站点
- https://dimedimebaby.app/ ，2026-10-19 注册，Dime Dime Baby 梗视频，$9.90/$19.90/$29.90
- https://ozilgoalaigenerator.com/ ，2026-10-14 注册，厄齐尔进球梗视频，$8.90/$18.90/$28.90

### 指纹
- 强：文案 "Photo deleted once your video is made"、"which is why the photo box is empty when you come back"
- 弱：条款写 "independent tool"（2026-10-22 发现无关站 burningbridgesai.app、unforgettablecar.com 页脚也写 "independent tool, not affiliated with…"，已从强降为弱）
- 中：文案 "Credits back if a render fails"（2026-10-21 发现无关站 popstarai.video、iwannaloveyouai.video 也在用，已从强降为中）
- 强：素材路径 r2.<域名>/site/<梗名>/，图标 /brand/mark.svg，接口 /api/meme/generate
- 中：ShipAny 模板（shipanyai/shipany-template-two + better-auth），首页 JS 文件哈希大量相同；部署在 Vercel
- 中：GA ID G-ZFD4YV344W（公开反查暂无结果）
- 弱：Cloudflare 注册 + Cloudflare NS 同一对 martha/rajeev（很多账号共用）
- 弱：邮箱 support@<域名>（Cloudflare 邮件转发）

### 监听手段
1. 网页 / X 搜上面的标志性文案（网页搜 "Photo deleted once your video is made" 和 "photo box is empty" 最好用，直接返回他的站）
2. 证书透明日志查新域名：certspotter 可用；crt.sh 有限流
3. 当下 TikTok / X 新梗词 + "ai generator" / "ai video" 的新注册精确匹配域名，打开后对指纹
4. 候选站至少匹配 1 条强指纹才算"确认"，只匹配中/弱的算"疑似"

## #2 popstarai.video 站长（Startup Fame 署名 "Joaquin Garcia"，疑似关联主体 ZheLogic）
- 来源：Yvette 让深挖 popstarai.video，2026-10-21
- 身份：Startup Fame 投稿账号 startupfa.me/catalinagarciasimon639（显示名 "Joaquin Garcia"，句柄和显示名对不上，像化名），名下挂 18 个站。另一组同模板站把统计放在自建 Plausible plausible.zhelogic.com 上，ZheLogic（zhelogic.com，地址是占位的 "123 Innovation Way"，X 账号 @zhelogic 已被封，GitHub 组织 ZheLogic 0 个公开仓库）可能是他的品牌/主体（中）。真实姓名、国籍未公开。
- 打法：两条线并行。① 新模型/竞品词站：krea3.pro、minih3.pro、gptimage-2.com、seed-audio.com 这类"模型名精确匹配域名"，新模型一出就上；② 梗视频站：TikTok/IG 梗一火几天内注册 `<梗名>ai.video`（popstarai.video 10-13、bulin47ai.video 10-09、roadsterai.video 10-17）。每站带一堆攻略页（trend、how-to、prompt、alternatives、editorial-policy），批量投 20+ 个导航站换外链。
- 定价：一次性点数包 $6.99/$9.99/$14.99/$24.99 起 + 月订阅 $29.90/$49.90（年付 $99.90/$499.90，即 $8.33/$41.67 每月）；渲染失败退点数。
- 与 #1 对比：不是同一人。#1 是 Vercel + Cloudflare 注册 + NS martha/rajeev + CF 邮件转发 + GA；#2 是 Spaceship 注册 + Cloudflare 托管 + NS harvey/kira、alex/tia、jason/margot + Zoho 企业邮箱 + 自建 Plausible，没有 GA。两边都用 ShipAny 模板和 r2.<域名>，这两点很多人都用，不能当关联证据。

### 已确认站点（Startup Fame 同账号 + 下方强指纹）
- 梗视频：popstarai.video（2026-10-13）、roadsterai.video（2026-10-17）
- 视频/图片：z-video.co、minih3.pro（2026-08-07）、krea3.pro、krea-2.pro、krea2turbo.pro（三站都是 2026-07-28 同一分钟注册）、image2image.app（2025-10-07）、getimgai.org（2026-04-22）、meigenai.co
- 语音/转写：speechnotes.org、speechtext.co、audioconvert.app、gpt-transcribe.org、omni-voice.app、voiceart.app、elevenai.app、fishvoices.com
- 高置信（不在 Startup Fame 列表，靠指纹 + 互链）：bulin47ai.video（2026-10-09）、whisper-ai.app、musevoice.pro、miso-one.com、seed-audio.com、gptimage-2.com、imgai.pro、z-image-ai.com、happyhorseai.video、nano-banana-pro.co、seedance2ai.video、bananaproai.app
- 明细和低置信候选见 findings.md

### 指纹
- 强：统计用 Plausible 反代子域 `p.<域名>/js/script.file-downloads[.hash].outbound-links.pageview-props.revenue.tagged-events.js`（脚本字节与 plausible.zhelogic.com 完全相同，和 plausible.io 官方版不同）
- 强：Startup Fame 投稿账号 catalinagarciasimon639 / "Joaquin Garcia"
- 强：站与站共用支持邮箱（z-image-ai.com、imgai.pro 页面写的都是 support@gptimage-2.com，Plausible 都走 p.imgai.pro）
- 强（梗站专用）：`data-theme="studio-console"` + CSS 类 `sc-step-card`，攻略页结构 /<梗>-trend、/how-to-do-<梗>-trend、/<梗>-alternatives、/editorial-policy，文案 "Draft Survives Sign-In"、"independent fan tool"、竞品信息"标注核对日期"
- 中：Cloudflare NS 固定三对 harvey/kira、alex/tia、jason/margot（代表 3 个 CF 账号，单看也可能撞别人）
- 中：MX 是 Zoho（mx/mx2/mx3.zoho.com）+ SPF include:zohomail.com + DMARC p=reject，邮箱 support@<域名>
- 中：自建 Plausible plausible.zhelogic.com（ZheLogic）
- 中：价格梯度 $6.99/$9.99/$14.99/$24.99 包 + $29.90/$49.90 月订阅 + $99.90/$499.90 年付
- 弱：Spaceship 注册；ShipAny Two 模板（后台配置里有 affonso、promotekit、creem 字段）；r2.<域名> 证书；"Credits back if a render fails"（iwannaloveyouai.video 等无关站也用）

### 监听手段
1. 定期打开 startupfa.me/catalinagarciasimon639，看有没有新挂的站
2. 已确认站的页脚/攻略页外链里冒出的新域名，逐个查 `p.<域名>` Plausible + Zoho MX + NS 对
3. 新梗词 + "ai.video" 拼域名（如 `<梗>ai.video`），查 RDAP（Spaceship）和 NS 对；新模型名（krea/minimax/seedance/gpt-image 等）+ .pro/.app/.co 同理
4. certspotter 查候选新域名的证书时间（梗站一般注册当天出证书）
5. 确认规则：Startup Fame 同账号，或 p.<域名> Plausible + Zoho + 三对 NS 之一同时满足，才算确认/高；只中 1–2 条中/弱指纹算疑似

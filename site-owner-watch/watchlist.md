# 监听对象

## #1 梗视频站长（身份未公开）
- 来源：需求分析 bot 交接，2026-10-21
- 身份：无公司名、无社媒；推测是国内独立开发者（弱）
- 打法：TikTok「一张照片变成我」类梗一火，几天内注册梗名精确匹配域名，一天内上线；同一套模板复制；一次性点数包约 $9/条；靠梗关键词自然搜索。

### 已确认站点
- https://dimedimebaby.app/ ，2026-10-19 注册，Dime Dime Baby 梗视频，$9.90/$19.90/$29.90
- https://ozilgoalaigenerator.com/ ，2026-10-14 注册，厄齐尔进球梗视频，$8.90/$18.90/$28.90

### 指纹
- 强：文案 "Photo deleted once your video is made"、"Credits back if a render fails"、"which is why the photo box is empty when you come back"；条款写 "independent tool"
- 强：素材路径 r2.<域名>/site/<梗名>/，图标 /brand/mark.svg，接口 /api/meme/generate
- 中：ShipAny 模板（shipanyai/shipany-template-two + better-auth），首页 JS 文件哈希大量相同；部署在 Vercel
- 中：GA ID G-ZFD4YV344W（公开反查暂无结果）
- 弱：Cloudflare 注册 + Cloudflare NS 同一对 martha/rajeev（很多账号共用）
- 弱：邮箱 support@<域名>（Cloudflare 邮件转发）

### 监听手段
1. 网页 / X 搜上面的标志性文案
2. 证书透明日志查新域名：certspotter 可用；crt.sh 有限流
3. 当下 TikTok / X 新梗词 + "ai generator" / "ai video" 的新注册精确匹配域名，打开后对指纹
4. 候选站至少匹配 1 条强指纹才算"确认"，只匹配中/弱的算"疑似"

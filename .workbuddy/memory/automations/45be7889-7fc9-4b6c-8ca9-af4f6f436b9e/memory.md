# 每日内容雷达扫描 — 执行记忆

## 运行约定
- 仓库本地镜像：`D:/WBDHC/2026-11-05-09-10-06/ip-workbench`，远端 origin = https://github.com/jinzhongkan/ip-workbench.git（main）
- 配置事实来源：`radar/radar-config.json`（v2），可读视图 `radar/sources.md`
- 日报输出：`radar/reports/YYYY-MM-DD.md`，按 `radar/report-template.md` 结构
- 栏目配比 40/25/20/15（门店里那点事/算笔账/新规翻译/我的解法）；focus_tags 8 个
- 选题须避让 `content/topics.md` 已有的 #1–#15 与 `ops/calendar.md` 已排期项

## 执行记录

### 2026-11-06（首次运行）
- **网络状况（重要）**：`github.com:443` 不可达（curl 返回 000，git pull/push 均 connect timeout 21098ms），`www.gov.cn` / `mohrss.gov.cn` 正常（200）。→ 本次**未能 pull，也未能 push**；已本地提交 `85d520e`，待网络恢复后执行 `git push origin main`。凭据问题未出现，属纯网络阻断，不要误判为认证失效。
- 产出：`radar/reports/2026-11-06.md`（7 条要闻 + 5 条连续跟踪项 + 5 条选题 + 噪音记录）
- 本条日报核心增量：伪平台用工穿透判例（最锋利素材）、滨海特大虚开劳务发票案 12.8 亿、宝山新职伤生活保障费案、陈斌三大涉税误区、"伪平台用工"三处破绽结构；并补录前次漏扫的国办发〔2026〕29 号（10-23 发布，第 13/14 条）。
- 经验：公众号信源命中率高，检索词加"公众号"后可直接捞到 mp.weixin.qq.com 原文，便于取条文原文；政策官网用 `gov.cn/zhengce/zuixin/` + `mohrss.gov.cn/.../buneiyaowen/` 两个列表页抓取最新，效率高于首页。
- 待办提示：11-08 为征求意见截止日，下一篇日报（11-07/11-08）需重点看是否发布正式稿或延期公告。

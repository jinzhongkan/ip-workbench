# ip-workbench — 个人 IP 内容创作工作台

> 单一事实来源：本仓库。所有档案、选题、草稿、发布记录、雷达日报均存放在此，任何一台电脑通过 WorkBuddy（GitHub 连接器）或 git 都能访问同一份数据。

## 目录结构

```
ip-workbench/
├── me/                   # 记忆与认知区（模型无关）：任何大模型读这里即可恢复对用户的完整认知
│   ├── README.md        # AI 接入说明与维护规则
│   ├── PROFILE.md       # 一页核心档案（30 秒版）
│   ├── CONTEXT.md       # 完整认知：指令/身份/职业/项目/偏好 五分类，条目带日期
│   └── UPDATE-LOG.md    # 认知变更日志
├── profile/              # 我是谁：用户档案 + 平台发布规范（写内容前必读）
│   ├── USER-PROFILE.md   # IP 定位、受众锚点、栏目矩阵、红线清单
│   └── PLATFORM-RULES.md # 视频号 / 小红书 两个平台的发布规范与适配要点
├── radar/                # 内容雷达：每日扫描信源 → 日报
│   ├── sources.md        # 信源清单（政策官网 + 公众号），可随时增删
│   ├── report-template.md# 日报格式模板
│   └── reports/          # 每日雷达报告（YYYY-MM-DD.md）
├── content/              # 内容资产
│   ├── topics.md         # 选题库（待开发 / 已排期 / 已写完）
│   ├── 素材口袋.md       # 随手积累的现场素材、金句、数据
│   ├── drafts/           # 草稿（一个选题一个 md）
│   └── published/        # 已发布归档
│       ├── shipinhao/    # 视频号（发布记录 + 口播稿）
│       └── xiaohongshu/  # 小红书（发布记录 + 图文笔记）
└── ops/
    └── calendar.md       # 双平台发布日历
```

## 多电脑使用

**方式 A（推荐，零 git 操作）**：任何一台装了 WorkBuddy 并连接 GitHub 的电脑，直接对仓库说需求，例如：
- "跑一下内容雷达" —— 扫描信源、生成当日日报、提交到 `radar/reports/`
- "看看今天雷达有什么能写的" —— 读取日报并推荐选题
- "把这条选题写成小红书图文 / 视频号口播稿" —— 落到 `content/drafts/`
- "记录发布：小红书发了《xxx》" —— 归档到 `content/published/`

**方式 C（配置界面）**：修改雷达信源与每日内容方向用图形界面——
```bash
python tools/radar_config_app.py   # 然后打开 http://127.0.0.1:8788
```
保存即写入 `radar/radar-config.json`（唯一配置事实来源）并自动提交推送 GitHub，次日 07:30 雷达按新方向扫描。任何一台电脑 clone 仓库后都能同样启动。

**方式 B（本地 git 镜像）**：
```bash
git clone https://github.com/jinzhongkan/ip-workbench.git
# 开始工作前：git pull
# 结束工作后：git add -A && git commit -m "更新" && git push
```

## 每日流程（建议）

0. **早（可选 10 秒）**：打开配置台（`python tools/radar_config_app.py`）改一句"今日焦点"，雷达当天按此调整选题方向。
1. **早**：雷达扫描（自动/手动）→ 读日报，标记可写的选题
2. **碎片时间**：现场素材随手丢进 `content/素材口袋.md`
3. **晚**：从选题库取 1 条写成草稿 → 按日历排期发布 → 发布后归档记录

## 铁律

- 仓库为唯一事实来源：发布过的内容必须归档到 `published/`，否则跨设备后状态不一致。
- 写任何内容前先读 `profile/USER-PROFILE.md`，红线清单不许越。
- `me/` 是用户认知的单一事实来源：对话中获得新的用户认知时，更新 `me/` 并在 `UPDATE-LOG.md` 记录。

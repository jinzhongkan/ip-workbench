# 多设备接入指南（v1 / 2026-11-05）

> 三种方式按场景选，可组合。数据永远在 GitHub 仓库（jinzhongkan/ip-workbench），不在任何单一设备上。

## 方式 A：云端版界面（零安装，适合手机/临时用/任何电脑）

1. 浏览器打开：https://ip-workbench-71987.app.workbuddy.host/?sharecode=2XEOFRFLNG
2. 首次在该设备使用：按页面指引创建 GitHub Fine-grained PAT（只授权 ip-workbench、Contents 读写），粘贴进登录页。
3. 能做：改雷达配置、读/写日报、编辑仓库任何文件（选题库、日历、素材口袋）。
4. 每台设备只需粘贴一次令牌（存浏览器 localStorage）。

## 方式 B：WorkBuddy 对话（适合日常 AI 干活：写文案、跑雷达、分析）

1. 新电脑安装 WorkBuddy 客户端，登录同一账号。
2. 在连接器里启用 GitHub 连接器（可读仓库）。
3. 新对话开场白（复制这段）：

   > 先读取 GitHub 仓库 jinzhongkan/ip-workbench 的 me/ 目录，把它作为我的长期认知；
   > 再读 profile/USER-PROFILE.md 和 profile/PLATFORM-RULES.md 作为内容创作规范。
   > 之后我说"跑一下内容雷达"时：git pull 仓库最新 → 按 radar/radar-config.json 配置扫描信源 →
   > 生成 radar/reports/当日.md → git commit + push → 给我摘要。

4. 注意：新电脑要向仓库**写**数据（git push），需完成一次 git 授权——新电脑装 git 后，
   在仓库目录执行一次 `git push`，会弹出浏览器登录 GitHub，之后凭据存入该机凭据管理器。
   （不装 git 时 AI 仍可读仓库，只是写不了。）

## 方式 C：完整本地镜像（适合主力开发/离线）

```bash
git clone https://github.com/jinzhongkan/ip-workbench.git
cd ip-workbench
python tools/radar_config_app.py   # 本地雷达配置台 http://127.0.0.1:8788
# 开始工作前 git pull，结束工作后 git add -A && git commit -m "更新" && git push
```

## 铁律（所有设备一致）

- 发布过的内容必须归档到 `content/published/`，否则跨设备状态不一致。
- 修改雷达配置以 `radar/radar-config.json` 为准（sources.md 是生成视图，勿手改）。
- 新认知/偏好让 AI 更新 `me/` 并记 `me/UPDATE-LOG.md`。

## 每日自动雷达的归属

- 每日 07:30 的定时自动化**只在创建它的那台电脑上运行**（Windows 工作区）。
- 换主力电脑时，在新电脑的 WorkBuddy 里说："把内容雷达每日自动化建在这台电脑上"，
  按方式 B 引导词执行，自动化会以新电脑为运行机。
- 自动化没跑的那天（如电脑关机），任何设备说"跑一下内容雷达"即可手动补跑。

# -*- coding: utf-8 -*-
"""
内容雷达配置界面（本地 Web App，零依赖，Python 3.8+ 标准库）

用法：python tools/radar_config_app.py
打开：http://127.0.0.1:8788

保存时：写入 radar/radar-config.json + 重新生成 radar/sources.md，并 git 提交推送到 GitHub。
"""
import json
import os
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, "radar", "radar-config.json")
SOURCES_PATH = os.path.join(ROOT, "radar", "sources.md")
REPO_URL = "https://github.com/jinzhongkan/ip-workbench.git"
PORT = 8788


def run_git(args, check=False):
    p = subprocess.run(["git"] + args, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    out = (p.stdout + p.stderr).strip()
    return p.returncode, out


def get_token_url():
    p = subprocess.run(["git", "credential", "fill"], cwd=ROOT,
                       input="protocol=https\nhost=github.com\n\n",
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    user = pwd = ""
    for line in p.stdout.splitlines():
        if line.startswith("username="):
            user = line.split("=", 1)[1]
        if line.startswith("password="):
            pwd = line.split("=", 1)[1]
    if not pwd:
        return None
    host = REPO_URL.replace("https://", "")
    return f"https://{user}:{pwd}@{host}"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def render_sources_md(cfg):
    gov_rows = "\n".join(f"| {s['name']} | {s['url']} | {s['note']} |" for s in cfg["gov_sites"])
    wx_rows = "\n".join(f"| {a['name']} | {a['type']} | {a['reason']} |" for a in cfg["weixin_accounts"])
    kw_lines = "\n".join(f"{i}. `{k}`" for i, k in enumerate(cfg["search_keywords"], 1))
    tags = "、".join(cfg["focus_tags"])
    w = cfg["direction_weights"]
    weights = " / ".join(f"{k} {v}%" for k, v in w.items())
    focus = cfg["daily_focus"].get("note", "").strip() or "（未设置）"
    topics = "\n".join(f"- {t}" for t in cfg["daily_focus"].get("priority_topics", [])) or "- （无）"
    return f"""# 内容雷达信源清单（由 radar-config.json 生成，请勿手改；界面修改：python tools/radar_config_app.py）

> 更新时间：{cfg["updated"]} ｜ 唯一配置事实来源：`radar/radar-config.json`

## 今日内容方向（雷达优先匹配）

- **今日焦点**：{focus}
- **优先选题方向**：
{topics}
- **栏目配比**：{weights}
- **重点关注标签**：{tags}
- **筛选灵敏度**：{cfg["scan"]["sensitivity"]}（{cfg["scan"]["sensitivity_desc"]}）

## 一、政策官网（必扫）

| 信源 | URL | 关注点 |
|---|---|---|
{gov_rows}

## 二、公众号（检索方式覆盖，查询词必须含"公众号"）

| 公众号 | 类型 | 关注理由 |
|---|---|---|
{wx_rows}

## 三、检索关键词组（每日固定查询）

{kw_lines}

## 筛选标准（命中什么才进日报）

- 与**新就业形态/灵活用工/门店用工**监管直接相关的新文件、新判例、新数据 → 必进
- 连锁业态的用工痛点事件（闭店、被仲裁、被罚）→ 必进
- 一般性 HR 干货（与零工/连锁无关）→ 不进（loose 模式除外）
- 每条记录：来源 / 日期 / 一句话事实 / 与 IP 定位的关联 / 可否转化为选题（哪个栏目）
- 日报"本周可写选题"必须优先贴合上方"今日内容方向"
"""


def save_config(cfg, push=True):
    cfg["updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    with open(SOURCES_PATH, "w", encoding="utf-8") as f:
        f.write(render_sources_md(cfg))
    msgs = ["已写入 radar/radar-config.json 和 radar/sources.md"]
    if push:
        url = get_token_url()
        if url:
            run_git(["fetch", url, "main"])
            run_git(["rebase", "FETCH_HEAD"])
            run_git(["add", "radar/radar-config.json", "radar/sources.md"])
            rc, out = run_git(["commit", "-m", f"更新内容雷达配置（界面，{cfg['updated']}）"])
            if rc != 0 and "nothing to commit" in out:
                msgs.append("git：无变化，跳过提交")
            else:
                rc, out = run_git(["push", url, "main:main"])
                safe = out.replace(url, REPO_URL)
                msgs.append("已推送到 GitHub" if rc == 0 else f"推送失败：{safe}")
        else:
            msgs.append("未找到 GitHub 凭据，仅本地保存（稍后手动 git push）")
    return "\n".join(msgs)


HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>内容雷达 · 配置台</title>
<style>
  :root { --bg:#f7f8fa; --card:#fff; --ink:#1f2329; --sub:#646a73; --line:#e5e7eb;
          --pri:#2563eb; --pri-bg:#eff6ff; --ok:#16a34a; --err:#dc2626; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink);
         font-family:"Microsoft YaHei","PingFang SC",system-ui,sans-serif; }
  .wrap { max-width:860px; margin:0 auto; padding:28px 20px 120px; }
  header h1 { font-size:22px; margin:0 0 4px; }
  header p { color:var(--sub); font-size:13px; margin:0 0 20px; }
  .card { background:var(--card); border:1px solid var(--line); border-radius:12px;
          padding:18px 20px; margin-bottom:16px; }
  .card h2 { font-size:15px; margin:0 0 4px; }
  .card .hint { font-size:12px; color:var(--sub); margin:0 0 12px; }
  textarea { width:100%; min-height:64px; border:1px solid var(--line); border-radius:8px;
             padding:10px 12px; font-size:14px; font-family:inherit; resize:vertical; }
  input[type=text] { border:1px solid var(--line); border-radius:8px; padding:8px 10px;
             font-size:13px; font-family:inherit; width:100%; }
  .w-row { display:flex; align-items:center; gap:12px; margin:8px 0; }
  .w-row label { width:110px; font-size:14px; }
  .w-row input { width:70px; text-align:center; border:1px solid var(--line);
                 border-radius:8px; padding:6px; font-size:14px; }
  .w-row .bar { flex:1; height:8px; background:#eef1f5; border-radius:4px; overflow:hidden; }
  .w-row .bar i { display:block; height:100%; background:var(--pri); }
  #sum { font-size:13px; color:var(--sub); }
  #sum.bad { color:var(--err); font-weight:600; }
  .chips { display:flex; flex-wrap:wrap; gap:8px; }
  .chip { border:1px solid var(--line); border-radius:999px; padding:5px 14px; font-size:13px;
          cursor:pointer; background:#fff; color:var(--sub); user-select:none; }
  .chip.on { background:var(--pri-bg); border-color:var(--pri); color:var(--pri); font-weight:600; }
  .addrow { display:flex; gap:8px; margin-top:10px; }
  table { width:100%; border-collapse:collapse; font-size:13px; }
  th { text-align:left; color:var(--sub); font-weight:500; padding:6px 8px;
       border-bottom:1px solid var(--line); font-size:12px; }
  td { padding:6px 8px; border-bottom:1px solid #f0f1f4; }
  td input { border:1px solid transparent; border-radius:6px; padding:5px 7px; width:100%;
             font-size:13px; background:transparent; }
  td input:focus { border-color:var(--line); background:#fff; outline:none; }
  .del { color:#b0b5bd; cursor:pointer; border:none; background:none; font-size:15px; }
  .del:hover { color:var(--err); }
  .btn { border:none; border-radius:8px; padding:9px 18px; font-size:14px; cursor:pointer;
         background:var(--pri); color:#fff; }
  .btn.sec { background:#fff; color:var(--ink); border:1px solid var(--line); }
  .btn:disabled { opacity:.5; cursor:default; }
  .radio-row label { display:block; padding:8px 10px; border:1px solid var(--line);
                     border-radius:8px; margin:6px 0; font-size:13px; cursor:pointer; }
  .radio-row input { margin-right:8px; }
  .radio-row .desc { color:var(--sub); font-size:12px; margin-left:22px; display:block; }
  #bar { position:fixed; left:0; right:0; bottom:0; background:#fff; border-top:1px solid var(--line);
         padding:12px 0; }
  #bar .wrap { padding:0 20px; display:flex; align-items:center; gap:12px; }
  #status { font-size:13px; color:var(--sub); white-space:pre-wrap; flex:1; }
  #status.ok { color:var(--ok); } #status.err { color:var(--err); }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>内容雷达 · 配置台</h1>
    <p>改完点底部「保存并同步」→ 写入仓库 → 自动推送 GitHub → 次日 07:30 雷达按新方向扫描。手动触发随时说"跑一下内容雷达"。</p>
  </header>

  <div class="card">
    <h2>今日内容方向</h2>
    <p class="hint">雷达选题建议将优先贴合这里。每天早上花 10 秒改一句，日报就换打法。</p>
    <textarea id="focusNote" placeholder="例：本周主打费率账+36条红线；或：今天多留意劳动争议判例，给视频号找口播素材"></textarea>
    <div id="topicList"></div>
    <div class="addrow">
      <input type="text" id="newTopic" placeholder="加一个优先选题方向，如：职伤保障落地后的门店案例">
      <button class="btn sec" onclick="addTopic()">添加</button>
    </div>
  </div>

  <div class="card">
    <h2>内容方向权重（栏目配比）</h2>
    <p class="hint">雷达推导"本周可写选题"时按此配比分配建议数量。</p>
    <div id="weights"></div>
    <div id="sum"></div>
  </div>

  <div class="card">
    <h2>重点关注标签</h2>
    <p class="hint">命中的信息按这些标签归类；可多选、可自定义。</p>
    <div class="chips" id="chips"></div>
    <div class="addrow">
      <input type="text" id="newTag" placeholder="自定义标签，如：AI用工">
      <button class="btn sec" onclick="addTag()">添加标签</button>
    </div>
  </div>

  <div class="card">
    <h2>政策官网（每日必扫）</h2>
    <table id="govTable"><thead><tr><th style="width:22%">名称</th><th style="width:34%">URL</th><th>关注点</th><th style="width:30px"></th></tr></thead><tbody></tbody></table>
    <div class="addrow"><button class="btn sec" onclick="addRow('gov')">＋ 加一行</button></div>
  </div>

  <div class="card">
    <h2>公众号清单</h2>
    <table id="wxTable"><thead><tr><th style="width:24%">公众号</th><th style="width:20%">类型</th><th>关注理由</th><th style="width:30px"></th></tr></thead><tbody></tbody></table>
    <div class="addrow"><button class="btn sec" onclick="addRow('wx')">＋ 加一行</button></div>
  </div>

  <div class="card">
    <h2>检索关键词组</h2>
    <p class="hint">每日固定执行的检索词，一行一条。</p>
    <div id="kwList"></div>
    <div class="addrow">
      <input type="text" id="newKw" placeholder="新检索词，如：灵活用工 社保 新规">
      <button class="btn sec" onclick="addKw()">添加</button>
    </div>
  </div>

  <div class="card">
    <h2>筛选灵敏度</h2>
    <div class="radio-row" id="sens">
      <label><input type="radio" name="sens" value="strict">严格<span class="desc">只收与新就业形态/灵活用工/门店用工直接相关的内容</span></label>
      <label><input type="radio" name="sens" value="normal">标准<span class="desc">严格 + 连锁业态用工动态</span></label>
      <label><input type="radio" name="sens" value="loose">宽松<span class="desc">标准 + 一般 HR 干货也参考</span></label>
    </div>
  </div>
</div>

<div id="bar"><div class="wrap">
  <span id="status">就绪</span>
  <button class="btn sec" onclick="location.reload()">放弃修改</button>
  <button class="btn" id="saveBtn" onclick="save()">保存并同步到 GitHub</button>
</div></div>

<script>
let CFG = null;
const ALL_TAGS = ["费率账","政策红线","C端自由","判例拆解","招聘成本","业态案例","职伤保障","代扣新政","多雇主生态","系统留痕","门店排班","社保新规","AI用工"];

function setStatus(msg, cls){ const s=document.getElementById("status"); s.textContent=msg; s.className=cls||""; }

async function boot(){
  const r = await fetch("/api/config"); CFG = await r.json();
  document.getElementById("focusNote").value = CFG.daily_focus.note || "";
  renderTopics(); renderWeights(); renderChips(); renderGov(); renderWx(); renderKw();
  document.querySelector(`#sens input[value="${CFG.scan.sensitivity}"]`).checked = true;
  setStatus("已载入配置（最后更新 " + CFG.updated + "）");
}

function renderTopics(){
  const box = document.getElementById("topicList"); box.innerHTML = "";
  (CFG.daily_focus.priority_topics||[]).forEach((t,i)=>{
    const d=document.createElement("div"); d.className="w-row";
    d.innerHTML = `<input type="text" value="${esc(t)}" oninput="CFG.daily_focus.priority_topics[${i}]=this.value">
      <button class="del" onclick="CFG.daily_focus.priority_topics.splice(${i},1);renderTopics()">✕</button>`;
    box.appendChild(d);
  });
}
function addTopic(){ const v=document.getElementById("newTopic").value.trim(); if(!v) return;
  CFG.daily_focus.priority_topics.push(v); document.getElementById("newTopic").value=""; renderTopics(); }

function renderWeights(){
  const box = document.getElementById("weights"); box.innerHTML = "";
  for(const k in CFG.direction_weights){
    const d=document.createElement("div"); d.className="w-row";
    d.innerHTML = `<label>${k}</label><input type="text" value="${CFG.direction_weights[k]}"
      oninput="CFG.direction_weights['${k}']=parseInt(this.value)||0;updateBars()">
      <div class="bar"><i style="width:${CFG.direction_weights[k]}%"></i></div><span class="pct">${CFG.direction_weights[k]}%</span>`;
    box.appendChild(d);
  }
  updateBars();
}
function updateBars(){
  let sum=0;
  document.querySelectorAll("#weights .w-row").forEach((row,i)=>{
    const v = parseInt(row.querySelector("input").value)||0; sum+=v;
    row.querySelector(".bar i").style.width = Math.min(v,100)+"%";
    row.querySelector(".pct").textContent = v+"%";
  });
  const el=document.getElementById("sum");
  el.textContent = "合计 " + sum + "%" + (sum!==100 ? "（建议凑整 100%）" : "");
  el.className = sum===100 ? "" : "bad";
}

function renderChips(){
  const box=document.getElementById("chips"); box.innerHTML="";
  const all=[...new Set([...ALL_TAGS, ...CFG.focus_tags])];
  all.forEach(t=>{
    const c=document.createElement("span"); c.className="chip"+(CFG.focus_tags.includes(t)?" on":"");
    c.textContent=t;
    c.onclick=()=>{ const i=CFG.focus_tags.indexOf(t);
      i>=0?CFG.focus_tags.splice(i,1):CFG.focus_tags.push(t); renderChips(); };
    box.appendChild(c);
  });
}
function addTag(){ const v=document.getElementById("newTag").value.trim(); if(!v) return;
  if(!CFG.focus_tags.includes(v)) CFG.focus_tags.push(v);
  document.getElementById("newTag").value=""; renderChips(); }

function esc(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"/g,"&quot;"); }

function renderTable(tbodyId, rows, fields){
  const tb=document.querySelector(tbodyId+" tbody"); tb.innerHTML="";
  rows.forEach((r,i)=>{
    const tr=document.createElement("tr");
    tr.innerHTML = fields.map(f=>`<td><input value="${esc(r[f])}" oninput="rowEdit(${tbodyId},${i},'${f}',this.value)"></td>`).join("")
      + `<td><button class="del" onclick="rowDel(${tbodyId},${i})">✕</button></td>`;
    tb.appendChild(tr);
  });
}
function renderGov(){ renderTable("#govTable", CFG.gov_sites, ["name","url","note"]); }
function renderWx(){ renderTable("#wxTable", CFG.weixin_accounts, ["name","type","reason"]); }
function rowEdit(tbody,i,f,v){
  const rows = tbody==="#govTable"?CFG.gov_sites:CFG.weixin_accounts; rows[i][f]=v; }
function rowDel(tbody,i){
  const rows = tbody==="#govTable"?CFG.gov_sites:CFG.weixin_accounts; rows.splice(i,1);
  tbody==="#govTable"?renderGov():renderWx(); }
function addRow(kind){
  if(kind==="gov"){ CFG.gov_sites.push({name:"",url:"",note:""}); renderGov(); }
  else { CFG.weixin_accounts.push({name:"",type:"",reason:""}); renderWx(); } }

function renderKw(){
  const box=document.getElementById("kwList"); box.innerHTML="";
  CFG.search_keywords.forEach((k,i)=>{
    const d=document.createElement("div"); d.className="w-row";
    d.innerHTML=`<input type="text" value="${esc(k)}" oninput="CFG.search_keywords[${i}]=this.value">
      <button class="del" onclick="CFG.search_keywords.splice(${i},1);renderKw()">✕</button>`;
    box.appendChild(d);
  });
}
function addKw(){ const v=document.getElementById("newKw").value.trim(); if(!v) return;
  CFG.search_keywords.push(v); document.getElementById("newKw").value=""; renderKw(); }

async function save(){
  const btn=document.getElementById("saveBtn"); btn.disabled=true;
  setStatus("正在保存并推送到 GitHub…");
  CFG.daily_focus.note = document.getElementById("focusNote").value;
  CFG.scan.sensitivity = document.querySelector('#sens input:checked').value;
  CFG.gov_sites = CFG.gov_sites.filter(r=>r.name&&r.url);
  CFG.weixin_accounts = CFG.weixin_accounts.filter(r=>r.name);
  CFG.search_keywords = CFG.search_keywords.filter(k=>k.trim());
  try{
    const r = await fetch("/api/save",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(CFG)});
    const j = await r.json();
    setStatus(j.message, r.ok?"ok":"err");
  }catch(e){ setStatus("保存失败："+e, "err"); }
  btn.disabled=false;
}
boot();
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", f"{ctype}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            self._send(200, HTML, "text/html")
        elif path == "/api/config":
            self._send(200, json.dumps(load_config(), ensure_ascii=False))
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if urlparse(self.path).path != "/api/save":
            self._send(404, json.dumps({"error": "not found"}))
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            cfg = json.loads(self.rfile.read(length).decode("utf-8"))
            for key in ("daily_focus", "direction_weights", "focus_tags", "scan",
                        "gov_sites", "weixin_accounts", "search_keywords"):
                assert key in cfg
            msg = save_config(cfg)
            self._send(200, json.dumps({"message": "✔ 保存成功\n" + msg}, ensure_ascii=False))
        except Exception as e:
            self._send(500, json.dumps({"message": f"保存失败：{e}"}, ensure_ascii=False))


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"内容雷达配置台已启动： http://127.0.0.1:{PORT}")
    threading.Timer(1.0, lambda: webbrowser.open(f"http://127.0.0.1:{PORT}")).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止。")

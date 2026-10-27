# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-10-04-22-46-18/build_reader.py')
# -*- coding: utf-8 -*-
fixture_value('texts.93c060f9_1')
import csv, json, base64, os, re, html
from collections import Counter, defaultdict

SRC = session_path('input_2')
OUT = os.path.join(SRC, "skill-review-reader.html")


def load(name):
    with open(os.path.join(SRC, name), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


# ---------- 读取数据 ----------
skills = load("global-skills.csv")
hosts = load("host-roots.csv")
hostspec = load("host-specific-directories.csv")
nested = load("nested-skills.csv")
plugins = load("session-plugin-skills.csv")
codexsys = load("codex-system-skills.csv")
cands = load("source-candidates.csv")
staged = load("staged-file-diff.csv")

with open(os.path.join(SRC, "audit-report.md"), encoding="utf-8") as f:
    report_md = f.read()

# ---------- Markdown -> HTML（够用即可） ----------
def md_inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    return t


def md_to_html(md):
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        # table
        if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:\-|]+\|$", lines[i + 1]):
            head = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            body = []
            while i < len(lines) and lines[i].startswith("|"):
                body.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            th = "".join(f"<th>{md_inline(c)}</th>" for c in head)
            rows = []
            for r in body:
                rows.append("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>")
            out.append(f'<div class="tw"><table><thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            lv = len(m.group(1))
            out.append(f"<h{lv}>{md_inline(m.group(2))}</h{lv}>")
            i += 1
            continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", ln):
            ordered = bool(re.match(r"^\s*\d+\.\s+", ln))
            items = []
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                items.append(re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i]))
                i += 1
            tag = "ol" if ordered else "ul"
            body = "".join(f"<li>{md_inline(x)}</li>" for x in items)
            out.append(f"<{tag}>{body}</{tag}>")
            continue
        if re.match(r"^\s*---+\s*$", ln):
            out.append("<hr>")
            i += 1
            continue
        if not ln.strip():
            i += 1
            continue
        buf = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("|", "#", "-", "*", ">")) \
                and not re.match(r"^\s*\d+\.\s+", lines[i]) and not re.match(r"^\s*---+\s*$", lines[i]):
            buf.append(lines[i])
            i += 1
        out.append(f"<p>{md_inline(' '.join(x.strip() for x in buf))}</p>")
    return "\n".join(out)


report_html = md_to_html(report_md)

# ---------- 派生统计 ----------
UPDATED = ["aihot", "html-ppt-skill", "guizang-ppt-skill", "humanizer",
           "skill_2053082097175687168", "ui-ux-pro-max", "personal-homepage-skill",
           "react-view-transitions", "ponytail-audit", "ponytail-debt",
           "ponytail-help", "ponytail-review"]
REVIEW = ["qclaw-rules", "skill-assistant-pro__skillhub", "skill_2053083109158420480",
          "ponytail", "brainstorming", "clawdefender-1", "skill_2053081406314844160",
          "video-frames-1.0.0", "kdocs", "kdocs-skill__skillhub", "impeccable", "skill-creator"]

cat_count = Counter(s["category"] for s in skills)
host_count = Counter()
for s in skills:
    for h in [x.strip() for x in s["hosts"].split(",") if x.strip()]:
        host_count[h] += 1
with_url = sum(1 for s in skills if s["sourceUrl"].strip())
# 与报告口径一致：已登记 61；未登记但正文有 GitHub 链接 40；连线索都没有 245
with_cand = sum(1 for c in cands
                if not c["registeredSourceUrl"].strip() and int(c["candidateCount"] or 0) > 0)

# 暂存目录文件统计
staging = []
sdir = os.path.join(SRC, "staging")
if os.path.isdir(sdir):
    for d in sorted(os.listdir(sdir)):
        p = os.path.join(sdir, d)
        n = sum(len(fs) for _, _, fs in os.walk(p))
        size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(p) for f in fs)
        staging.append({"name": d, "files": n, "size": size})

# 截图 base64
shots = []
sdir2 = os.path.join(SRC, "screenshots")
if os.path.isdir(sdir2):
    for f in sorted(os.listdir(sdir2)):
        if f.lower().endswith(".png"):
            with open(os.path.join(sdir2, f), "rb") as fh:
                shots.append({"name": f, "b64": base64.b64encode(fh.read()).decode()})


def human_size(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1024


# 根目录文件清单
DESC = {
    "audit-report.md": fixture_value('texts.93c060f9_3'),
    "global-skills.md": '346 合成示例段落：用于验证文档布局与内容转换流程',
    "global-skills.csv": fixture_value('texts.93c060f9_4'),
    "host-roots.csv": fixture_value('texts.93c060f9_5'),
    "host-specific-directories.csv": fixture_value('texts.93c060f9_6'),
    "nested-skills.csv": '合成示例段落：用于验证文档布局与内容转换流程.md',
    "session-plugin-skills.csv": fixture_value('texts.93c060f9_7'),
    "codex-system-skills.csv": "Codex 内置 .system 技能 5 个",
    "source-candidates.csv": fixture_value('texts.93c060f9_8'),
    "staged-file-diff.csv": fixture_value('texts.93c060f9_9'),
    "skill-review.html": '合成示例段落：用于验证文档布局与内容转换流程',
    "skill-review-reader.html": "本阅读版页面",
}
FOLDER_DESC = {
    "screenshots": '合成示例段落：用于验证文档布局与内容转换流程',
    "staging": '10 合成示例段落：用于验证文档布局与内容转换流程',
}

manifest = []
for name in sorted(os.listdir(SRC)):
    p = os.path.join(SRC, name)
    if os.path.isfile(p):
        manifest.append({"name": name, "size": os.path.getsize(p), "type": "文件",
                         "desc": DESC.get(name, "")})
    else:
        cnt = sum(len(fs) for _, _, fs in os.walk(p))
        size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(p) for f in fs)
        manifest.append({"name": name + "/", "size": size, "type": "目录",
                         "count": cnt, "desc": FOLDER_DESC.get(name, "")})

data = {
    "skills": skills, "hosts": hosts, "hostspec": hostspec, "nested": nested,
    "plugins": plugins, "codexsys": codexsys, "cands": cands, "staged": staged,
    "stats": {
        "skills": len(skills), "hostRoots": len(hosts), "hostspec": len(hostspec),
        "nested": len(nested), "plugins": len(plugins), "codexsys": len(codexsys),
        "staged": len(staged), "withUrl": with_url, "withCand": with_cand,
        "noHint": len(skills) - with_url - with_cand,
        "catCount": len(cat_count), "hostCount": len(host_count),
        "shots": len(shots), "stagingDirs": len(staging),
    },
    "cats": cat_count.most_common(),
    "hostUse": host_count.most_common(),
    "updated": UPDATED, "review": REVIEW,
    "staging": staging, "manifest": manifest,
    "shotsData": shots,
}

DATA_JSON = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

TEMPLATE = fixture_value('texts.93c060f9_2')

html_out = TEMPLATE.replace("__DATA__", DATA_JSON)
# 报告正文直接内嵌，避免 file:// 下 fetch 被 CORS 拦掉
REPORT_BLOCK = '<script id="reportRaw" type="text/plain">' + report_md.replace("</script", "<\\/script") + "</script>"
html_out = html_out.replace('<script id="payload"', REPORT_BLOCK + '\n<script id="payload"')
html_out = html_out.replace(
    """fetch('audit-report.md').then(r=>r.ok?r.text():null).then(t=>{ if(t) $('#reportBody').innerHTML=mdInline(t); })
 .catch(()=>{});""",
    "(function(){const t=document.getElementById('reportRaw');if(t)$('#reportBody').innerHTML=renderMd(t.textContent);})();")
html_out = html_out.replace(
    "function mdInline(t){ return esc(t)",
    "function renderMd(t){\n  const L=t.replace(/\\r/g,'').split('\\n'); const O=[]; let i=0;\n"
    "  while(i<L.length){ const ln=L[i];\n"
    "    if(ln.startsWith('|') && i+1<L.length && /^\\|[\\s:\\-|]+\\|$/.test(L[i+1])){\n"
    "      const head=ln.trim().replace(/^\\||\\|$/g,'').split('|').map(s=>s.trim()); i+=2; const body=[];\n"
    "      while(i<L.length && L[i].startsWith('|')){ body.push(L[i].trim().replace(/^\\||\\|$/g,'').split('|').map(s=>s.trim())); i++; }\n"
    "      O.push('<div class=\"tw\"><table><thead><tr>'+head.map(h=>'<th>'+mdInline(h)+'</th>').join('')+'</tr></thead><tbody>'\n"
    "        + body.map(r=>'<tr>'+r.map(c=>'<td>'+mdInline(c)+'</td>').join('')+'</tr>').join('') + '</tbody></table></div>'); continue; }\n"
    "    let m=ln.match(/^(#{1,4})\\s+(.*)$/);\n"
    "    if(m){ O.push('<h'+m[1].length+'>'+mdInline(m[2])+'</h'+m[1].length+'>'); i++; continue; }\n"
    "    if(/^\\s*([-*]|\\d+\\.)\\s+/.test(ln)){ const ord=/^\\s*\\d+\\.\\s+/.test(ln); const it=[];\n"
    "      while(i<L.length && /^\\s*([-*]|\\d+\\.)\\s+/.test(L[i])){ it.push(L[i].replace(/^\\s*([-*]|\\d+\\.)\\s+/,'')); i++; }\n"
    "      const tag=ord?'ol':'ul'; O.push('<'+tag+'>'+it.map(x=>'<li>'+mdInline(x)+'</li>').join('')+'</'+tag+'>'); continue; }\n"
    "    if(/^\\s*---+\\s*$/.test(ln)){ O.push('<hr>'); i++; continue; }\n"
    "    if(!ln.trim()){ i++; continue; }\n"
    "    const buf=[ln]; i++;\n"
    "    while(i<L.length && L[i].trim() && !L[i].startsWith('|') && !/^#{1,4}\\s/.test(L[i]) && !/^\\s*([-*]|\\d+\\.)\\s+/.test(L[i]) && !/^\\s*---+\\s*$/.test(L[i])){ buf.push(L[i]); i++; }\n"
    "    O.push('<p>'+mdInline(buf.map(s=>s.trim()).join(' '))+'</p>'); }\n"
    "  return O.join('\\n'); }\n"
    "function mdInline(t){ return esc(t)")

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html_out)

print("written:", OUT, os.path.getsize(OUT), "bytes")
print("shots:", len(shots), "staging dirs:", len(staging), "manifest:", len(manifest))

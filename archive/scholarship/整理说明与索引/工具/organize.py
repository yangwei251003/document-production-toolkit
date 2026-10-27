# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('scholarship/整理说明与索引/工具/organize.py')
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import csv, json, hashlib, zipfile, html
from collections import Counter
from urllib.parse import quote

root=workspace_root()
out=root/'整理说明与索引'
rows=json.loads((out/'原始清单.json').read_text(encoding='utf-8'))
with (out/'工具/annotations.tsv').open(encoding='utf-8',newline='') as f:
    annotations={x['id']:x for x in csv.DictReader(f,delimiter='\t')}
assert len(annotations)==len(rows)==71
manual={'H003','H023','H041','H044'}
for r in rows:
    r.update(annotations[r['id']])
    p=root/r['old']
    assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
    r['corrected']=r['id'] in manual or r['exif_orientation']!=1
    suffix='.png' if r['corrected'] else p.suffix.lower()
    r['new']=(Path(r['old']).parent/r['category']/f"{r['id']}_{r['date']}_{r['title']}{suffix}").as_posix()
    assert not (root/r['new']).exists()
assert len({r['new'] for r in rows})==71
(out/'重命名计划.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
backup=root/'原始照片备份_整理前.zip'
assert not backup.exists()
with zipfile.ZipFile(backup,'x',compression=zipfile.ZIP_STORED) as z:
    for r in rows: z.write(root/r['old'],r['old'].replace('\\','/'))
with zipfile.ZipFile(backup) as z:
    assert z.testzip() is None
    for r in rows: assert hashlib.sha256(z.read(r['old'].replace('\\','/'))).hexdigest()==r['sha256']
for r in rows:
    src=root/r['old']; dest=root/r['new']; dest.parent.mkdir(exist_ok=True)
    if r['corrected']:
        with Image.open(src) as raw:
            im=ImageOps.exif_transpose(raw)
            if r['id'] in manual: im=im.transpose(Image.Transpose.ROTATE_90)
            im.save(dest,format='PNG')
            with Image.open(dest) as check:
                assert check.size==im.size and check.tobytes()==im.tobytes()
        src.unlink()
    else: src.rename(dest)
    with Image.open(dest) as im:
        im.load(); r['final_width'],r['final_height']=im.size
        assert im.getexif().get(274,1)==1
    r['final_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
    if not r['corrected']: assert r['final_sha256']==r['sha256']
(out/'素材索引.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
fields={'id':'编号','category':'分类','date':'图载时间或待补','title':'内容名称','notes':'理解与使用提示','new':'整理后路径','old':'原始路径','final_width':'宽度','final_height':'高度','corrected':'方向已固化或旋转','sha256':'原文件SHA256','final_sha256':'整理后SHA256'}
with (out/'素材索引与重命名对照.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f); w.writerow(fields.values())
    for r in rows: w.writerow([r[k] for k in fields])
thumbs=out/'缩略图'; thumbs.mkdir(exist_ok=True)
cards=[]
for r in rows:
    with Image.open(root/r['new']) as im:
        im=im.convert('RGB'); im.thumbnail((640,440)); im.save(thumbs/f"{r['id']}.jpg",quality=86)
    url='../'+quote(r['new']); title=html.escape(r['id']+' '+r['title'])
    search=html.escape(' '.join(str(r[k]) for k in ['id','category','date','title','notes']),quote=True)
    cards.append(f'<article data-search="{search}"><a href="{url}" target="_blank"><img loading="lazy" src="缩略图/{r["id"]}.jpg" alt="{title}"></a><div><small>{html.escape(r["category"])} · {html.escape(r["date"])}</small><h2>{title}</h2><p>{html.escape(r["notes"])}</p><a href="{url}" target="_blank">打开原尺寸素材 ↗</a></div></article>')
page='<!doctype html><html lang="zh-CN"><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>国家奖学金答辩素材库</title><style>body{margin:0;background:#f4f3ef;color:#203332;font:16px/1.65 \'Microsoft YaHei\',sans-serif}header{padding:40px 5%;background:#173c37;color:white}h1{font-size:32px;margin:0}header p{color:#d7e2dc}input{box-sizing:border-box;width:100%;max-width:720px;padding:14px;border:0;border-radius:5px;font:inherit}main{padding:30px 5%;display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:22px}article{background:white;border-radius:8px;overflow:hidden;border:1px solid #ddd}article img{width:100%;height:250px;object-fit:contain;background:#eae9e4}article div{padding:20px}h2{font-size:18px;line-height:1.5}small{color:#626d65}a{color:#176a58}p{font-size:14px}#count{margin-left:16px}article[hidden]{display:none}</style><header><h1>合成示例内容：通过项目实践展示文档制作与检查流程</h1><p>71合成示例内容：通过项目实践展示文档制作与检查流程</p><input id="q" type="search" placeholder="合成示例内容：通过项目实践展示文档制作与检查流程……"><span id="count">71 / 71</span></header><main>'+''.join(cards)+'''</main><script>document.getElementById('q').addEventListener('input',e=>{let n=0;const q=e.target.value.trim().toLowerCase();document.querySelectorAll('article').forEach(a=>{a.hidden=!a.dataset.search.toLowerCase().includes(q);if(!a.hidden)n++});document.getElementById('count').textContent=n+' / 71'})</script></html>'''
(out/'素材总览.html').write_text(page,encoding='utf-8')
font=ImageFont.truetype(source_path('msyh.ttc'),21)
for prefix in ['H','P']:
    group=[r for r in rows if r['id'].startswith(prefix)]
    for start in range(0,len(group),8):
        subset=group[start:start+8]
        sheet=Image.new('RGB',(1600,550*((len(subset)+1)//2)),'#eeeeee'); d=ImageDraw.Draw(sheet)
        for k,r in enumerate(subset):
            with Image.open(root/r['new']) as im:
                im=im.convert('RGB'); im.thumbnail((770,460))
                x=k%2*800;y=k//2*550
                sheet.paste(im,(x+(800-im.width)//2,y+65+(460-im.height)//2))
                label=r['id']+' '+r['title'];d.text((x+12,y+5),label[:33],fill='black',font=font)
                if len(label)>33:d.text((x+12,y+30),label[33:66],fill='black',font=font)
        sheet.save(out/'预览'/f'{prefix}_{start//8+1:02}.jpg',quality=90)
counts=Counter(r['category'] for r in rows)
report={'total':len(rows),'H':sum(r['id'].startswith('H') for r in rows),'P':sum(r['id'].startswith('P') for r in rows),'direction_corrected':sum(r['corrected'] for r in rows),'manual_90_degree':len(manual),'exif_baked':sum(r['exif_orientation']!=1 for r in rows),'backup_hashes_verified':len(rows),'output_files_verified':len(rows),'categories':dict(counts)}
(out/'整理验证结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='categories'}))

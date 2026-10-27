# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('scholarship/整理说明与索引/工具/organize_round3.py')
from pathlib import Path
from PIL import Image,ImageOps
import json,hashlib,zipfile,csv,html
from urllib.parse import quote
root=workspace_root();out=root/'整理说明与索引'
rows=json.loads((out/'素材索引.json').read_text(encoding='utf-8'))
specs=[
('1c6f9a4225f932bbee8194069f78b761.png','03_志愿劳动与社会实践','三下乡电学实验课_互动演示','合成示例内容：通过项目实践展示文档制作与检查流程'),
('361289e8ec483439a59b15ca5d66aeba.jpg','07_体育运动','操场拔河活动_团队协作现场','合成示例内容：通过项目实践展示文档制作与检查流程'),
('4d8b6abb90b2b10c9d4237b85350102d.png','08_美育作品与表达','荔枝树下卡通人物_数字创作画面','合成示例内容：通过项目实践展示文档制作与检查流程'),
('5f60a495212b8fd9e6223daa3cd9d006.jpg','03_志愿劳动与社会实践','室内清扫_持扫帚清理现场','合成示例内容：通过项目实践展示文档制作与检查流程'),
('9485f2de776da3ac25bc11235bbba084.jpg','08_美育作品与表达','拾光记忆_日常文创用品作品展示截图','合成示例内容：通过项目实践展示文档制作与检查流程'),
('9f9869ada7f4ed98bc5b20eb93262c13.png','03_志愿劳动与社会实践','三下乡科学课堂_灯光实验互动','合成示例内容：通过项目实践展示文档制作与检查流程'),
('ca3c6f864b6b304197134d193e1f0221.png','08_美育作品与表达','红色主题视频_历史场景数字创作画面','合成示例内容：通过项目实践展示文档制作与检查流程'),
('e0c068f9747a8fbef4e950e18f2dc1aa.jpg','03_志愿劳动与社会实践','校园清扫_志愿者协作清理现场','合成示例内容：通过项目实践展示文档制作与检查流程'),
('ef7f3cb657e96bac5d274be357612940.jpg','07_体育运动','羽毛球运动_室内球场现场','合成示例内容：通过项目实践展示文档制作与检查流程'),
('f07f3a6b40952c30128461aa971ad30c.png','08_美育作品与表达','把长征走成今天的路_主题讲述视频截图','合成示例内容：通过项目实践展示文档制作与检查流程')]
new=[]
for i,(old,cat,title,notes) in enumerate(specs,25):
 p=root/old;rid=f'P{i:03}';existing=next((r for r in rows if r['id']==rid),None)
 if existing: continue
 with Image.open(p) as im:
  orientation=im.getexif().get(274,1);w,h=im.size
 suffix='.png' if orientation!=1 else p.suffix.lower()
 dest=Path('项目经历照片')/cat/f'{rid}_日期待补_{title}{suffix}'
 new.append(dict(id=rid,old=old,new=dest.as_posix(),category=cat,title=title,notes=notes,date='日期待补',width=w,height=h,exif_orientation=orientation,corrected=orientation!=1,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
backup=root/'新增照片备份_第三批整理前.zip'
if new:
 with zipfile.ZipFile(backup,'x',zipfile.ZIP_STORED) as z:
  for r in new:z.write(root/r['old'],r['old'])
 with zipfile.ZipFile(backup) as z:
  for r in new:assert hashlib.sha256(z.read(r['old'])).hexdigest()==r['sha256']
 for r in new:
  src=root/r['old'];dst=root/r['new'];dst.parent.mkdir(exist_ok=True)
  assert not dst.exists()
  if r['corrected']:
   with Image.open(src) as im:ImageOps.exif_transpose(im).save(dst)
   src.unlink()
  else:src.rename(dst)
  with Image.open(dst) as im:im.load();r['final_width'],r['final_height']=im.size
  r['final_sha256']=hashlib.sha256(dst.read_bytes()).hexdigest();rows.append(r)
r=next(r for r in rows if r['id']=='H025')
correct='合成示例内容：通过项目实践展示文档制作与检查流程_含24电气工程本科5班'
if r['title']!=correct:
 src=root/r['new'];dst=src.with_name(f'H025_日期待补_{correct}{src.suffix}');assert not dst.exists();src.rename(dst);r['new']=dst.relative_to(root).as_posix();r['title']=correct
r['notes']='合成示例内容：通过项目实践展示文档制作与检查流程'
for r in rows:
 if r['id'] in ['P004','P006','P017','P019','P020']:
  r['notes']=r['notes'].replace('服务人数课时和报道链接待补。','合成示例内容：通过项目实践展示文档制作与检查流程')
 if r['id']=='H015':r['notes']='合成示例内容：通过项目实践展示文档制作与检查流程'
 if r['id']=='P010':r['notes']='合成示例内容：通过项目实践展示文档制作与检查流程/合成示例内容：通过项目实践展示文档制作与检查流程'
 if r['id']=='P023':r['notes']='合成示例内容：通过项目实践展示文档制作与检查流程'
 if r['id']=='P024':r['notes']='合成示例内容：通过项目实践展示文档制作与检查流程'
(out/'素材索引.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
original=json.loads((out/'原始清单.json').read_text(encoding='utf-8'));known={r['id'] for r in original}
original.extend({k:r[k] for k in ['id','old','width','height','exif_orientation','sha256']} for r in new if r['id'] not in known)
(out/'原始清单.json').write_text(json.dumps(original,ensure_ascii=False,indent=2),encoding='utf-8')
fields=['id','category','date','title','notes','new','old','final_width','final_height','corrected','sha256','final_sha256']
with (out/'素材索引与重命名对照.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
cards=[]
for r in rows:
 p=root/r['new'];assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==r['final_sha256']
 with Image.open(p) as im:
  im.load();im=im.convert('RGB');im.thumbnail((640,440));im.save(out/'缩略图'/f"{r['id']}.jpg",quality=88)
 title=html.escape(r['id']+' '+r['title']);note=html.escape(r['notes']);href='../'+quote(r['new'])
 cards.append(f'<article data-search="{title} {note}"><a href="{href}"><img src="缩略图/{r["id"]}.jpg" loading="lazy"></a><h3>{title}</h3><p>{note}</p></article>')
page='''<!doctype html><meta charset="utf-8"><title>国奖素材总览</title><style>body{background:#f5f2eb;font:16px/1.6 'Microsoft YaHei';color:#183e38;margin:40px}input{padding:14px;width:70%;font:inherit}main{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:30px}article{background:white;padding:20px;border-radius:10px}img{width:100%;height:240px;object-fit:contain}p{font-size:13px}article[hidden]{display:none}</style>'''+f'<h1>国家奖学金答辩 · {len(rows)}张素材</h1><p>49合成示例内容：通过项目实践展示文档制作与检查流程</p><input id="q" placeholder="搜索编号、内容、类别"><main>'+''.join(cards)+'''</main><script>q.oninput=()=>document.querySelectorAll('article').forEach(a=>a.hidden=!a.dataset.search.toLowerCase().includes(q.value.toLowerCase()))</script>'''
(out/'素材总览.html').write_text(page,encoding='utf-8')
report={'total':len(rows),'H':49,'P':len(rows)-49,'new_ids':[r['id'] for r in new],'new_backup':str(backup),'new_backup_verified':len(new),'output_hashes_verified':len(rows),'orientation_normalized_new':[r['id'] for r in new if r['corrected']],'H025_corrected':True}
(out/'第三批整理验证.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))

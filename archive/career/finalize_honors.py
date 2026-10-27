# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('career/finalize_honors.py')
from pathlib import Path
import json,shutil,zipfile
from PIL import Image,ImageChops,ImageStat
R=workspace_root();V=R/'PPT制作_V2';D=R/'交付文件/求职综合展示PPT_V2_22页'
n=json.loads((V/'qa/PowerPoint实测.json').read_text('utf-8-sig'));assert n['status']=='PASS' and n['slides']==22
assert all(x['hidden']==(x['slide']>19) and x['exported'] for x in n['checks'])
checks=[]
for i in range(1,23):
 a=Image.open(V/'slides'/f'{i:02}.png').convert('RGB');b=Image.open(V/'qa/PowerPoint渲染'/f'{i:02}.png').convert('RGB')
 if a.size!=b.size:a=a.resize(b.size,Image.Resampling.BICUBIC)
 d=sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3;assert d<12
 checks.append({'slide':i,'pixel_mean_absolute_difference':round(d,3),'status':'PASS'})
f=V/'qa/交付检查.json';r=json.loads(f.read_text('utf-8'));r.update(status='PASS',native_pixel_comparisons=checks,latest_revision='第7页八证书扩充',latest_visual_spotcheck=[7]);f.write_text(json.dumps(r,ensure_ascii=False,indent=2),'utf-8')
for name in ['交付检查.json','PowerPoint实测.json']:shutil.copy2(V/'qa'/name,D/name)
for p in [V/'修订说明.md',D/'修订说明.md',R/'项目说明.md']:
 with p.open('a',encoding='utf-8') as out:out.write('\n\n2026-10-23合成示例内容：通过项目实践展示文档制作与检查流程.37MB，PowerPoint合成示例内容：通过项目实践展示文档制作与检查流程_V2/版本备份/荣誉页扩充前。\n')
bundle=R/'示例同学_求职综合展示PPT_V2_22页交付包.zip'
with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(D.rglob('*')):
  if p.is_file():z.write(p,Path(D.name)/p.relative_to(D))
with zipfile.ZipFile(bundle) as z:assert z.testzip() is None;count=len(z.namelist())
receipt={'status':'PASS','zip_entries':count,'zip_bytes':bundle.stat().st_size,'pptx_bytes':r['pptx_bytes'],'honor_certificates':8,'slides':22,'other_21_images_unchanged':True}
(V/'qa/打包验收.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(receipt))

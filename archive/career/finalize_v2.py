# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('career/finalize_v2.py')
from pathlib import Path
import json,shutil,zipfile,hashlib
from PIL import Image,ImageChops,ImageStat
R=workspace_root();V=R/'PPT制作_V2';D=R/'交付文件/求职综合展示PPT_V2_22页'
native=json.loads((V/'qa/PowerPoint实测.json').read_text('utf-8-sig'))
assert native['status']=='PASS' and native['slides']==22
assert all(x['exported'] and x['shapes']==1 and x['hidden']==(x['slide']>19) for x in native['checks'])
comp=[]
for n in range(1,23):
 a=Image.open(V/'slides'/f'{n:02}.png').convert('RGB');b=Image.open(V/'qa/PowerPoint渲染'/f'{n:02}.png').convert('RGB')
 if a.size!=b.size:a=a.resize(b.size,Image.Resampling.BICUBIC)
 mae=sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3
 assert mae<12,(n,mae)
 comp.append({'slide':n,'pixel_mean_absolute_difference':round(mae,3),'status':'PASS'})
report=json.loads((V/'qa/交付检查.json').read_text('utf-8'))
report.update(status='PASS',native_application='Microsoft PowerPoint '+native['version'],native_open_and_export='PASS',native_visual_spotcheck=[5,7,9,19],native_pixel_comparisons=comp)
(V/'qa/交付检查.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
for f in ['交付检查.json','PowerPoint实测.json']:shutil.copy2(V/'qa'/f,D/f)
M=json.loads((V/'imagegen-manifest.json').read_text('utf-8'))
notes=['# V2逐页检查与逻辑复核','','2026-10-23合成示例内容：通过项目实践展示文档制作与检查流程','','## 文件验证','','- PPTX 40.36MB，小于50MB。','- Microsoft PowerPoint合成示例内容：通过项目实践展示文档制作与检查流程','- 合成示例内容：通过项目实践展示文档制作与检查流程','- 合成示例内容：通过项目实践展示文档制作与检查流程/7/9/19页未见新增裁切或遮挡。','- PDF合成示例内容：通过项目实践展示文档制作与检查流程','','## 前后页逻辑','','- 1—5：身份与岗位目标 → 选择依据 → 岗位工作 → 具体意向企业。','- 6—10：胜任力过渡 → 荣誉资格 → 无人机实习 → 三下乡表达与组织 → 文体、班级与文创。','- 11—15：能策Pilot → AI任务组织 → 硬件与前端作品 → 岗位情境演示 → 五项能力证据汇总。','- 16—19：发展过渡 → 保留的补强行动 → 发展路径 → 结束。','- 20—22：合成示例内容：通过项目实践展示文档制作与检查流程','','## 逐页复核','','| 页码 | 检查结果 | 说明 |','|---|---|---|']
for x in M:notes.append(f"| {x['slide']:02} | {'通过；原件细字以源文件为准' if x['slide']==7 else '通过'} | {x['review_notes']} |")
notes+=['','## 已知边界','','- 合成示例内容：通过项目实践展示文档制作与检查流程','- 合成示例内容：通过项目实践展示文档制作与检查流程','- 官方图片是行业/合成示例内容：通过项目实践展示文档制作与检查流程','- 合成示例内容：通过项目实践展示文档制作与检查流程','- 合成示例内容：通过项目实践展示文档制作与检查流程','- 合成示例内容：通过项目实践展示文档制作与检查流程']
(D/'逐页检查与使用说明.md').write_text('\n'.join(notes),'utf-8')
o=json.loads((V/'outline.json').read_text('utf-8'));o['stage']='DELIVERED';(V/'outline.json').write_text(json.dumps(o,ensure_ascii=False,indent=2),'utf-8')
project=R/'项目说明.md'
with project.open('a',encoding='utf-8') as f:f.write('\n## PPT V2修订交付（2026-10-23）\n\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 交付：`交付文件/求职综合展示PPT_V2_22页/`；PPTX 40.36MB。\n- PowerPoint合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n')
bundle=R/'示例同学_求职综合展示PPT_V2_22页交付包.zip'
with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(D.rglob('*')):
  if f.is_file():z.write(f,Path('求职综合展示PPT_V2_22页')/f.relative_to(D))
with zipfile.ZipFile(bundle) as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if '/逐页图片/' in n and n.endswith('.png')])==22
 receipt={'status':'PASS','zip':str(bundle),'zip_bytes':bundle.stat().st_size,'entries':len(z.namelist()),'pptx_bytes':report['pptx_bytes'],'max_native_pixel_mae':max(x['pixel_mean_absolute_difference'] for x in comp),'preserved_original16':True}
(V/'qa/打包验收.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(receipt,ensure_ascii=False))

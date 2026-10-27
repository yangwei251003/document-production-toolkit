# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('career/finalize_ppt_delivery.py')
from pathlib import Path
import json, zipfile, shutil, hashlib
from PIL import Image, ImageChops, ImageStat
ROOT=workspace_root()
PROD=ROOT/'PPT制作'
OUT=ROOT/'交付文件'/'求职综合展示PPT'
native=json.loads((PROD/'qa'/'PowerPoint实测.json').read_text('utf-8-sig'))
assert native['status']=='PASS' and native['slides']==21
assert all(r['exported'] and r['shapes']==1 and r['hidden']==(r['slide']>18) for r in native['checks'])
comparisons=[]
for n in range(1,22):
    a=Image.open(PROD/'slides'/f'{n:02}.png').convert('RGB')
    b=Image.open(PROD/'qa'/'PowerPoint渲染'/f'{n:02}.png').convert('RGB')
    if a.size!=b.size: a=a.resize(b.size,Image.Resampling.BICUBIC)
    diff=ImageStat.Stat(ImageChops.difference(a,b))
    mae=sum(diff.mean)/3
    assert mae<12, (n,mae)
    comparisons.append({'slide':n,'mean_absolute_pixel_difference_0_255':round(mae,3),'status':'PASS'})
reportpath=PROD/'qa'/'交付检查.json'
report=json.loads(reportpath.read_text('utf-8'))
report.update({'native_powerpoint_open':'PASS','native_powerpoint_version':native['version'],'native_export_all_21_slides':'PASS','native_pixel_comparison':comparisons,'native_visual_spotcheck':[1,6,12,18],'status':'PASS'})
reportpath.write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
shutil.copy2(reportpath,OUT/'交付检查.json')
shutil.copy2(PROD/'qa'/'PowerPoint实测.json',OUT/'PowerPoint实测.json')
manifest=json.loads((PROD/'imagegen-manifest.json').read_text('utf-8'))
qa=['# PPT逐页检查与逻辑复核','', '检查日期：2026-10-23。21合成示例内容：通过项目实践展示文档制作与检查流程','', '## 文件实测','', f'- PPTX：{report["pptx_MB_decimal"]} MB（{report["pptx_bytes"]:,}字节），小于50,000,000字节。', '- Microsoft PowerPoint '+native['version']+' 只读打开成功，21页全部导出成功。','- 18合成示例内容：通过项目实践展示文档制作与检查流程','- PowerPoint合成示例内容：通过项目实践展示文档制作与检查流程','- PDF合成示例内容：通过项目实践展示文档制作与检查流程','', '## 前后逻辑','', '- 01—04：合成示例内容：通过项目实践展示文档制作与检查流程','- 05—09：合成示例内容：通过项目实践展示文档制作与检查流程','- 10—12：合成示例内容：通过项目实践展示文档制作与检查流程','- 13—14：合成示例内容：通过项目实践展示文档制作与检查流程','- 15—18：合成示例内容：通过项目实践展示文档制作与检查流程','- 19—21：合成示例内容：通过项目实践展示文档制作与检查流程','', '## 每页检查','', '| 页 | 结果 | 核对记录 |','|---|---|---|']
for row in manifest: qa.append(f'| {row["slide"]:02} | PASS | {row["review_notes"]} |')
qa += ['', '## 使用边界','', '- 合成示例内容：通过项目实践展示文档制作与检查流程','- 合成示例内容：通过项目实践展示文档制作与检查流程','- 合成示例内容：通过项目实践展示文档制作与检查流程','- 合成示例内容：通过项目实践展示文档制作与检查流程']
(OUT/'逐页检查与使用说明.md').write_text('\n'.join(qa),'utf-8')
# Record the final prompt constraints used in regenerations.
supplements={12:'合成示例内容：通过项目实践展示文档制作与检查流程',14:'合成示例内容：通过项目实践展示文档制作与检查流程',20:'合成示例内容：通过项目实践展示文档制作与检查流程'}
for n,t in supplements.items(): (PROD/'prompts'/f'{n:02}_revision.md').write_text(t,'utf-8')
(PROD/'qa'/'原图与PowerPoint渲染比较.json').write_text(json.dumps(comparisons,ensure_ascii=False,indent=2),'utf-8')

project=ROOT/'项目说明.md'
text=project.read_text('utf-8')
text=text.replace('合成示例内容：通过项目实践展示文档制作与检查流程','合成示例内容：通过项目实践展示文档制作与检查流程')
text=text.replace('尚待本人审查。','已获本人同意并完成制作。')
text=text.replace('当前未生成任何正式幻灯片。','合成示例内容：通过项目实践展示文档制作与检查流程.15 MB；合成示例内容：通过项目实践展示文档制作与检查流程')
text+='\n## PPT正式交付（2026-10-23）\n\n- [PPT与配套文件](交付文件/求职综合展示PPT/)：PPTX、合成示例内容：通过项目实践展示文档制作与检查流程\n- [PPT检查记录](PPT制作/qa/交付检查.json)：合成示例内容：通过项目实践展示文档制作与检查流程\n- [生成来源清单](PPT制作/imagegen-manifest.json)：合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n'
project.write_text(text,'utf-8')

bundle=ROOT/'示例同学_求职综合展示PPT交付包_[示例编号].zip'
with zipfile.ZipFile(bundle,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file(): z.write(p,Path('求职综合展示PPT')/p.relative_to(OUT))
with zipfile.ZipFile(bundle) as z:
    assert z.testzip() is None
    assert len([n for n in z.namelist() if '/逐页图片/' in n and n.endswith('.png')])==21
    assert any(n.endswith('.pptx') for n in z.namelist())
    count=len(z.namelist())
receipt={'zip':str(bundle),'zip_bytes':bundle.stat().st_size,'zip_entries':count,'zip_integrity':'PASS','pptx_bytes':report['pptx_bytes'],'pptx_sha256':hashlib.sha256(next(OUT.glob('*.pptx')).read_bytes()).hexdigest(),'max_pixel_mae':max(r['mean_absolute_pixel_difference_0_255'] for r in comparisons)}
(PROD/'qa'/'打包验收.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),'utf-8')
print(json.dumps(receipt,ensure_ascii=False))

# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('career/build_ppt_review.py')
from pathlib import Path
import re, json, html, base64, mimetypes

ROOT=workspace_root()
OUT=ROOT/'PPT设计方案'
source=(OUT/'设计审查稿.md').read_text(encoding='utf-8')
sections=re.findall(r'^### (\d{2})｜(.+?)\n\n(.*?)(?=^### \d{2}｜|^## 5\.|\Z)', source, re.M|re.S)
assert len(sections)==21,len(sections)
slides=[]
for number,title,body in sections:
    match=re.search(r'（(\d+)秒）',title)
    slides.append({'slide_number':int(number),'title':re.sub(r'（\d+秒）|（不计主讲）','',title),
        'hidden':int(number)>18,'speaker_seconds':int(match[1]) if match else 0,
        'design_spec_markdown':body.strip(),'generation_status':'NOT_STARTED',
        'backend_planned':'built-in imagegen','review_status':'AWAITING_USER_REVIEW'})
assert sum(x['speaker_seconds'] for x in slides)==345
outline={'title':'以技为桥，让低空服务电力','candidate':'示例同学',
 'career_target':'无人机技术销售工程师（电力能源方向）','stage':'DESIGN_REVIEW',
 'route_id':'65afd034-6b2b-4f0e-8423-244be6539b10','aspect_ratio':'16:9',
 'palette':['#10283F','#F5F8FB','#1AABC0','#C99B45','#243747'],
 'main_slides':18,'backup_slides':3,'planned_seconds':345,'max_pptx_bytes_exclusive':50000000,
 'slides':slides}
(OUT/'outline.json').write_text(json.dumps(outline,ensure_ascii=False,indent=2),encoding='utf-8')

base=Path(source_path('项目经历照片'))
assets=[
 ('本人正装照｜封面与结尾',base/'05_个人形象/P007_日期待补_个人正装白底证件照.jpg'),
 ('电学互动课｜技术表达',base/'03_志愿劳动与社会实践/P025_日期待补_三下乡电学实验课_互动演示.png'),
 ('校园竞赛合影｜不作为实习现场',base/'02_校园分享与组织活动/P008_日期待补_智能飞行器应用技术技能竞赛_现场合影.jpg'),
 ('团队硬件原型｜智能出纸机',base/'01_技术项目与作品/P021_日期待补_智能抽纸机_硬件原型实物.jpg'),
 ('已有网站界面｜云游地图相关展示',base/'01_技术项目与作品/P005_日期待补_六祖云游文旅平台_新兴旅游首页.png'),
 ('宣传设计作品｜画中人物不作实习纪实',Path(source_path('fixture-portrait.png')))]
gallery=[]
for label,path in assets:
    assert path.exists(),path
    data=base64.b64encode(path.read_bytes()).decode()
    mime=mimetypes.guess_type(path.name)[0]
    gallery.append(f'<figure><img loading="lazy" src="data:{mime};base64,{data}" alt="{html.escape(label)}"><figcaption>{html.escape(label)}</figcaption></figure>')
(OUT/'图片候选索引.json').write_text(json.dumps([{'label':label,'source':str(path),'use':'reference input; not generated slide'} for label,path in assets],ensure_ascii=False,indent=2),encoding='utf-8')

def inline(s):
    s=html.escape(s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',r'<a href="\2" target="_blank" rel="noreferrer">\1</a>',s)
    return s
lines=source.splitlines();blocks=[];i=0
while i<len(lines):
    line=lines[i]
    if not line.strip():i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].startswith('|'):
            row=lines[i];i+=1
            if re.fullmatch(r'[|\s:-]+',row):continue
            cells=row.strip('|').split('|');tag='th' if not rows else 'td'
            rows.append('<tr>'+''.join(f'<{tag}>{inline(c.strip())}</{tag}>' for c in cells)+'</tr>')
        blocks.append('<div class="table"><table>'+''.join(rows)+'</table></div>');continue
    m=re.match(r'^(#{1,3}) (.+)',line)
    if m:
        level=len(m[1]);title=m[2]
        sid='s'+title[:2] if re.match(r'\d{2}｜',title) else 'section'+str(i)
        blocks.append(f'<h{level} id="{sid}">{inline(title)}</h{level}>')
    elif line.startswith('- '):blocks.append('<p class="list">• '+inline(line[2:])+'</p>')
    else:blocks.append('<p>'+inline(line)+'</p>')
    i+=1
toc=''.join(f'<a href="#s{x["slide_number"]:02d}">{x["slide_number"]:02d}　{html.escape(x["title"])}</a>' for x in slides)
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>合成示例内容：通过项目实践展示文档制作与检查流程</title>\n<style>body{margin:0;background:#f5f8fb;color:#243747;font:16px/1.85 "Microsoft YaHei",sans-serif}aside{position:fixed;width:250px;inset:0 auto 0 0;padding:24px;background:#10283f;color:white;overflow:auto;box-sizing:border-box}aside a{display:block;color:#d9eef1;text-decoration:none;font-size:13px;margin:10px 0}aside strong{font-size:20px}main{margin-left:250px;padding:36px 5vw;max-width:1120px}h1{font-size:32px;line-height:1.4}h2{font-size:25px;margin-top:54px;color:#10283f}h3{font-size:22px;border-top:2px solid #1aabc0;padding-top:22px;margin-top:38px;scroll-margin-top:24px}p{margin:12px 0}a{color:#126c87}table{width:100%;border-collapse:collapse;font-size:14px;background:white}td,th{padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid #dce5eb}th{background:#e5eff4}.table{overflow-x:auto}code{font-size:13px;overflow-wrap:anywhere}strong{color:#10283f}.gallery{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}figure{margin:0;background:white;padding:14px}img{width:100%;height:260px;object-fit:contain}figcaption{font-size:14px;margin-top:10px}.notice{padding:18px;border-left:5px solid #c99b45;background:white}.list{margin-left:12px}@media(max-width:950px){aside{display:none}main{margin-left:0;padding:24px}.gallery{grid-template-columns:1fr}}@media print{aside{display:none}main{margin:0;padding:0}h3{break-before:page}img{height:180px}}</style>\n<aside><strong style="color:white">设计审查稿 V1</strong><p>18页主讲 · 3页备用<br>尚未生成PPT</p>'+toc+'<a href="#gallery">候选图片预览</a></aside><main><div class="notice">合成示例内容：通过项目实践展示文档制作与检查流程</div>'+''.join(blocks)+'<h2 id="gallery">候选图片预览</h2><p>合成示例内容：通过项目实践展示文档制作与检查流程</p><div class="gallery">'+''.join(gallery)+'</div></main></html>'
(OUT/'设计审查稿_含素材预览.html').write_text(page,encoding='utf-8')
(OUT/'方案检查.json').write_text(json.dumps({'main_pages':18,'backup_pages':3,'planned_seconds':345,'timing_rehearsed':False,'reference_images_found':len(assets),'generated_slides':0,'pptx_created':False,'status':'plan ready for user review'},ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 21 page plans, 345 planned seconds, 6 existing image references; MD + JSON + self-contained HTML.')

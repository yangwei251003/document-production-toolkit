# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('scholarship/国家奖学金答辩_修订版/生成与检查记录/render_sources.py')
from pathlib import Path
import json,sys,hashlib
from PIL import Image
from playwright.sync_api import sync_playwright
root=workspace_root()
out=root/'国家奖学金答辩_修订版'
record=out/'生成与检查记录'
assets=json.loads((out/'修改依据/素材路径表.json').read_text(encoding='utf-8'))
n=int(sys.argv[1]);spec=json.loads((record/f'{n:02}_原图嵌入.json').read_text(encoding='utf-8'))
source=record/f'{n:02}_生图原稿.png'
body=f'<div class="stage"><img class="base" src="{source.as_uri()}">'
manifest=[]
for i,a in enumerate(spec):
 if 'text' in a:
  x,y,w,h=a['box'];body+=f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{a.get("background","#f6f3ec")};color:{a.get("color","#123f37")};font:{a.get("font",22)}px SimSun;display:flex;align-items:center;justify-content:center;text-align:center">{a["text"]}</div>';continue
 p=Path(assets.get(a['asset'],str(root/a['asset'])));im=Image.open(p);fw,fh=im.size
 x,y,w,h=a['box'];cx,cy,cw,ch=a.get('crop',[0,0,fw,fh]);aspect='xMidYMid slice' if a.get('fit')=='cover' else 'xMidYMid meet'
 body+=f'<div class="photo" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{a.get("background","#f6f3ec")}"><svg viewBox="{cx} {cy} {cw} {ch}" preserveAspectRatio="{aspect}"><defs><clipPath id="clip{i}"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}"/></clipPath></defs><image href="{p.as_uri()}" width="{fw}" height="{fh}" clip-path="url(#clip{i})"/></svg></div>'
 if a.get('caption'):
  body+=f'<div style="position:absolute;left:{x}px;top:{y+h-38}px;width:{w}px;height:38px;background:linear-gradient(90deg,#123f37ed,#123f3788);color:#fff;font:23px SimSun;line-height:38px;padding-left:13px">{a["caption"]}</div>'
 manifest.append({**a,'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
body+='</div>'
html='<meta charset="utf-8"><style>*{box-sizing:border-box}body{margin:0}.stage{position:relative;width:1672px;height:941px;overflow:hidden}.base{position:absolute;width:100%;height:100%}.photo{position:absolute;overflow:hidden}.photo svg{display:block;width:100%;height:100%;overflow:hidden}</style>'+body
hp=record/f'{n:02}_保真排版.html';hp.write_text(html,encoding='utf-8')
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=source_path('msedge.exe'),headless=True)
 page=b.new_page(viewport={'width':1672,'height':941},device_scale_factor=2)
 page.goto(hp.as_uri());page.wait_for_load_state('networkidle');page.locator('.stage').screenshot(path=str(out/'整页图片'/f'{n:02}.png'));b.close()
(record/f'{n:02}_原图校验.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Page {n}: {len(spec)} original placements rendered')

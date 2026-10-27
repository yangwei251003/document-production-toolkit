# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('scholarship/整理说明与索引/工具/prepare.py')
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import json, hashlib
root=workspace_root()
out=root/'整理说明与索引'
rows=[]
font=ImageFont.truetype(source_path('msyh.ttc'),20)
for folder,prefix in [('荣誉奖状证书','H'),('项目经历照片','P')]:
    files=sorted((root/folder).iterdir(),key=lambda p:p.name)
    group=[]
    for n,p in enumerate(files,1):
        im=Image.open(p)
        row=dict(id=f'{prefix}{n:03}',old=str(p.relative_to(root)),width=im.width,height=im.height,exif_orientation=im.getexif().get(274,1),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        rows.append(row); group.append(row)
    for start in range(0,len(group),8):
        sheet=Image.new('RGB',(1600,2200),'#eeeeee'); d=ImageDraw.Draw(sheet)
        for k,row in enumerate(group[start:start+8]):
            im=ImageOps.exif_transpose(Image.open(root/row['old'])).convert('RGB'); im.thumbnail((770,490))
            x=(k%2)*800;y=(k//2)*550
            sheet.paste(im,(x+(800-im.width)//2,y+35+(490-im.height)//2))
            d.text((x+15,y+5),row['id']+' '+Path(row['old']).stem[:30],fill='black',font=font)
        sheet.save(out/'预览'/f'{prefix}_{start//8+1:02}.jpg',quality=90)
(out/'原始清单.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(rows)} images inventoried')

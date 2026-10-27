# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('scholarship/整理说明与索引/工具/add_new.py')
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import csv,json,hashlib,zipfile,html
from collections import Counter
from urllib.parse import quote
root=workspace_root();out=root/'整理说明与索引'
rows=json.loads((out/'素材索引.json').read_text(encoding='utf-8'))
new=[('P023','68f37e843306769cd99dcaa2d3afb843.png','05_个人形象','正装肖像_带英文署名','合成示例内容：通过项目实践展示文档制作与检查流程'),('P024','ChatGPT Image 2026年9月10日 09_19_42 (1).png','06_学校标识','示例大学_校徽及中英文校名横版','合成示例内容：通过项目实践展示文档制作与检查流程')]
with zipfile.ZipFile(root/'原始照片备份_整理前.zip','a',compression=zipfile.ZIP_STORED) as z:
    for id,oldname,category,title,notes in new:
        original_path=root/'项目经历照片'/oldname
        dest=root/'项目经历照片'/category/f'{id}_日期待补_{title}.png'
        p=original_path if original_path.exists() else dest
        r=dict(id=id,old=str(original_path.relative_to(root)),category=category,date='日期待补',title=title,notes=notes,corrected=False)
        with Image.open(p) as im:r.update(width=im.width,height=im.height,final_width=im.width,final_height=im.height,exif_orientation=im.getexif().get(274,1))
        r['sha256']=r['final_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
        arc=Path(r['old']).as_posix()
        if arc not in z.namelist(): z.write(p,arc)
        assert hashlib.sha256(z.read(arc)).hexdigest()==r['sha256']
        r['new']=(Path('项目经历照片')/category/f'{id}_日期待补_{title}.png').as_posix()
        dest=root/r['new'];dest.parent.mkdir(exist_ok=True)
        if p != dest:
            assert not dest.exists()
            p.rename(dest)
        rows.append(r)
(out/'素材索引.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
original=json.loads((out/'原始清单.json').read_text(encoding='utf-8'))
original.extend({k:r[k] for k in ['id','old','width','height','exif_orientation','sha256']} for r in rows[-2:])
(out/'原始清单.json').write_text(json.dumps(original,ensure_ascii=False,indent=2),encoding='utf-8')
manual={'H003','H023','H041','H044'}
code='fields='+(out/'工具/organize.py').read_text(encoding='utf-8').split('fields=',1)[1]
exec(code)
p=out/'素材总览.html';s=p.read_text(encoding='utf-8').replace('71张素材','73张素材').replace('71 / 71','73 / 73').replace("' / 71'","' / 73'");p.write_text(s,encoding='utf-8')
p=out/'整理完成说明.md';s=p.read_text(encoding='utf-8').replace('71','73').replace('22张','24张').replace('5类经历','6类经历').replace('P022','P024').replace('55张','57张');s+='\n合成示例内容：通过项目实践展示文档制作与检查流程\n';p.write_text(s,encoding='utf-8')

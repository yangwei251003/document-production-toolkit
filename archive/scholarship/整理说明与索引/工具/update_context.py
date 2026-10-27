# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('scholarship/整理说明与索引/工具/update_context.py')
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import csv,json,hashlib,html
from collections import Counter
from urllib.parse import quote
root=workspace_root();out=root/'整理说明与索引'
rows=json.loads((out/'素材索引.json').read_text(encoding='utf-8'))
for r in rows:
    if r['id'] in ['H017','H018','P015']:
        r['notes']='合成示例内容：通过项目实践展示文档制作与检查流程'
    if r['id'] in ['P004','P006','P017','P019','P020']:
        r['notes']+='；合成示例内容：通过项目实践展示文档制作与检查流程'
    if r['id'] in ['H040','H041']:
        r['title']='合成示例内容：通过项目实践展示文档制作与检查流程_'+('铜奖公示' if r['id']=='H040' else '铜奖证书')
        p=root/r['new'];dest=p.with_name(f"{r['id']}_{r['date']}_{r['title']}{p.suffix}")
        if p!=dest:
            assert not dest.exists();p.rename(dest);r['new']=dest.relative_to(root).as_posix()
    if r['id']=='P024':r['notes']+='；已保留原始透明通道。'
(out/'素材索引.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
manual={'H003','H023','H041','H044'}
exec('fields='+(out/'工具/organize.py').read_text(encoding='utf-8').split('fields=',1)[1])
p=out/'素材总览.html';s=p.read_text(encoding='utf-8').replace('71张素材','73张素材').replace('71 / 71','73 / 73').replace("' / 71'","' / 73'");p.write_text(s,encoding='utf-8')
p=out/'后续请提供的信息.md';s=p.read_text(encoding='utf-8');s=s.replace('合成示例内容：通过项目实践展示文档制作与检查流程','合成示例内容：通过项目实践展示文档制作与检查流程.md》；合成示例内容：通过项目实践展示文档制作与检查流程').replace('所有71张图片','所有73张图片');p.write_text(s,encoding='utf-8')
p=out/'国奖答辩调研与内容设计建议.md';s=p.read_text(encoding='utf-8').replace('个人信息及本校要求尚未齐全','合成示例内容：通过项目实践展示文档制作与检查流程').replace('所有71张','所有73张');s+='\n\n合成示例内容：通过项目实践展示文档制作与检查流程.md》。合成示例内容：通过项目实践展示文档制作与检查流程.md》。合成示例内容：通过项目实践展示文档制作与检查流程\n';p.write_text(s,encoding='utf-8')
print('Context updated.')

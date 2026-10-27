# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('career/fetch_ppt_references.py')
from pathlib import Path
import requests, concurrent.futures, zipfile, io
from lxml import etree
import sys
sys.stdout.reconfigure(encoding='utf-8')
out = Path(__file__).resolve().parents[1] / 'PPT设计方案' / '调研参考'
out.mkdir(parents=True, exist_ok=True)
items = [
 ('金奖选手分享_现场1.png',source_path('fixture-portrait.png')),
 ('金奖选手分享_现场2.png',source_path('fixture-portrait.png')),
 ('北科大省级金奖_现场.jpeg',source_path('fixture-portrait.png')),
 ('第四届就业赛道官方方案.docx',source_path('W020261010465563631809.docx'))
]
def fetch(item):
    name,url=item
    try:
        r=requests.get(url,timeout=25);r.raise_for_status()
        (out/name).write_bytes(r.content)
        if name.endswith('.docx'):
            z=zipfile.ZipFile(io.BytesIO(r.content));root=etree.fromstring(z.read('word/document.xml'))
            paras=[''.join(p.itertext()) for p in root.xpath('//w:p',namespaces={'w':source_path('main')})]
            (out/'官方方案提取.txt').write_text('\n'.join(paras),encoding='utf-8')
        return [name,len(r.content),'OK']
    except Exception as e: return [name,str(e)]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    for item in ex.map(fetch,items): print(item)

# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('career/revision_assets.py')
from pathlib import Path
import requests,json,re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
ROOT=workspace_root()
ROOT.mkdir(exist_ok=True)
AS=ROOT/'assets';AS.mkdir(exist_ok=True)
pages=[source_path('PowerGrid.html'),source_path('electricity'),source_path('www.ikingtec.com')]
rows=[]
for n,url in enumerate(pages):
    try:
        r=requests.get(url,timeout=20);r.raise_for_status()
        (AS/f'page_{n}.html').write_text(r.text,'utf-8')
        soup=BeautifulSoup(r.text,'html.parser')
        imgs=[]
        for img in soup.find_all('img'):
            src=img.get('data-src') or img.get('src')
            if src: imgs.append({'url':urljoin(url,src),'alt':img.get('alt',''),'context':img.parent.get_text(' ',strip=True)[:100]})
        rows.append({'url':url,'status':r.status_code,'images':imgs})
        print(json.dumps({'page':n,'url':url,'images':imgs[:45]},ensure_ascii=False))
    except Exception as e: print(url,str(e))
(AS/'web-image-inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),'utf-8')
for name,url in [('uat_grid.jpg',source_path('fixture-portrait.png')),('uat_station.jpg',source_path('fixture-portrait.png'))]:
    r=requests.get(url,timeout=20);r.raise_for_status();(AS/name).write_bytes(r.content)

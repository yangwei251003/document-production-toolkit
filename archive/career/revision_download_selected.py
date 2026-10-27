# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('career/revision_download_selected.py')
from pathlib import Path
import requests,json
root=workspace_root()
assets=[
('dji_tower.jpg',source_path('fixture-portrait.png'),source_path('electricity'),'输电杆塔巡检'),
('dji_field.jpg',source_path('fixture-portrait.png'),source_path('electricity'),'高原电力巡检'),
('iking_system.jpg',source_path('fixture-portrait.png'),source_path('www.ikingtec.com'),'基础设施层'),
('iking_grid.jpg',source_path('fixture-portrait.png'),source_path('www.ikingtec.com'),'电力行业')]
for name,url,page,label in assets:
    r=requests.get(url,timeout=20);r.raise_for_status();(root/name).write_bytes(r.content)
data=[{'file':name,'url':url,'source_page':page,'description':label,'use':'官网行业场景参考，非个人经历照片'} for name,url,page,label in assets]
data += [{'file':'uat_grid.jpg','url':source_path('fixture-portrait.png'),'source_page':source_path('6.html'),'description':'电网巡检场景','use':'官网行业场景参考，非个人经历照片'},{'file':'uat_station.jpg','url':source_path('fixture-portrait.png'),'source_page':source_path('6.html'),'description':'电站巡检场景','use':'官网行业场景参考，非个人经历照片'}]
(root/'selected-assets.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf-8')
print('Downloaded',len(assets),'official assets')

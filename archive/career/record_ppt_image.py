# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('career/record_ppt_image.py')
from pathlib import Path
from PIL import Image
import sys,json,shutil,hashlib
ROOT=workspace_root()
manifest=ROOT/'imagegen-manifest.json'
rows=json.loads(manifest.read_text(encoding='utf-8'))
if sys.argv[1]=='approve':
    n=int(sys.argv[2]);row=next(r for r in rows if r['slide']==n)
    row['visual_review']='PASS';row['review_notes']=sys.argv[3]
else:
    n=int(sys.argv[1]);src=Path(sys.argv[2]);dest=ROOT/'slides'/f'{n:02d}.png'
    shutil.copy2(src,dest)
    with Image.open(dest) as im:size=list(im.size)
    row={'slide':n,'prompt_file':str(ROOT/'prompts'/f'{n:02d}.md'),'generated_source':str(src),'copied_to':str(dest),'backend':'built-in imagegen','dimensions':size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'visual_review':'PENDING'}
    old=next((r for r in rows if r['slide']==n),None)
    if old:row['prior_attempts']=old.get('prior_attempts',[])+[old]
    rows=[r for r in rows if r['slide']!=n]+[row]
manifest.write_text(json.dumps(sorted(rows,key=lambda x:x['slide']),ensure_ascii=False,indent=2),encoding='utf-8')
print('Recorded',n)

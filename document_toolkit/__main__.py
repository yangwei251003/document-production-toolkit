import argparse,ast,hashlib,html,importlib.metadata,json,runpy,sys,zipfile
from pathlib import Path
from .runtime import synthetic_resume_session

ROOT=Path(__file__).resolve().parents[1]

def source_index():
    return json.loads((ROOT/'docs/source-map.json').read_text(encoding='utf-8'))

def inspect_sources():
    rows=[]
    for item in source_index():
        path=ROOT/item['archived_path']
        syntax='PowerShell static parse required on Windows'
        if path.suffix=='.py':ast.parse(path.read_text(encoding='utf-8'));syntax='Python syntax passed'
        elif path.suffix in ('.js','.mjs','.cjs'):syntax='Node static syntax verification required'
        rows.append({'id':item['id'],'class':item['execution_class'],'syntax':syntax,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    return rows

def demo(output):
    """Run the preserved four-variant resume flow against newly created synthetic data."""
    from PIL import Image,ImageDraw
    from docx import Document
    output=Path(output).resolve()
    if output.exists():raise ValueError('Choose a new output directory; existing files are never overwritten.')
    output.mkdir(parents=True)
    (output/'工作记录').mkdir();(output/'assets').mkdir()
    portrait=Image.new('RGB',(400,520),'#e8f2f6');draw=ImageDraw.Draw(portrait)
    draw.ellipse((120,60,280,220),fill='#548294');draw.rounded_rectangle((70,240,330,510),radius=90,fill='#548294')
    portrait.save(output/'assets/fixture-portrait.png')
    archive=ROOT/'archive/career/build_resumes.py'
    with synthetic_resume_session(output):runpy.run_path(str(archive),run_name='__document_synthetic_demo__')
    review=output/'review';review.mkdir();(review/'downloads').mkdir()
    documents=[]
    for path in sorted((output/'交付文件').glob('*.docx')):
        content=path.read_bytes();doc=Document(path)
        with zipfile.ZipFile(path) as package:
            assert 'word/document.xml' in package.namelist()
            assert any(x.startswith('word/media/') for x in package.namelist())
            xml=package.read('word/document.xml').decode('utf-8')
            assert '示例同学' in xml and '[示例电话]' in xml
        (review/'downloads'/path.name).write_bytes(content)
        documents.append({'name':path.name,'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content),'paragraphs':[p.text for p in doc.paragraphs if p.text.strip()]})
    assert len(documents)==4
    result={'synthetic':True,'generator':'archive/career/build_resumes.py','archive_scripts':len(source_index()),'documents':documents,'office_automation_run':False,'network_requests':0,'word_pagination_verified':False}
    (output/'demo-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    cards=[]
    for i,doc in enumerate(documents):
        paragraphs=''.join('<p>'+html.escape(p)+'</p>' for p in doc['paragraphs'])
        cards.append(f'<article id="doc-{i}" class="sheet"><div class="sheet-top"><span>SYNTHETIC EXAMPLE / {i+1:02}</span><a href="downloads/{html.escape(doc["name"])}">下载实际生成的 DOCX</a></div><h2>{html.escape(doc["name"].removesuffix(".docx"))}</h2>{paragraphs}</article>')
    links=''.join(f'<a href="#doc-{i}">{i+1:02} · {html.escape(d["name"].removesuffix(".docx"))}</a>' for i,d in enumerate(documents))
    page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Document Production Toolkit</title><style>*{box-sizing:border-box}body{margin:0;background:#edf2f5;color:#203b4a;font-family:system-ui,"Microsoft YaHei",sans-serif}header{padding:58px 7vw 38px;background:#173b4e;color:#fff}small{letter-spacing:.18em;color:#a7d8df}h1{font-size:clamp(28px,4vw,48px);line-height:1.2;margin:15px 0}header p{max-width:780px;line-height:1.8;color:#cee0e6}nav{display:flex;flex-wrap:wrap;gap:10px;padding:22px 7vw}nav a,a{color:#226279}nav a{background:#fff;padding:10px 14px;text-decoration:none;border-radius:7px}.stats{display:flex;gap:28px;margin-top:30px}.stats b{display:block;font-size:29px;color:#fff}.stats span{font-size:13px;color:#cee0e6}main{max-width:1100px;margin:0 auto;padding:0 24px 45px}.sheet{background:white;margin:22px 0;padding:35px 48px;border:1px solid #dbe5eb;border-radius:12px;box-shadow:0 8px 30px #254d6410}.sheet-top{display:flex;justify-content:space-between;gap:15px;font-size:12px;letter-spacing:.06em;color:#668592}.sheet h2{font-size:22px;border-bottom:2px solid #9bbbc7;padding-bottom:15px}.sheet p{line-height:1.8;font-size:14px;overflow-wrap:anywhere}footer{text-align:center;padding:20px;color:#668592}@media(max-width:650px){header{padding:34px 24px}.sheet{padding:24px}.sheet-top{display:block}.sheet-top a{display:block;margin-top:12px}.stats{gap:18px}}</style><header><small>DOCUMENT PRODUCTION TOOLKIT</small><h1>从脚本到成品，让制作过程可检查</h1><p>保全简历、演示文稿、申请表与素材索引中的独有程序。此页来自真实运行的合成简历子流程，展示实际 DOCX 的段落内容；它不是 Word 分页或原始个人材料截图。</p><div class="stats"><div><b>55</b><span>保留的历史脚本</span></div><div><b>4</b><span>实际生成的示例 DOCX</span></div><div><b>0</b><span>Office 与网络调用</span></div></div></header><nav>'''+links+'</nav><main>'+''.join(cards)+'</main><footer>全部示例为合成数据 · 无真实证件、电话、住址或个人照片 · Office 分页未验证</footer></html>'
    (review/'index.html').write_text(page,encoding='utf-8')
    print(json.dumps({'output':str(output),'documents':len(documents),'review':str(review/'index.html'),'office_run':False,'network_requests':0},ensure_ascii=False))
    return result

def main(argv=None):
    parser=argparse.ArgumentParser(description='Inspect historical document scripts or run an isolated synthetic resume demonstration.')
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('list');sub.add_parser('check');sub.add_parser('doctor')
    sp=sub.add_parser('session-demo');sp.add_argument('--output',required=True)
    dp=sub.add_parser('demo');dp.add_argument('--output',required=True,help='New directory for synthetic results; never overwrites an existing directory')
    args=parser.parse_args(argv)
    if args.command=='session-demo':
        from .session_demo import run
        run(args.output)
    elif args.command=='demo':demo(args.output)
    elif args.command in ('list','check'):print(json.dumps(inspect_sources(),ensure_ascii=False,indent=2))
    else:
        packages={}
        for name in ('python-docx','Pillow','openpyxl'):
            try:packages[name]=importlib.metadata.version(name)
            except importlib.metadata.PackageNotFoundError:packages[name]=None
        print(json.dumps({'python':sys.version.split()[0],'required_for_demo':packages,'Office':'not needed for synthetic demo; original Office flows not verified','network':'not needed'},ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,FileNotFoundError) as error:print(str(error),file=sys.stderr);raise SystemExit(2)

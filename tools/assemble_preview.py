import argparse,shutil
from pathlib import Path

def assemble(resume,session,output):
    resume,session,output=map(Path,(resume,session,output))
    if output.exists():raise ValueError('Preview output must be a new directory')
    if not (resume/'index.html').is_file() or not (session/'index.html').is_file():raise ValueError('Both verified review indexes are required')
    shutil.copytree(resume,output);shutil.copytree(session,output/'session')
    p=output/'index.html';s=p.read_text(encoding='utf-8').replace('<b>35</b>','<b>55</b>')
    s=s.replace('</nav>','<a href="session/index.html">新增20程序 · 工作簿与阅读转换示例 →</a></nav>')
    p.write_text(s,encoding='utf-8')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--resume',required=True);p.add_argument('--session',required=True);p.add_argument('--output',required=True);a=p.parse_args();assemble(a.resume,a.session,a.output)

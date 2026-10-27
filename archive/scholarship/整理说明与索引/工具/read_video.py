# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('scholarship/整理说明与索引/工具/read_video.py')
from pathlib import Path
import subprocess,json,hashlib,math
import imageio_ffmpeg,cv2
from PIL import Image,ImageDraw,ImageFont
root=workspace_root()
p=root/'o4VAjFDXFSguq3Sfg97kABrANiRQINhfgqTtdE.mp4'
out=root/'整理说明与索引/视频研读';frames=out/'字幕抽帧';frames.mkdir(parents=True,exist_ok=True)
ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ffmpeg,'-y','-hide_banner','-loglevel','error','-i',str(p),'-vf','fps=1,crop=1080:180:0:1320','-q:v','2',str(frames/'sub_%03d.jpg')],check=True)
files=sorted(frames.glob('sub_*.jpg'));font=ImageFont.truetype(source_path('msyh.ttc'),22)
for start in range(0,len(files),20):
 subset=files[start:start+20];sheet=Image.new('RGB',(2160,220*math.ceil(len(subset)/2)),'#eee');d=ImageDraw.Draw(sheet)
 for k,f in enumerate(subset):
  x=k%2*1080;y=k//2*220;sec=start+k
  d.text((x+15,y+5),f'{sec//60:02}:{sec%60:02} approx',font=font,fill='black');sheet.paste(Image.open(f),(x,y+35))
 sheet.save(out/f'字幕总览_{start//20+1:02}.jpg',quality=93)
v=cv2.VideoCapture(str(p));meta={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fps':v.get(cv2.CAP_PROP_FPS),'frames':v.get(cv2.CAP_PROP_FRAME_COUNT),'duration_seconds':v.get(cv2.CAP_PROP_FRAME_COUNT)/v.get(cv2.CAP_PROP_FPS),'subtitle_samples':len(files),'method':'1 fps burned-in subtitle visual sampling; timestamps approximate, not audio transcription'};v.release()
(out/'读取记录.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(meta))

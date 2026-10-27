# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('scholarship/整理说明与索引/工具/build_16page_plan.py')
from pathlib import Path
import json,html,re
from urllib.parse import quote
root=workspace_root();out=root/'答辩制作_16页定稿';out.mkdir(exist_ok=True)
assets={r['id']:r for r in json.loads((root/'整理说明与索引/素材索引.json').read_text(encoding='utf-8'))}
slides=[]
def add(ch,title,sub,lines,ids,layout,seconds,speech,notes='',kind='story'):
 slides.append(dict(page=len(slides)+1,chapter=ch,title=title,subtitle=sub,screen_text=lines,assets=ids,layout=layout,seconds=seconds,speech=speech,production_notes=notes,kind=kind))
add('封面','五育并进\n向实而行','国家奖学金答辩',
 ['示例同学','合成示例内容：通过项目实践展示文档制作与检查流程','博学扩域 · 热忱坚韧 · 善谋笃行'],['P023','P024'],
 '左侧56%合成示例内容：通过项目实践展示文档制作与检查流程%合成示例内容：通过项目实践展示文档制作与检查流程%；合成示例内容：通过项目实践展示文档制作与检查流程/16。',12,
 '合成示例内容：通过项目实践展示文档制作与检查流程',
 'P023合成示例内容：通过项目实践展示文档制作与检查流程', 'cover')
add('目录','五育相融，知行相长','从个人成长，到作品与行动',
 ['德｜以责任凝聚　03—05','智｜以专业创造　06—09','体｜以坚持强志　10—11','美｜以审美表达　12—13','劳｜以行动践行　14—15'],
 ['P025','P021','P033','P029','P032'],
 '合成示例内容：通过项目实践展示文档制作与检查流程',17,
 '合成示例内容：通过项目实践展示文档制作与检查流程',
 '合成示例内容：通过项目实践展示文档制作与检查流程','contents')
add('德','以责任凝聚\n以热忱服务','德｜善谋笃行',
 ['责任，是把身边的人放在心上。'],['P017','P025'],
 '合成示例内容：通过项目实践展示文档制作与检查流程%合成示例内容：通过项目实践展示文档制作与检查流程',5,
 '合成示例内容：通过项目实践展示文档制作与检查流程',
 '合成示例内容：通过项目实践展示文档制作与检查流程','transition')
add('德','把14人的第一次\n组织成共同的行动','三下乡｜从提前准备，到亲自示范',
 ['14合成示例内容：通过项目实践展示文档制作与检查流程','提前调研与请教 → 任务分工 → 亲自示范 → 总结复盘','合成示例内容：通过项目实践展示文档制作与检查流程'],['P025','P030','P006'],
 '合成示例内容：通过项目实践展示文档制作与检查流程%，合成示例内容：通过项目实践展示文档制作与检查流程%，合成示例内容：通过项目实践展示文档制作与检查流程',36,
 '合成示例内容：通过项目实践展示文档制作与检查流程',
 '32合成示例内容：通过项目实践展示文档制作与检查流程')
add('德','从自己做好\n到带动大家一起做好','德育｜组织带动与荣誉见证',
 ['45人班级｜以兴趣小组连接同学','五好班集体｜共同成长的成果','160合成示例内容：通过项目实践展示文档制作与检查流程'],['P010','P008','H025','H016','H030','H038'],
 '合成示例内容：通过项目实践展示文档制作与检查流程/H030/H038合成示例内容：通过项目实践展示文档制作与检查流程',27,
 '合成示例内容：通过项目实践展示文档制作与检查流程',
 'P010合成示例内容：通过项目实践展示文档制作与检查流程/H038合成示例内容：通过项目实践展示文档制作与检查流程','evidence')
add('智','博学扩域\n让知识走向应用','智｜学习的价值，在于解决问题',
 ['从前端与UI，到智能设备。','把学到的知识，做成有用的作品。'],['P005','P021'],
 '过渡页：左侧40%合成示例内容：通过项目实践展示文档制作与检查流程/02连接。',5,
 '合成示例内容：通过项目实践展示文档制作与检查流程',kind='transition')
add('智','让地方文旅\n多一份探索的趣味','代表项目①｜云游地图',
 ['需求｜旅游体验缺少趣味性','合成示例内容：通过项目实践展示文档制作与检查流程','合成示例内容：通过项目实践展示文档制作与检查流程','进展｜网站已上线，持续推进小程序优化'],['P005','H015'],
 '左侧约66%合成示例内容：通过项目实践展示文档制作与检查流程/本人完成/合成示例内容：通过项目实践展示文档制作与检查流程',29,
 '[示例地址]',
 '合成示例内容：通过项目实践展示文档制作与检查流程')
add('智','从取纸的不便\n出发做工程创新','代表项目②｜智能出纸机',
 ['合成示例内容：通过项目实践展示文档制作与检查流程','团队实践｜智能出纸机研发','合成示例内容：通过项目实践展示文档制作与检查流程','进展｜推进专利申请'],['P021','H008','H005'],
 '左侧60%合成示例内容：通过项目实践展示文档制作与检查流程/全国总决赛优秀奖。',27,
 '合成示例内容：通过项目实践展示文档制作与检查流程',
 '合成示例内容：通过项目实践展示文档制作与检查流程/合成示例内容：通过项目实践展示文档制作与检查流程')
add('智','以竞赛检验学习\n以作品沉淀能力','智育｜代表竞赛成果',
 ['Python本科组｜全国总决赛一等奖','Python挑战赛｜全国决赛三等奖','机器人智能家电创新赛｜广东省赛二等奖','合成示例内容：通过项目实践展示文档制作与检查流程'],['H035','H048','H008','H005'],
 '四张证书2×2，合成示例内容：通过项目实践展示文档制作与检查流程',15,
 '合成示例内容：通过项目实践展示文档制作与检查流程',
 '合成示例内容：通过项目实践展示文档制作与检查流程','evidence')
add('体','热忱坚韧\n在坚持中向前','体｜运动与自我管理',
 ['认真投入 · 保持专注 · 学会取舍','把持续行动，带进运动与学习。'],['P033','P026'],
 '合成示例内容：通过项目实践展示文档制作与检查流程',22,
 '合成示例内容：通过项目实践展示文档制作与检查流程',
 '合成示例内容：通过项目实践展示文档制作与检查流程','transition')
add('体','每一次认真投入\n都有成长的刻度','体育｜运动成绩与荣誉',
 ['广州马拉松｜净计时2:56:31','合成示例内容：通过项目实践展示文档制作与检查流程:31:02','源羽杯青年组男子双打｜第一名','灯塔镇青年职工羽毛球赛男子组｜季军'],['H002','H012','H006','H026','P033'],
 '合成示例内容：通过项目实践展示文档制作与检查流程%；合成示例内容：通过项目实践展示文档制作与检查流程',15,
 '合成示例内容：通过项目实践展示文档制作与检查流程',
 '合成示例内容：通过项目实践展示文档制作与检查流程','evidence')
add('美','以审美表达\n以创作记录','美｜让表达具有自己的温度',
 ['从校园文创，到数字影像与主题表达。'],['P029','P027','P034'],
 '合成示例内容：通过项目实践展示文档制作与检查流程%合成示例内容：通过项目实践展示文档制作与检查流程/合成示例内容：通过项目实践展示文档制作与检查流程',8,
 '合成示例内容：通过项目实践展示文档制作与检查流程',
 'P027合成示例内容：通过项目实践展示文档制作与检查流程','transition')
add('美','让创作被看见\n让表达有回响','美育｜作品与荣誉见证',
 ['《合成示例内容：通过项目实践展示文档制作与检查流程','红色精神视频类比赛｜二等奖','学院征文活动｜三等奖'],['P029','H039','H013','H037','P031'],
 '合成示例内容：通过项目实践展示文档制作与检查流程/合成示例内容：通过项目实践展示文档制作与检查流程',20,
 '《合成示例内容：通过项目实践展示文档制作与检查流程',
 'P031合成示例内容：通过项目实践展示文档制作与检查流程','evidence')
add('劳','以行动践行\n在具体工作中担责','劳｜把责任落在亲手完成的事情上',
 ['清扫环境 · 整理空间 · 协作完成'],['P032','P028'],
 '合成示例内容：通过项目实践展示文档制作与检查流程%，P028窄竖图占25%；合成示例内容：通过项目实践展示文档制作与检查流程',10,
 '合成示例内容：通过项目实践展示文档制作与检查流程',kind='transition')
add('劳','把责任落在行动里','劳育｜真实实践与过程见证',
 ['校园清扫｜协作整理公共环境','室内清扫｜从身边空间做起','从参与到完成，认真做好具体工作。'],['P032','P028','P003'],
 '合成示例内容：通过项目实践展示文档制作与检查流程%，合成示例内容：通过项目实践展示文档制作与检查流程',17,
 '合成示例内容：通过项目实践展示文档制作与检查流程',
 '合成示例内容：通过项目实践展示文档制作与检查流程','evidence')
add('结束','让全面发展\n落在每一次具体行动里','博学扩域 · 热忱坚韧 · 善谋笃行',
 ['把知识做成作品，把热忱化为行动。','感谢各位老师，请批评指正。','示例同学'],['P023','P025','P021','P032'],
 '合成示例内容：通过项目实践展示文档制作与检查流程/16进度完整。',12,
 '合成示例内容：通过项目实践展示文档制作与检查流程',kind='closing')
assert len(slides)==16
for s in slides:
 for aid in s['assets']:assert aid in assets
plan={'title':'五育并进，向实而行','version':'16页融合版','seconds':sum(s['seconds'] for s in slides),'slides':slides}
(out/'逐页内容与素材映射.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
design='# 合成示例内容：通过项目实践展示文档制作与检查流程\n\n合成示例内容：通过项目实践展示文档制作与检查流程\n\n## 一、结构与重点\n\n16合成示例内容：通过项目实践展示文档制作与检查流程\n\n5合成示例内容：通过项目实践展示文档制作与检查流程\n\n## 二、全套视觉系统\n\n- 画幅：16:9；建议最终3840×2160，合成示例内容：通过项目实践展示文档制作与检查流程×1080坐标理解。\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 配色：暖白#F6F3EC，墨绿#123F37，深灰#283C38，金色#B58B4D；技术页只局部增加深蓝#173C56。合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程/合成示例内容：通过项目实践展示文档制作与检查流程/合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程/ 16”至“16 / 16”；合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程%—75%。合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程/合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程/播放器/合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n\n## 三、逐页执行卡\n'
for s in slides:
 design+=f"\n### {s['page']:02d}｜{s['title'].replace(chr(10),'，')}（{s['seconds']}秒）\n\n**页面小标题：** {s['subtitle']}\n\n**上屏正文：**\n"+''.join('- '+x+'\n' for x in s['screen_text'])
 design+='\n**选图：** '+ '；'.join(f"{aid} {assets[aid]['title']}" for aid in s['assets'])+'。\n\n**排版：** '+s['layout']+'\n\n**口播：** '+s['speech']+'\n'
 if s['production_notes']:design+='\n**制作核对：** '+s['production_notes']+'\n'
design+='\n## 合成示例内容：通过项目实践展示文档制作与检查流程\n\n合成示例内容：通过项目实践展示文档制作与检查流程\n\n合成示例内容：通过项目实践展示文档制作与检查流程:9合成示例内容：通过项目实践展示文档制作与检查流程/合成示例内容：通过项目实践展示文档制作与检查流程\n\n合成示例内容：通过项目实践展示文档制作与检查流程\n\n## 五、事实与表达边界\n\n- H025合成示例内容：通过项目实践展示文档制作与检查流程\n- P010合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程/H038合成示例内容：通过项目实践展示文档制作与检查流程\n- P029合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n'
(out/'16页逐页文案与视觉执行稿.md').write_text(design,encoding='utf-8')
speech='# 合成示例内容：通过项目实践展示文档制作与检查流程\n\n合成示例内容：通过项目实践展示文档制作与检查流程\n'
for s in slides:speech+=f"\n## 第{s['page']:02d}页｜目标{s['seconds']}秒\n\n{s['speech']}\n"
count=sum(len(re.findall(r'[\u4e00-\u9fff]',s['speech'])) for s in slides)
speech+=f'\n计划总时长{plan['seconds']}秒；稿件约{count}合成示例内容：通过项目实践展示文档制作与检查流程\n'
speech+='\n## 现场表达提示\n\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n\n## 常见追问的回答方向\n\n1. 合成示例内容：通过项目实践展示文档制作与检查流程\n2. 合成示例内容：通过项目实践展示文档制作与检查流程\n3. 合成示例内容：通过项目实践展示文档制作与检查流程\n4. 合成示例内容：通过项目实践展示文档制作与检查流程\n5. 合成示例内容：通过项目实践展示文档制作与检查流程\n'
(out/'16页配套答辩稿与问答提纲.md').write_text(speech,encoding='utf-8')
# Browser-based review artifact: actual source images arranged for review, no generated imagery.
css='''*{box-sizing:border-box}body{margin:0;background:#dfe4e0;font-family:'Microsoft YaHei',sans-serif;color:#203b34}header{padding:28px 5%;background:#123f37;color:#fff}header p{max-width:1050px;line-height:1.7}.wrap{max-width:1500px;margin:auto;padding:30px}.slide{aspect-ratio:16/9;background:#f6f3ec;position:relative;padding:4% 5% 5%;margin:30px 0 10px;overflow:hidden;box-shadow:0 12px 32px #183f3720;container-type:inline-size}.kicker{font-size:1.15cqw;color:#957343;letter-spacing:.16em;margin-bottom:.7cqw}.slide h2{font-family:SimSun,serif;font-weight:900;font-size:3.6cqw;line-height:1.15;margin:0 0 1.2cqw;white-space:pre-line}.slide .subtitle{font-size:1.4cqw;color:#5d7169}.body{display:flex;gap:2.5%;height:68%;margin-top:1.4cqw}.copy{width:32%;font-size:1.65cqw;line-height:1.55}.copy p{margin:.5cqw 0 1.1cqw}.pics{width:68%;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1cqw;min-height:0}.pics figure{margin:0;background:#fff;min-height:0;display:flex;flex-direction:column;overflow:hidden;border:1px solid #e1dfd7}.pics img{width:100%;height:calc(100% - 2.1cqw);min-height:0;object-fit:contain;flex:1}.pics figcaption{font-size:.94cqw;padding:.3cqw .6cqw;color:#53655e;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;height:2.1cqw;flex-shrink:0}.pics.count-2 figure:first-child{grid-row:span 2}.pics.count-2{grid-template-columns:2fr 1fr}.pics.count-1{grid-template-columns:1fr}.pics.count-3{grid-template-columns:1.5fr 1fr}.pics.count-3 figure:first-child{grid-row:span 2}.footer{position:absolute;bottom:3%;left:5%;right:5%;display:flex;justify-content:space-between;font-size:1.05cqw;letter-spacing:.07em}.track{position:absolute;bottom:1.7%;left:5%;right:5%;height:3px;background:#d9dfd7}.track span{display:block;height:100%;background:#b58b4d}.transition{background:#123f37;color:#fff}.transition .subtitle,.transition .kicker{color:#dac9a1}.transition .copy{font-size:2cqw}.transition .body{height:61%}.transition .pics figure{background:#204c42;border:0}.transition .pics figcaption{color:#eee}.evidence .copy{width:24%;font-size:1.35cqw}.evidence .pics{width:76%}.cover .body,.closing .body{height:63%}.cover .copy,.closing .copy{width:48%}.cover .pics,.closing .pics{width:52%}.cover .pics{grid-template-columns:1fr 1fr}.cover .pics figure:first-child{grid-row:span 2}.contents .body{display:block;height:68%}.contents .copy{display:none}.contents .pics{width:100%;height:100%;grid-template-columns:repeat(5,1fr)}.contents .pics img{object-fit:cover}.contents .pics figcaption{font-size:1.1cqw;white-space:normal;height:4.8cqw}.notes{background:#fff;padding:20px 26px;border-radius:5px;line-height:1.7;font-size:14px}.notes summary{cursor:pointer;font-weight:bold}.notes p{margin:10px 0}.nav{display:flex;flex-wrap:wrap;gap:8px}.nav a{color:#fff;background:#ffffff1a;padding:7px 12px;border-radius:4px;text-decoration:none}.badge{position:absolute;right:5%;top:4%;font-size:1cqw;color:#85764f}.transition .badge{color:#d8c395}@media print{body{background:white}header,.notes{display:none}.wrap{padding:0;max-width:none}.slide{margin:0;box-shadow:none;break-after:page;width:100vw}.slide:last-child{break-after:auto}}'''
css+='''
#p1 h2{font-size:6.6cqw;position:absolute;left:6%;top:22%;z-index:2}#p1>.subtitle{position:absolute;left:6%;top:16%;font-size:1.8cqw}#p1 .body{position:absolute;inset:8% 6% 9%;height:auto;margin:0}#p1 .copy{position:absolute;left:0;top:57%;width:52%;font-size:1.65cqw}#p1 .pics{position:absolute;right:0;top:11%;height:88%;width:40%;display:block}#p1 .pics figure:first-child{height:100%;border:0;background:transparent}#p1 .pics figure:first-child svg{height:100%}#p1 .pics figcaption{display:none}#p1 .pics figure:last-child{position:absolute;right:0;top:-14%;width:88%;height:15%;border:0;background:transparent}#p1 .pics figure:last-child img{height:100%}
#p5 .body{height:65%}#p5 .pics{grid-template-columns:repeat(3,1fr);grid-template-rows:47% 53%}#p5 .pics figure:nth-child(3){font-size:1cqw}#p5 .pics figure:nth-child(3) div{font-size:1.05cqw!important;padding:.5cqw!important}#p5 .pics figure:nth-child(3) small{display:none}
#p13 .copy{width:24%}#p13 .pics{grid-template-columns:1.2fr 1fr 1fr;grid-template-rows:56% 44%}#p13 .pics figure:first-child{grid-row:1 / 3}#p13 .pics figure:last-child{grid-column:3;grid-row:2}
.pics.count-5{grid-template-columns:repeat(3,1fr)}.contents .pics.count-5{grid-template-columns:repeat(5,1fr)}.pics svg{display:block;overflow:hidden}.contents .pics svg{background:#ecece4}.pics.count-4{grid-template-rows:repeat(2,minmax(0,1fr))}.pics.count-6{grid-template-rows:repeat(3,minmax(0,1fr))}
'''
def img_html(aid,s):
 a=assets[aid];url='../'+quote(a['new']);extra='';caption=aid+' '+a['title']
 if aid=='H025':
  # No sensitive source pixels are loaded on the review board. Text stands in for sanitized excerpt.
  return '<figure><div style="padding:1cqw;font-size:1.25cqw;line-height:1.7;flex:1">24电气工程本科5班<br>示例同学<br><b>五好班集体</b><br><small>合成示例内容：通过项目实践展示文档制作与检查流程</small></div><figcaption>H025 名单信息摘录</figcaption></figure>'
 if aid=='P023':extra=' style="object-fit:cover;object-position:50% 0%"'
 if aid=='P026':extra=' style="object-fit:cover;object-position:center"'
 if aid=='P024':extra=' style="object-fit:contain;padding:12px"'
 if s['kind']=='contents':caption=s['screen_text'][s['assets'].index(aid)]
 crops={'P023':(0,0,1122,1225),'P026':(0,885,1080,610),'P027':(42,70,1835,925),'P029':(142,620,785,1350),'P034':(24,80,1870,850)}
 if aid in crops:
  x,y,w,h=crops[aid];fw=assets[aid]['final_width'];fh=assets[aid]['final_height']
  clip=f'crop-{s["page"]}-{aid}'
  svg=f'<svg viewBox="{x} {y} {w} {h}" style="width:100%;height:calc(100% - 2.1cqw);flex:1;min-height:0" preserveAspectRatio="xMidYMid meet"><defs><clipPath id="{clip}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath></defs><image href="{url}" width="{fw}" height="{fh}" clip-path="url(#{clip})"/></svg>'
  return f'<figure data-asset="{aid}">{svg}<figcaption>{html.escape(caption)}</figcaption></figure>'
 return f'<figure><img src="{url}"{extra}><figcaption>{html.escape(caption)}</figcaption></figure>'
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>合成示例内容：通过项目实践展示文档制作与检查流程</title><style>'+css+'</style><header><h1>合成示例内容：通过项目实践展示文档制作与检查流程</h1><p>合成示例内容：通过项目实践展示文档制作与检查流程</p><nav class="nav">'+''.join(f'<a href="#p{s["page"]}">{s["page"]:02d} {s["chapter"]}</a>' for s in slides)+'</nav></header><main class="wrap">'
for s in slides:
 page+=f'<section id="p{s['page']}" class="slide {s['kind']}"><span class="badge">选图与排版草案</span><div class="kicker">示例同学 / 国家奖学金答辩</div><h2>{html.escape(s['title'])}</h2><div class="subtitle">{html.escape(s['subtitle'])}</div><div class="body"><div class="copy">'+''.join('<p>'+html.escape(t)+'</p>' for t in s['screen_text'])+f'</div><div class="pics count-{len(s["assets"])}">'+''.join(img_html(aid,s) for aid in s['assets'])+f'</div></div><footer class="footer"><span>{s['chapter']}\u3000合成示例内容：通过项目实践展示文档制作与检查流程</span><span>{s['page']:02d} / 16</span></footer><div class="track"><span style="width:{s['page'] / 16 * 100}%"></span></div></section><details class="notes"><summary>第{s['page']:02d}页 · 口播{s['seconds']}合成示例内容：通过项目实践展示文档制作与检查流程</summary><p><b>精细排版：</b>{html.escape(s['layout'])}</p><p><b>口播：</b>{html.escape(s['speech'])}</p><p><b>核对：</b>{html.escape(s['production_notes'])}</p></details>'
page+='</main></html>'
(out/'16页选图与排版草案.html').write_text(page,encoding='utf-8')
used=sorted({i for s in slides for i in s['assets']});manifest=[]
for aid in used:manifest.append({'id':aid,'path':str(root/assets[aid]['new']),'pages':[s['page'] for s in slides if aid in s['assets']]})
(out/'入选素材与使用页码.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'slides':len(slides),'seconds':plan['seconds'],'speech_chinese_characters':count,'unique_assets':len(used),'references':sum(len(s['assets']) for s in slides),'out':str(out)},ensure_ascii=False))

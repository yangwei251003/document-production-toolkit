# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('career/prepare_v2.py')
from pathlib import Path
import json,copy,shutil,hashlib
R=workspace_root(); V=R/'PPT制作_V2'; O=json.loads((R/'PPT制作/outline.json').read_text('utf-8'))
for d in ['prompts','slides','qa']: (V/d).mkdir(exist_ok=True)
A=V/'assets'; B=Path(source_path('国家奖学金评审')); P=B/'项目经历照片'; H=B/'荣誉奖状证书'
mapping=[1,2,3,4,None,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
retained={11,13,17,20,21,22}
slides=[]
for n,old in enumerate(mapping,1):
 s=copy.deepcopy(O['slides'][(old or 4)-1]);s.update(slide_number=n,original_slide=old,hidden=n>19,generation_status='REUSE' if n in retained else 'PENDING',review_status='PENDING',generated_image=f'slides/{n:02}.png',prompt_file=str(V/'prompts'/f'{n:02}.md'));slides.append(s)
def change(n,text,design,refs=None,speech=None):
 s=slides[n-1];s['exact_text']=text.split('\n');s['title']=s['exact_text'][0];s['design_spec_markdown']=design
 if refs is not None:s['reference_paths']=[str(x) for x in refs]
 if speech:s['speaker_draft']=speech
portrait=P/'05_个人形象/P007_日期待补_个人正装白底证件照.jpg'
change(1,'以技为桥\n让低空服务电力\n求职综合展示\n合成示例内容：通过项目实践展示文档制作与检查流程\n示例同学\n合成示例内容：通过项目实践展示文档制作与检查流程\n2025—2026学年国家奖学金获得者','合成示例内容：通过项目实践展示文档制作与检查流程%合成示例内容：通过项目实践展示文档制作与检查流程',[portrait,A/'uat_grid.jpg'])
change(2,'合成示例内容：通过项目实践展示文档制作与检查流程\n目录\n01 职业目标\n理解电力场景\n02 岗位胜任\n用真实经历作答\n03 发展潜力\n面向上岗持续补强\n合成示例内容：通过项目实践展示文档制作与检查流程','合成示例内容：通过项目实践展示文档制作与检查流程/02/03合成示例内容：通过项目实践展示文档制作与检查流程',[A/'dji_tower.jpg',A/'uat_station.jpg',A/'uat_grid.jpg'])
change(3,'合成示例内容：通过项目实践展示文档制作与检查流程\n电气专业\n理解能源应用语境\n无人机实践\n接触产品与教育场景\nAI协作\n组织调研与项目推进\n无人机技术销售工程师\n电力能源方向\n合成示例内容：通过项目实践展示文档制作与检查流程\n行业场景图：联合飞机','合成示例内容：通过项目实践展示文档制作与检查流程/02/03合成示例内容：通过项目实践展示文档制作与检查流程',[A/'uat_grid.jpg'])
change(4,'合成示例内容：通过项目实践展示文档制作与检查流程\n了解场景\n巡什么\n澄清需求\n解决什么\n解释方案\n如何选\n演示验证\n怎样验\n协同交付\n谁来用\n合成示例内容：通过项目实践展示文档制作与检查流程\n目标入口：技术销售 / 售前支持 / 解决方案培训生\n合成示例内容：通过项目实践展示文档制作与检查流程','上方35%合成示例内容：通过项目实践展示文档制作与检查流程+合成示例内容：通过项目实践展示文档制作与检查流程',[A/'dji_field.jpg'])
change(5,'合成示例内容：通过项目实践展示文档制作与检查流程\n大疆行业应用\n电力巡检产品与行业方案\n合成示例内容：通过项目实践展示文档制作与检查流程\n云圣智能\n无人机与机巢协同巡检\n合成示例内容：通过项目实践展示文档制作与检查流程\n联合飞机\n电网巡检与电站巡检\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程','合成示例内容：通过项目实践展示文档制作与检查流程',[A/'dji_field.jpg',A/'iking_system.jpg',A/'uat_station.jpg'],'合成示例内容：通过项目实践展示文档制作与检查流程')
change(6,'岗位胜任\n用真实经历\n回答岗位要求\n合成示例内容：通过项目实践展示文档制作与检查流程\n02','章节过渡。深海军蓝+合成示例内容：通过项目实践展示文档制作与检查流程',[A/'dji_tower.jpg'])
change(7,'合成示例内容：通过项目实践展示文档制作与检查流程\n2025—2026学年 国家奖学金\n专业竞赛与校级荣誉\n2026 合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程\n2025 合成示例内容：通过项目实践展示文档制作与检查流程\nPython合成示例内容：通过项目实践展示文档制作与检查流程\n2024—2025学年 学校一等奖学金\n已获资格\n合成示例内容：通过项目实践展示文档制作与检查流程\n大学英语四级通过\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程','合成示例内容：通过项目实践展示文档制作与检查流程%合成示例内容：通过项目实践展示文档制作与检查流程',[H/'02_专业竞赛与创新创业/广东省教育厅无人机低空智能应用挑战赛三等奖.png',H/'02_专业竞赛与创新创业/H035_2025-11-29_全国大学生大数据分析技术技能大赛Python本科组全国总决赛_一等奖.png',H/'03_综合荣誉与组织管理/H045_2025-12_2024-2025学年_学校一等奖学金.png'],'合成示例内容：通过项目实践展示文档制作与检查流程')
change(8,'合成示例内容：通过项目实践展示文档制作与检查流程\n示例科技单位｜2026.09—至今\n01 无人机教育\n知识讲解与教学支持\n02 组装调试\n参与无人机装调实践\n03 宣传支持\n策划、海报与赛事物料\n宣传设计作品\n合成示例内容：通过项目实践展示文档制作与检查流程','白底，左侧大标题+合成示例内容：通过项目实践展示文档制作与检查流程%，合成示例内容：通过项目实践展示文档制作与检查流程%合成示例内容：通过项目实践展示文档制作与检查流程',[Path(slides[7]['reference_paths'][0])])
change(9,'合成示例内容：通过项目实践展示文档制作与检查流程\n14人团队\n25名儿童\n32个课程单元\n电学实验与用电安全教学\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程','合并两页。上部标题+合成示例内容：通过项目实践展示文档制作与检查流程%合成示例内容：通过项目实践展示文档制作与检查流程%课前/课堂/合成示例内容：通过项目实践展示文档制作与检查流程',[P/'03_志愿劳动与社会实践/P025_日期待补_三下乡电学实验课_互动演示.png',P/'03_志愿劳动与社会实践/P017_日期待补_三下乡儿童陪伴活动_校旗团队合影.jpg'],'合成示例内容：通过项目实践展示文档制作与检查流程')
change(10,'多面成长，支撑长期行动\n自律与韧性\n2025广州马拉松\n净计时 2:56:31\n合成示例内容：通过项目实践展示文档制作与检查流程\n组织与协作\n班长：服务45人班级\n合成示例内容：通过项目实践展示文档制作与检查流程\n参与班级与社团活动组织\n审美与表达\n《拾光记忆》校园文创作品\n校赛二等奖｜合作作品\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程','合成示例内容：通过项目实践展示文档制作与检查流程+合成示例内容：通过项目实践展示文档制作与检查流程/组织/审美。马拉松2:56:31合成示例内容：通过项目实践展示文档制作与检查流程',[P/'07_体育运动/P033_日期待补_羽毛球运动_室内球场现场.jpg',P/'02_校园分享与组织活动/P010_日期待补_教室集体活动_自拍合影.jpg',P/'08_美育作品与表达/P029_日期待补_拾光记忆_日常文创用品作品展示截图.jpg'],'合成示例内容：通过项目实践展示文档制作与检查流程')
change(12,'合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程\n理解任务 → 匹配能力 → 安排执行 → 检查结果\n我负责\n合成示例内容：通过项目实践展示文档制作与检查流程\nAI辅助\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程','合成示例内容：通过项目实践展示文档制作与检查流程%合成示例内容：通过项目实践展示文档制作与检查流程%合成示例内容：通过项目实践展示文档制作与检查流程',[])
change(14,'合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程\n先问需求\n合成示例内容：通过项目实践展示文档制作与检查流程\n解释方案\n采集、分析、报告与培训\n共同验证\n合成示例内容：通过项目实践展示文档制作与检查流程\n协同交付\n使用培训、反馈与复盘\n合成示例内容：通过项目实践展示文档制作与检查流程\n合成示例内容：通过项目实践展示文档制作与检查流程','左侧40%合成示例内容：通过项目实践展示文档制作与检查流程%合成示例内容：通过项目实践展示文档制作与检查流程',[A/'dji_tower.jpg'])
change(15,'合成示例内容：通过项目实践展示文档制作与检查流程\n岗位能力\n真实经历\n技术理解\n电气学习、无人机装调\n讲解表达\n无人机教育、电学互动课\n方案呈现\n合成示例内容：通过项目实践展示文档制作与检查流程\n协作执行\n带队实践、协会组织\n数字素养\nAI调研与项目协作\n合成示例内容：通过项目实践展示文档制作与检查流程','合成示例内容：通过项目实践展示文档制作与检查流程-05，每行左32%大能力名，右68%合成示例内容：通过项目实践展示文档制作与检查流程',[A/'uat_grid.jpg'])
change(16,'发展潜力\n把已有基础\n变成上岗能力\n下一步，走近真实场景\n03','合成示例内容：通过项目实践展示文档制作与检查流程',[A/'uat_station.jpg'])
change(18,'合成示例内容：通过项目实践展示文档制作与检查流程\n在校至2028\n深化实习与作品证据\n初入岗位\n合成示例内容：通过项目实践展示文档制作与检查流程\n后续发展\n合成示例内容：通过项目实践展示文档制作与检查流程\n接受海外出差及长期驻外\n合成示例内容：通过项目实践展示文档制作与检查流程\n行业场景图：联合飞机','合成示例内容：通过项目实践展示文档制作与检查流程+合成示例内容：通过项目实践展示文档制作与检查流程',[A/'uat_grid.jpg'])
change(19,'把技术讲清楚\n把方案做扎实\n示例同学\n合成示例内容：通过项目实践展示文档制作与检查流程\n感谢聆听，恳请指教','合成示例内容：通过项目实践展示文档制作与检查流程%，合成示例内容：通过项目实践展示文档制作与检查流程%，合成示例内容：通过项目实践展示文档制作与检查流程',[portrait,A/'uat_grid.jpg'])
seconds=[10,6,16,18,18,4,24,25,28,22,28,20,20,30,16,4,20,16,10,0,0,0]
common='合成示例内容：通过项目实践展示文档制作与检查流程:9合成示例内容：通过项目实践展示文档制作与检查流程/合成示例内容：通过项目实践展示文档制作与检查流程#10283F、合成示例内容：通过项目实践展示文档制作与检查流程-50pt视觉大小，正文22-28pt，次要注释14-16pt，四周5%合成示例内容：通过项目实践展示文档制作与检查流程'
rows=[];oldmanifest=json.loads((R/'PPT制作/imagegen-manifest.json').read_text('utf-8'))
for s,sec in zip(slides,seconds):
 n=s['slide_number'];s['speaker_seconds']=sec
 prompt=common+'\n\n页面设计：\n'+s['design_spec_markdown']+'\n\n合成示例内容：通过项目实践展示文档制作与检查流程\n'+'\n'.join(s['exact_text'])+'\n\n合成示例内容：通过项目实践展示文档制作与检查流程'
 (V/'prompts'/f'{n:02}.md').write_text(prompt,encoding='utf-8')
 if n in retained:
  old=s['original_slide'];src=R/'PPT制作/slides'/f'{old:02}.png';dest=V/'slides'/f'{n:02}.png';shutil.copy2(src,dest)
  row=copy.deepcopy(next(x for x in oldmanifest if x['slide']==old));row.update(slide=n,copied_to=str(dest),reuse_from_v1=old,visual_review='PASS',review_notes='按用户要求原第16页完整保留' if n==17 else '复核保留：项目实物/UI合成示例内容：通过项目实践展示文档制作与检查流程');rows.append(row)
O.update(slides=slides,stage='REVISION_GENERATING',main_slides=19,backup_slides=3,planned_seconds=sum(seconds),revision='V2');(V/'outline.json').write_text(json.dumps(O,ensure_ascii=False,indent=2),encoding='utf-8');(V/'imagegen-manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
rec=(R/'工作记录/record_ppt_image.py').read_text('utf-8').replace("/'PPT制作'","/'PPT制作_V2'");(R/'工作记录/record_v2_image.py').write_text(rec,encoding='utf-8')
(V/'修订说明.md').write_text('# 22页修订方案\n\n19合成示例内容：通过项目实践展示文档制作与检查流程\n\n'+ '\n'.join(f"- {s['slide_number']:02d} {s['title']}：{'保留已核对图' if s['slide_number'] in retained else '重新imagegen生成'}" for s in slides),encoding='utf-8')
print('Prepared all22 prompts; generated16/reuse6; seconds',sum(seconds))

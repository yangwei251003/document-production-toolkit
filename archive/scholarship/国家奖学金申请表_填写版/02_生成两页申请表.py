# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('scholarship/国家奖学金申请表_填写版/02_生成两页申请表.py')
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
from pathlib import Path

OUT=Path(__file__).resolve().parent
FINAL=OUT/'2025－2026学年国家奖学金申请审批表_示例同学_24电气工程本科5班.docx'
APPLICATION='合成示例内容：通过项目实践展示文档制作与检查流程'
RECOMMENDATION='合成示例内容：通过项目实践展示文档制作与检查流程'

def set_cell_text(cell, text, size=10.5, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, first_indent=False):
    cell.text=""
    p=cell.paragraphs[0]
    p.alignment=align
    p.paragraph_format.space_before=Pt(0)
    p.paragraph_format.space_after=Pt(0)
    p.paragraph_format.line_spacing=1.15
    if first_indent:
        p.paragraph_format.first_line_indent=Pt(size*2)
    run=p.add_run(text)
    run.bold=bold
    run.font.name="宋体"
    run._element.rPr.rFonts.set(qn("w:eastAsia"),"宋体")
    run.font.size=Pt(size)
    cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    return p

def set_cell_margins(cell, top=60, start=70, bottom=60, end=70):
    tc=cell._tc
    tcPr=tc.get_or_add_tcPr()
    tcMar=tcPr.first_child_found_in("w:tcMar")
    if tcMar is None:
        tcMar=OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for m,v in (("top",top),("start",start),("bottom",bottom),("end",end)):
        node=tcMar.find(qn("w:"+m))
        if node is None:
            node=OxmlElement("w:"+m);tcMar.append(node)
        node.set(qn("w:w"),str(v));node.set(qn("w:type"),"dxa")

def shade(cell, fill):
    tcPr=cell._tc.get_or_add_tcPr()
    shd=tcPr.find(qn("w:shd"))
    if shd is None:
        shd=OxmlElement("w:shd");tcPr.append(shd)
    shd.set(qn("w:fill"),fill)

def set_width(cell, cm):
    tcPr=cell._tc.get_or_add_tcPr()
    tcW=tcPr.find(qn("w:tcW"))
    if tcW is None:
        tcW=OxmlElement("w:tcW");tcPr.append(tcW)
    tcW.set(qn("w:w"),str(int(Cm(cm).twips)));tcW.set(qn("w:type"),"dxa")

def no_split(row):
    trPr=row._tr.get_or_add_trPr()
    if trPr.find(qn("w:cantSplit")) is None: trPr.append(OxmlElement("w:cantSplit"))

def set_height(row, cm, exact=True):
    row.height=Cm(cm)
    row.height_rule=WD_ROW_HEIGHT_RULE.EXACTLY if exact else WD_ROW_HEIGHT_RULE.AT_LEAST
    no_split(row)

def style_table(table):
    table.alignment=WD_TABLE_ALIGNMENT.CENTER
    table.autofit=False
    table.style="Table Grid"
    for row in table.rows:
        no_split(row)
        for cell in row.cells:
            set_cell_margins(cell)
            for p in cell.paragraphs:
                p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(0)

def add_title(doc):
    p=doc.add_paragraph()
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after=Pt(5)
    r=p.add_run('2025－2026合成示例内容：通过项目实践展示文档制作与检查流程')
    r.bold=True;r.font.name="方正小标宋简体";r._element.rPr.rFonts.set(qn("w:eastAsia"),"方正小标宋简体");r.font.size=Pt(18)
    p=doc.add_paragraph()
    p.paragraph_format.space_after=Pt(4)
    p.paragraph_format.line_spacing=1
    r=p.add_run('合成示例内容：通过项目实践展示文档制作与检查流程[示例编号]')
    r.font.name="宋体";r._element.rPr.rFonts.set(qn("w:eastAsia"),"宋体");r.font.size=Pt(10.5)

def basic_table(doc):
    data=[
      ["基本情况","姓名",'示例同学',"性别","男","出生年月","2005年10月"],
      ["","政治面貌","共青团员","民族","汉族","入学时间","2024年09月"],
      ["","院系","人工智能与大数据学院","专业","电气工程及其自动化","学制","4年"],
      ["","年级","2024级","班级","24电气工程本科5班","联系电话",'[示例电话]'],
      ["","身份证号",'[示例证件号]',"","","",""],
    ]
    t=doc.add_table(rows=5,cols=7)
    style_table(t)
    widths=[0.85,1.4,3.3,1.15,3.0,1.45,3.1]
    for row in t.rows:
      for c,w in zip(row.cells,widths): set_width(c,w)
    t.cell(0,0).merge(t.cell(4,0))
    t.cell(4,1).merge(t.cell(4,2));t.cell(4,1).merge(t.cell(4,6))
    for ri,row in enumerate(data):
      for ci,txt in enumerate(row):
        if ri==4 and ci not in (0,1): continue
        if ri>0 and ci==0: continue
        label=ci in (0,1,3,5) or (ri==4 and ci==1)
        set_cell_text(t.cell(ri,ci),txt,10,bold=label,align=WD_ALIGN_PARAGRAPH.CENTER if label or ci in (2,4,6) else WD_ALIGN_PARAGRAPH.LEFT)
        if label: shade(t.cell(ri,ci),"F2F2F2")
      set_height(t.rows[ri],0.84 if ri!=2 and ri!=3 else 1.02)
    return t

def study_table(doc):
    t=doc.add_table(rows=2,cols=5);style_table(t)
    widths=[0.85,3.1,3.3,2.75,4.25]
    for row in t.rows:
      for c,w in zip(row.cells,widths): set_width(c,w)
    t.cell(0,0).merge(t.cell(1,0))
    vals=[
      ["学习情况","成绩排名","27/433（名次/总人数）","实行综合考评排名","是"],
      ["","必修课","14门，其中及格以上14门","如是，排名","3/433（名次/总人数）"]
    ]
    for ri,row in enumerate(vals):
      for ci,txt in enumerate(row):
        if ri==1 and ci==0: continue
        label=ci in (0,1,3)
        set_cell_text(t.cell(ri,ci),txt,9.8,bold=label,align=WD_ALIGN_PARAGRAPH.CENTER)
        if label: shade(t.cell(ri,ci),"F2F2F2")
      set_height(t.rows[ri],0.86)
    return t

def awards_table(doc):
    rows=[
      ["主要获奖情况","日期","奖项名称","颁奖单位"],
      ["","2025年12月",'合成示例内容：通过项目实践展示文档制作与检查流程',"全国高等学校计算机教育研究会"],
      ["","2026年7月",'合成示例内容：通过项目实践展示文档制作与检查流程',"中国机器人及人工智能大赛组委会"],
      ["","2026年8月",'“合成示例内容：通过项目实践展示文档制作与检查流程',"共青团广东省委员会等"],
      ["","2025年12月",'合成示例内容：通过项目实践展示文档制作与检查流程',"华教杯全国大学生数学竞赛组委会"]
    ]
    t=doc.add_table(rows=5,cols=4);style_table(t)
    widths=[0.85,1.75,6.45,4.25]
    for row in t.rows:
      for c,w in zip(row.cells,widths): set_width(c,w)
    t.cell(0,0).merge(t.cell(4,0))
    for ri,row in enumerate(rows):
      for ci,txt in enumerate(row):
        if ri>0 and ci==0: continue
        label=ri==0
        set_cell_text(t.cell(ri,ci),txt,9 if ri else 9.8,bold=label,align=WD_ALIGN_PARAGRAPH.CENTER)
        if label: shade(t.cell(ri,ci),"F2F2F2")
      set_height(t.rows[ri],0.75 if ri==0 else 1.12)
    return t

def reason_table(doc):
    t=doc.add_table(rows=1,cols=2);style_table(t)
    set_width(t.cell(0,0),0.85);set_width(t.cell(0,1),12.45)
    set_cell_text(t.cell(0,0),"申请理由\n（200字）",9.5,True,WD_ALIGN_PARAGRAPH.CENTER);shade(t.cell(0,0),"F2F2F2")
    cell=t.cell(0,1);cell.text=""
    p=cell.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY;p.paragraph_format.first_line_indent=Pt(21);p.paragraph_format.line_spacing=1.25
    run=p.add_run(APPLICATION);run.font.name="宋体";run._element.rPr.rFonts.set(qn("w:eastAsia"),"宋体");run.font.size=Pt(10.5)
    p=cell.add_paragraph();p.paragraph_format.space_before=Pt(8);p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    run=p.add_run("申请人签名（手签）：________________");run.font.name="宋体";run._element.rPr.rFonts.set(qn("w:eastAsia"),"宋体");run.font.size=Pt(10)
    p=cell.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    run=p.add_run("年      月      日");run.font.name="宋体";run._element.rPr.rFonts.set(qn("w:eastAsia"),"宋体");run.font.size=Pt(10)
    set_height(t.rows[0],6.35)
    return t

def opinion_table(doc,label,height,body_lines,signature_lines,reason=None):
    t=doc.add_table(rows=1,cols=2);style_table(t)
    set_width(t.cell(0,0),0.9);set_width(t.cell(0,1),12.4)
    set_cell_text(t.cell(0,0),label,9.5,True,WD_ALIGN_PARAGRAPH.CENTER);shade(t.cell(0,0),"F2F2F2")
    cell=t.cell(0,1);cell.text=""
    if reason:
        p=cell.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY;p.paragraph_format.first_line_indent=Pt(21);p.paragraph_format.line_spacing=1.25
        rr=p.add_run(reason);rr.font.name="宋体";rr._element.rPr.rFonts.set(qn("w:eastAsia"),"宋体");rr.font.size=Pt(10.5)
    else:
        cell.paragraphs[0].add_run("")
    for _ in range(body_lines):
        p=cell.add_paragraph();p.paragraph_format.space_after=Pt(0)
    for line in signature_lines:
        p=cell.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.RIGHT;p.paragraph_format.space_after=Pt(0)
        rr=p.add_run(line);rr.font.name="宋体";rr._element.rPr.rFonts.set(qn("w:eastAsia"),"宋体");rr.font.size=Pt(10)
    set_height(t.rows[0],height)
    return t

doc=Document()
sec=doc.sections[0]
sec.page_width=Cm(21);sec.page_height=Cm(29.7)
sec.top_margin=Cm(1.15);sec.bottom_margin=Cm(1.0);sec.left_margin=Cm(1.45);sec.right_margin=Cm(1.45)
sec.header_distance=Cm(0.4);sec.footer_distance=Cm(0.4)
styles=doc.styles
styles["Normal"].font.name="宋体";styles["Normal"]._element.rPr.rFonts.set(qn("w:eastAsia"),"宋体");styles["Normal"].font.size=Pt(10.5)
add_title(doc);basic_table(doc);study_table(doc);awards_table(doc);reason_table(doc)
p=doc.add_page_break();p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(0)
opinion_table(doc,"推荐理由\n（100字）",6.4,2,['合成示例内容：通过项目实践展示文档制作与检查流程________________',"年      月      日"],RECOMMENDATION)
opinion_table(doc,"院\n（系）\n意\n见",8.0,6,['合成示例内容：通过项目实践展示文档制作与检查流程________________',"（院系公章）","年      月      日"])
opinion_table(doc,"学\n校\n意\n见",8.0,1,["（学校公章）","年      月      日"],'合成示例内容：通过项目实践展示文档制作与检查流程')
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.RIGHT;p.paragraph_format.space_before=Pt(3)
rr=p.add_run('合成示例内容：通过项目实践展示文档制作与检查流程');rr.font.name="宋体";rr._element.rPr.rFonts.set(qn("w:eastAsia"),"宋体");rr.font.size=Pt(8.5)
# Preserve fields and print behavior.
settings=doc.settings._element
compat=settings.find(qn("w:compat"))
if compat is None: compat=OxmlElement("w:compat");settings.append(compat)
zoom=settings.find(qn("w:zoom"))
if zoom is not None: zoom.set(qn("w:percent"),"100")
doc.core_properties.title='2025－2026合成示例内容：通过项目实践展示文档制作与检查流程'
doc.core_properties.subject='示例同学 24电气工程本科5班'
doc.core_properties.author='示例同学'
doc.save(FINAL)
print(FINAL)
print("application_chars",len(APPLICATION),"recommendation_chars",len(RECOMMENDATION))

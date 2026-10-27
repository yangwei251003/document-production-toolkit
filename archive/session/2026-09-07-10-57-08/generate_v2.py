# Sanitized session source; synthetic fixture values and explicit execution gate.
"""
主生成器 - 单一文件，整合所有逻辑
"""
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-07-10-57-08/generate_v2.py')
import zipfile
import os
import shutil
from lxml import etree

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC_NS = "http://schemas.openxmlformats.org/drawingml/2006/picture"
WP_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"

XML_NS = "http://www.w3.org/XML/1998/namespace"

def w(tag): return f"{{{W_NS}}}{tag}"
def r(tag): return f"{{{R_NS}}}{tag}"

WORKSPACE = session_path('input_26')
TEMPLATE = f"{WORKSPACE}/template_base.docx"
LOGO_DIR = f"{WORKSPACE}/logo_assets"
NEW_LOGO = f"{LOGO_DIR}/mei_logo.png"

UNPACK_DIR = f"{WORKSPACE}/unpacked"
OUTPUT_DOCX = f"{WORKSPACE}/output_generated.docx"


# ============================================================
# Step 1: 解压模板
# ============================================================
def unpack_template():
    if os.path.exists(UNPACK_DIR):
        shutil.rmtree(UNPACK_DIR)
    os.makedirs(UNPACK_DIR)
    with zipfile.ZipFile(TEMPLATE, 'r') as z:
        z.extractall(UNPACK_DIR)
    print(f"Unpacked template to {UNPACK_DIR}")


# ============================================================
# Step 2: 替换页眉第4个logo (image4.png) 为用户的梅你不行队
# ============================================================
def replace_header_logo():
    target = f"{UNPACK_DIR}/word/media/image4.png"
    shutil.copy(NEW_LOGO, target)
    print(f"Replaced image4.png with {NEW_LOGO}")


# ============================================================
# Step 2b: 复制第一篇封面的团队大标识作为封面顶部logo
# ============================================================
COVER_LOGO_SRC = session_path('input_27.png')

def add_cover_logo():
    fixture_value('texts.b38d32a6_1')
    dst_media = f"{UNPACK_DIR}/word/media/image32.png"
    shutil.copy(COVER_LOGO_SRC, dst_media)
    # 在 document.xml.rels 添加关系（字符串操作，保持原格式）
    rels_path = f"{UNPACK_DIR}/word/_rels/document.xml.rels"
    with open(rels_path, 'r', encoding='utf-8') as f:
        rels_content = f.read()
    # 找到已有最大 rId 数字
    import re
    ids = re.findall(r'Id="rId(\d+)"', rels_content)
    max_id = max(int(i) for i in ids)
    new_rid = f"rId{max_id + 1}"
    new_rel = (
        f'<Relationship Id="{new_rid}" '
        f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
        f'Target="media/image32.png"/>'
    )
    # 在 </Relationships> 前插入
    rels_content = rels_content.replace('</Relationships>', new_rel + '</Relationships>')
    with open(rels_path, 'w', encoding='utf-8') as f:
        f.write(rels_content)
    print(f"Added cover logo as image32.png, rId={new_rid}")
    return new_rid


# ============================================================
# Step 2c: 提取原报告的 7 张正文图片并注册关系
# ============================================================
REPORT_IMAGES_DIR = session_path('input_28')

# 图片配置：(源文件名, 图号, 原宽EMU, 原高EMU)
REPORT_IMAGE_CONFIG = fixture_value('tables.table_3')

# 最大显示宽度（EMU）：5.5 英寸，适配 A4 页（左右 1.25" 边距）
MAX_IMG_WIDTH_EMU = int(5.5 * 914400)


def add_report_images():
    fixture_value('texts.b38d32a6_2')
    import re
    # 新文件名映射（避免与模板已有 image1-31 冲突）
    new_names = {
        "image2.png":  "image33.png",
        "image3.png":  "image34.png",
        "image4.jpeg": "image35.jpeg",
        "image5.jpeg": "image36.jpeg",
        "image6.jpeg": "image37.jpeg",
        "image7.jpeg": "image38.jpeg",
        "image8.jpeg": "image39.jpeg",
    }
    # 复制图片
    for src_name, new_name in new_names.items():
        src = f"{REPORT_IMAGES_DIR}/{src_name}"
        dst = f"{UNPACK_DIR}/word/media/{new_name}"
        if os.path.exists(src):
            shutil.copy(src, dst)
        else:
            print(f"警告：图片不存在 {src}")

    # 注册关系（字符串方式）
    rels_path = f"{UNPACK_DIR}/word/_rels/document.xml.rels"
    with open(rels_path, 'r', encoding='utf-8') as f:
        rels_content = f.read()
    ids = re.findall(r'Id="rId(\d+)"', rels_content)
    max_id = max(int(i) for i in ids)

    result = {}
    new_rel_entries = []
    next_id = max_id + 1
    for src_name, fig, cx_orig, cy_orig in REPORT_IMAGE_CONFIG:
        new_name = new_names[src_name]
        rid = f"rId{next_id}"
        # 缩放：宽度超限则等比缩小
        if cx_orig > MAX_IMG_WIDTH_EMU:
            scale = MAX_IMG_WIDTH_EMU / cx_orig
            cx = MAX_IMG_WIDTH_EMU
            cy = int(cy_orig * scale)
        else:
            cx = cx_orig
            cy = cy_orig
        new_rel_entries.append(
            f'<Relationship Id="{rid}" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="media/{new_name}"/>'
        )
        result[fig] = (rid, cx, cy)
        next_id += 1

    rels_content = rels_content.replace('</Relationships>', ''.join(new_rel_entries) + '</Relationships>')
    with open(rels_path, 'w', encoding='utf-8') as f:
        f.write(rels_content)
    print(f"Added 7 report images, rIds rId{max_id+1}..rId{next_id-1}")
    return result


# ============================================================
# Step 3: 解析 document.xml
# ============================================================
def load_document():
    doc_path = f"{UNPACK_DIR}/word/document.xml"
    with open(doc_path, 'rb') as f:
        tree = etree.parse(f)
    root = tree.getroot()
    body = root.find(w('body'))
    if body is None:
        raise RuntimeError("No <w:body> found")
    # 保存含 headerReference 的 sectPr（第一个 section 的页面设置，含 4 logo 页眉）
    saved_sectPr = None
    all_sectPrs = root.findall('.//' + w('sectPr'))
    for sp in all_sectPrs:
        if sp.find(w('headerReference')) is not None:
            saved_sectPr = etree.fromstring(etree.tostring(sp))  # 深拷贝
            break
    if saved_sectPr is None and all_sectPrs:
        saved_sectPr = etree.fromstring(etree.tostring(all_sectPrs[0]))
    # 清空 body（删除所有段落和表格）
    for child in list(body):
        body.remove(child)
    return root, body, saved_sectPr


# ============================================================
# Helper functions for building content
# ============================================================

def set_default_run(rPr, *, font=None, size=None, bold=False, italic=False, color=None):
    if font:
        etree.SubElement(rPr, w('rFonts'),
                         {w('ascii'): font, w('hAnsi'): font, w('eastAsia'): font})
    if size is not None:
        v = str(size * 2)
        etree.SubElement(rPr, w('sz'), {w('val'): v})
        etree.SubElement(rPr, w('szCs'), {w('val'): v})
    if bold:
        etree.SubElement(rPr, w('b'))
        etree.SubElement(rPr, w('bCs'))
    if italic:
        etree.SubElement(rPr, w('i'))
        etree.SubElement(rPr, w('iCs'))
    if color:
        etree.SubElement(rPr, w('color'), {w('val'): color})


def make_run(text, *, size=12, font_ea="宋体", font_la="Times New Roman", bold=False, italic=False, color=None):
    r_el = etree.Element(w('r'))
    rPr = etree.SubElement(r_el, w('rPr'))
    # OOXML 顺序：rFonts → b/bCs → i/iCs → color → sz/szCs
    etree.SubElement(rPr, w('rFonts'),
                     {w('ascii'): font_la, w('hAnsi'): font_la, w('eastAsia'): font_ea})
    if bold:
        etree.SubElement(rPr, w('b'))
        etree.SubElement(rPr, w('bCs'))
    if italic:
        etree.SubElement(rPr, w('i'))
        etree.SubElement(rPr, w('iCs'))
    if color:
        etree.SubElement(rPr, w('color'), {w('val'): color})
    v = str(int(size * 2))
    etree.SubElement(rPr, w('sz'), {w('val'): v})
    etree.SubElement(rPr, w('szCs'), {w('val'): v})
    t = etree.SubElement(r_el, w('t'))
    t.set(f'{{{XML_NS}}}space', 'preserve')
    t.text = text
    return r_el


def make_image_para(rId, *, cx_emu, cy_emu, align="center", descr="图片"):
    fixture_value('texts.b38d32a6_3')
    drawing_xml = (
        '<w:drawing xmlns:w="{W}" xmlns:wp="{WP}" xmlns:a="{A}" xmlns:pic="{PIC}" xmlns:r="{R}">'
        '<wp:inline distT="0" distB="0" distL="114300" distR="114300">'
        '<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:docPr id="900" name="{descr}" descr="{descr}"/>'
        '<wp:cNvGraphicFramePr>'
        '<a:graphicFrameLocks noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic>'
        '<a:graphicData uri="{PIC}">'
        '<pic:pic>'
        '<pic:nvPicPr>'
        '<pic:cNvPr id="900" name="{descr}" descr="{descr}"/>'
        '<pic:cNvPicPr>'
        '<a:picLocks noChangeAspect="1"/>'
        '</pic:cNvPicPr>'
        '</pic:nvPicPr>'
        '<pic:blipFill>'
        '<a:blip r:embed="{rId}"/>'
        '<a:stretch><a:fillRect/></a:stretch>'
        '</pic:blipFill>'
        '<pic:spPr>'
        '<a:xfrm>'
        '<a:off x="0" y="0"/>'
        '<a:ext cx="{cx}" cy="{cy}"/>'
        '</a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        '</pic:spPr>'
        '</pic:pic>'
        '</a:graphicData>'
        '</a:graphic>'
        '</wp:inline>'
        '</w:drawing>'
    ).format(
        W=W_NS, WP=WP_NS, A=A_NS, PIC=PIC_NS, R=R_NS,
        cx=cx_emu, cy=cy_emu, descr=descr, rId=rId
    )
    drawing_el = etree.fromstring(drawing_xml)

    p = etree.Element(w('p'))
    pPr = etree.SubElement(p, w('pPr'))
    etree.SubElement(pPr, w('jc'), {w('val'): align})
    etree.SubElement(pPr, w('spacing'),
                     {w('after'): '0', w('line'): '360', w('lineRule'): 'auto'})
    r_el = etree.SubElement(p, w('r'))
    r_el.append(drawing_el)
    return p


def make_p(*, align=None, line=None, after=None, before=None, indent=None,
           page_break_before=False, runs=None, text=None,
           size=12, font_ea="宋体", bold=False, italic=False, color=None,
           border_below=None):
    p = etree.Element(w('p'))
    pPr = etree.SubElement(p, w('pPr'))
    # OOXML pPr 顺序：pageBreakBefore → ... → pBdr → ... → spacing → ind → jc
    if page_break_before:
        etree.SubElement(pPr, w('pageBreakBefore'))
    if border_below:
        bdr = etree.SubElement(pPr, w('pBdr'))
        etree.SubElement(bdr, w('bottom'), border_below)
    if before is not None or after is not None or line is not None:
        attrs = {}
        if before is not None: attrs[w('before')] = str(before)
        if after is not None: attrs[w('after')] = str(after)
        if line is not None:
            attrs[w('line')] = str(line)
            attrs[w('lineRule')] = 'auto'
        etree.SubElement(pPr, w('spacing'), attrs)
    if indent:
        etree.SubElement(pPr, w('ind'), {w(k): str(v) for k, v in indent.items()})
    if align:
        etree.SubElement(pPr, w('jc'), {w('val'): align})
    if text is not None:
        p.append(make_run(text, size=size, font_ea=font_ea, bold=bold, italic=italic, color=color))
    elif runs:
        for run_text, kw in runs:
            p.append(make_run(run_text, **kw))
    return p


def add_to_body(body, element):
    body.append(element)


def page_break(body):
    p = etree.Element(w('p'))
    r_el = etree.SubElement(p, w('r'))
    etree.SubElement(r_el, w('br'), {w('type'): 'page'})
    body.append(p)
    return p


def make_table(rows, *, col_widths, total_width, header_color="D9E2F3"):
    tbl = etree.Element(w('tbl'))
    tblPr = etree.SubElement(tbl, w('tblPr'))
    etree.SubElement(tblPr, w('tblW'),
                     {w('w'): str(total_width), w('type'): 'dxa'})
    etree.SubElement(tblPr, w('jc'), {w('val'): 'center'})
    borders = etree.SubElement(tblPr, w('tblBorders'))
    for side in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        etree.SubElement(borders, w(side),
                         {w('val'): 'single', w('sz'): '4', w('space'): '0', w('color'): '808080'})
    tblGrid = etree.SubElement(tbl, w('tblGrid'))
    for cw in col_widths:
        etree.SubElement(tblGrid, w('gridCol'), {w('w'): str(cw)})

    for ri, row in enumerate(rows):
        tr = etree.SubElement(tbl, w('tr'))
        for ci, cell_text in enumerate(row):
            tc = etree.SubElement(tr, w('tc'))
            tcPr = etree.SubElement(tc, w('tcPr'))
            etree.SubElement(tcPr, w('tcW'),
                             {w('w'): str(col_widths[ci]), w('type'): 'dxa'})
            if ri == 0:
                etree.SubElement(tcPr, w('shd'),
                                 {w('val'): 'clear', w('color'): 'auto', w('fill'): header_color})
            etree.SubElement(tcPr, w('vAlign'), {w('val'): 'center'})
            cp = etree.SubElement(tc, w('p'))
            cpPr = etree.SubElement(cp, w('pPr'))
            etree.SubElement(cpPr, w('spacing'),
                             {w('after'): '0', w('before'): '0',
                              w('line'): '300', w('lineRule'): 'auto'})
            etree.SubElement(cpPr, w('jc'),
                             {w('val'): 'center' if ri == 0 else 'left'})
            cr = etree.SubElement(cp, w('r'))
            crPr = etree.SubElement(cr, w('rPr'))
            etree.SubElement(crPr, w('rFonts'),
                             {w('ascii'): "Times New Roman", w('hAnsi'): "Times New Roman", w('eastAsia'): "宋体"})
            if ri == 0:
                etree.SubElement(crPr, w('b'))
                etree.SubElement(crPr, w('bCs'))
            etree.SubElement(crPr, w('sz'), {w('val'): '21'})
            etree.SubElement(crPr, w('szCs'), {w('val'): '21'})
            ct = etree.SubElement(cr, w('t'))
            ct.set(f'{{{XML_NS}}}space', 'preserve')
            ct.text = cell_text
    return tbl


# ============================================================
# Section builders
# ============================================================

def build_cover(body, logo_rId=None):
    # 顶部留白
    for _ in range(2):
        body.append(make_p(line=360, align="left"))

    # 顶部团队大标识（居中）
    if logo_rId:
        # 1.65 x 1.65 英寸 = 1508760 EMU (1 inch = 914400 EMU)
        size_emu = int(1.65 * 914400)
        body.append(make_image_para(logo_rId, cx_emu=size_emu, cy_emu=size_emu, align="center", descr="梅你不行实践队标识"))

    # 留白
    body.append(make_p(line=360, align="left"))

    # 主标题
    body.append(make_p(
        align="center", before=0, after=120, line=360,
        text='合成示例段落：用于验证文档布局与内容转换流程',
        size=20, font_ea="黑体", bold=True
    ))

    # 副标题
    body.append(make_p(
        align="center", before=0, after=120, line=360,
        text='——合成示例段落：用于验证文档布局与内容转换流程',
        size=16, font_ea="黑体", bold=True
    ))

    # 主标题2（活动名称，两行用 <w:br/> 分隔）
    p = etree.Element(w('p'))
    pPr = etree.SubElement(p, w('pPr'))
    etree.SubElement(pPr, w('jc'), {w('val'): 'center'})
    etree.SubElement(pPr, w('spacing'),
                     {w('after'): '120', w('line'): '360', w('lineRule'): 'auto'})
    r1 = etree.SubElement(p, w('r'))
    rPr1 = etree.SubElement(r1, w('rPr'))
    etree.SubElement(rPr1, w('rFonts'),
                     {w('ascii'): "Times New Roman", w('hAnsi'): "Times New Roman", w('eastAsia'): "黑体"})
    etree.SubElement(rPr1, w('b'))
    etree.SubElement(rPr1, w('bCs'))
    etree.SubElement(rPr1, w('sz'), {w('val'): '32'})
    etree.SubElement(rPr1, w('szCs'), {w('val'): '32'})
    t1 = etree.SubElement(r1, w('t'))
    t1.set(f'{{{XML_NS}}}space', 'preserve')
    t1.text = "2026年暑期“三下乡”社会实践"
    etree.SubElement(r1, w('br'))
    r2 = etree.SubElement(p, w('r'))
    rPr2 = etree.SubElement(r2, w('rPr'))
    etree.SubElement(rPr2, w('rFonts'),
                     {w('ascii'): "Times New Roman", w('hAnsi'): "Times New Roman", w('eastAsia'): "黑体"})
    etree.SubElement(rPr2, w('b'))
    etree.SubElement(rPr2, w('bCs'))
    etree.SubElement(rPr2, w('sz'), {w('val'): '32'})
    etree.SubElement(rPr2, w('szCs'), {w('val'): '32'})
    t2 = etree.SubElement(r2, w('t'))
    t2.set(f'{{{XML_NS}}}space', 'preserve')
    t2.text = "调研报告"
    body.append(p)

    # 留白
    for _ in range(2):
        body.append(make_p(line=240, align="left"))

    # 团队信息
    info_lines = [
        '合成示例段落：用于验证文档布局与内容转换流程',
        "　　　　　杨主新（专业老师）",
        "　　　　　杨小凤（思政老师）",
        "",
        '团队负责人：示例同学',
        '合成示例段落：用于验证文档布局与内容转换流程',
        '合成示例段落：用于验证文档布局与内容转换流程',
        '合成示例段落：用于验证文档布局与内容转换流程',
        '合成示例段落：用于验证文档布局与内容转换流程',
        "",
        '合成示例段落：用于验证文档布局与内容转换流程',
    ]
    for txt in info_lines:
        if txt:
            body.append(make_p(
                align="left", line=360,
                indent={"left": "1800"},
                text=txt, size=14
            ))
        else:
            body.append(make_p(line=240, align="left"))

    # 实践时间（靠右下）
    body.append(make_p(
        align="right", line=360,
        indent={"right": "1800"},
        text='合成示例段落：用于验证文档布局与内容转换流程',
        size=14
    ))


def section_title(body, text, *, size=18):
    body.append(make_p(
        align="center", before=240, after=240, line=360,
        text=text, size=size, font_ea="黑体", bold=True, color="1F4E79"
    ))


def subsection_title(body, text, *, level=2):
    if level == 2:
        size = 14
        color = "1F4E79"
    else:
        size = 12
        color = "2E75B6"
    body.append(make_p(
        align="left", before=180, after=120, line=360,
        text=text, size=size, font_ea="黑体", bold=True, color=color
    ))


def body_para(body, text, *, indent=True, size=12, line=360):
    ind = {"firstLineChars": "0", "firstLine": "480"} if indent else None
    body.append(make_p(
        align="both", after=0, line=line,
        indent=ind,
        text=text, size=size
    ))


def caption(body, text):
    body.append(make_p(
        align="center", before=60, after=180, line=300,
        text=text, size=10.5, font_ea="楷体", italic=True
    ))


def centered_title(body, text, *, size=18, after=240):
    body.append(make_p(
        align="center", before=0, after=after, line=360,
        text=text, size=size, font_ea="黑体", bold=True, color="1F4E79"
    ))


# ============================================================
# Content blocks
# ============================================================

def build_abstract(body):
    page_break(body)
    centered_title(body, "摘 要", size=18)
    body_para(body,
        fixture_value('texts.b38d32a6_5'),
        indent=False)
    body_para(body,
        fixture_value('texts.b38d32a6_6'),
        indent=False)
    body_para(body,
        fixture_value('texts.b38d32a6_7'),
        indent=False)
    body_para(body,
        fixture_value('texts.b38d32a6_8'),
        indent=False)
    p = etree.Element(w('p'))
    pPr = etree.SubElement(p, w('pPr'))
    etree.SubElement(pPr, w('spacing'), {w('before'): '180', w('after'): '0', w('line'): '360', w('lineRule'): 'auto'})
    etree.SubElement(pPr, w('jc'), {w('val'): 'left'})
    p.append(make_run("关键词：", size=12, font_ea="黑体", bold=True))
    p.append(make_run(
        fixture_value('texts.b38d32a6_76'),
        size=12, font_ea="宋体"))
    body.append(p)


def build_toc(body):
    page_break(body)
    centered_title(body, "目  录", size=18)
    items = [
        "一、绪论",
        "　　1.1 实践背景",
        "　　1.2 调研思路与目标",
        "二、政策与文献依据",
        "三、调研对象与研究方法",
        "　　3.1 案例边界与材料",
        "　　3.2 数据构建与口径",
        "　　3.3 研究伦理",
        "四、五日实践与数据呈现",
        '\u3000\u30004.1 合成示例段落：用于验证文档布局与内容转换流程',
        '\u3000\u30004.2 合成示例段落：用于验证文档布局与内容转换流程',
        "　　4.3 作品与个体表达",
        "　　4.4 课程表之外的安全与陪伴",
        "五、核心发现",
        '\u3000\u30005.1 合成示例段落：用于验证文档布局与内容转换流程',
        '\u3000\u30005.2 合成示例段落：用于验证文档布局与内容转换流程',
        "　　5.3 大学生志愿者的优势与边界",
        '\u3000\u30005.4 合成示例段落：用于验证文档布局与内容转换流程',
        "六、问题与原因分析",
        '合成示例段落：用于验证文档布局与内容转换流程',
        "　　7.1 三阶分龄适配",
        "　　7.2 七模块课程库",
        "　　7.3 五步服务闭环",
        "　　7.4 安全 SOP",
        "八、实践价值",
        "九、结论与反思",
        "参考文献",
        "附录：证据与数据说明",
    ]
    for it in items:
        body_para(body, it, indent=False)


def build_section_1(body):
    page_break(body)
    section_title(body, "一、绪论")
    subsection_title(body, "1.1 实践背景")
    body_para(body,
        fixture_value('texts.b38d32a6_9'))
    body_para(body,
        fixture_value('texts.b38d32a6_10'))
    body_para(body,
        fixture_value('texts.b38d32a6_11'))

    subsection_title(body, "1.2 调研思路与目标")
    body_para(body, '合成示例段落：用于验证文档布局与内容转换流程')
    bullets = [
        fixture_value('texts.b38d32a6_12'),
        fixture_value('texts.b38d32a6_13'),
        fixture_value('texts.b38d32a6_14'),
        fixture_value('texts.b38d32a6_15'),
    ]
    for b in bullets:
        body.append(make_p(
            align="left", after=0, line=360,
            indent={"left": "720", "hanging": "360"},
            text=b, size=11
        ))
    body_para(body,
        fixture_value('texts.b38d32a6_16'))


def build_section_2(body):
    page_break(body)
    section_title(body, "二、政策与文献依据")
    body_para(body,
        fixture_value('texts.b38d32a6_17'))
    body_para(body,
        fixture_value('texts.b38d32a6_18'))
    body_para(body,
        fixture_value('texts.b38d32a6_19'))
    body_para(body,
        fixture_value('texts.b38d32a6_20'))


def build_section_3(body):
    page_break(body)
    section_title(body, "三、调研对象与研究方法")
    subsection_title(body, "3.1 案例边界与材料")
    body_para(body,
        fixture_value('texts.b38d32a6_21'))
    body_para(body,
        fixture_value('texts.b38d32a6_22'))
    subsection_title(body, "3.2 数据构建与口径")
    body_para(body, '合成示例段落：用于验证文档布局与内容转换流程')
    rows = fixture_value('tables.table_4')
    body.append(make_table(rows, col_widths=[1800, 2400, 1200, 4000], total_width=9400))
    caption(body, '合成示例段落：用于验证文档布局与内容转换流程')
    body_para(body,
        fixture_value('texts.b38d32a6_23'))
    subsection_title(body, "3.3 研究伦理")
    body_para(body,
        fixture_value('texts.b38d32a6_24'))


def build_section_4(body, img_rids=None):
    fixture_value('texts.b38d32a6_4')
    if img_rids is None:
        img_rids = {}
    def add_img(fig, descr):
        if fig in img_rids:
            rid, cx, cy = img_rids[fig]
            body.append(make_image_para(rid, cx_emu=cx, cy_emu=cy, align="center", descr=descr))
    page_break(body)
    section_title(body, "四、五日实践与数据呈现")
    subsection_title(body, '4.1 合成示例段落：用于验证文档布局与内容转换流程')
    body_para(body,
        fixture_value('texts.b38d32a6_25'))
    body_para(body,
        fixture_value('texts.b38d32a6_26'))
    add_img("图 1", "五日课程/服务单元主类别结构")
    caption(body, fixture_value('texts.b38d32a6_27'))

    subsection_title(body, '4.2 合成示例段落：用于验证文档布局与内容转换流程')
    body_para(body,
        fixture_value('texts.b38d32a6_28'))
    body_para(body,
        fixture_value('texts.b38d32a6_29'))
    add_img("图 2", '合成示例段落：用于验证文档布局与内容转换流程')
    caption(body, fixture_value('texts.b38d32a6_30'))
    add_img("图 3", '合成示例段落：用于验证文档布局与内容转换流程')
    caption(body, fixture_value('texts.b38d32a6_31'))
    add_img("图 4", "儿童展示完成的剪纸作品")
    caption(body, fixture_value('texts.b38d32a6_32'))

    subsection_title(body, "4.3 作品与个体表达")
    body_para(body,
        fixture_value('texts.b38d32a6_33'))
    body_para(body,
        fixture_value('texts.b38d32a6_34'))
    add_img("图 5", "多名儿童展示自然材料创作")
    caption(body, fixture_value('texts.b38d32a6_35'))

    subsection_title(body, "4.4 课程表之外的安全与陪伴")
    body_para(body,
        fixture_value('texts.b38d32a6_36'))
    body_para(body,
        fixture_value('texts.b38d32a6_37'))
    body_para(body,
        fixture_value('texts.b38d32a6_38'))
    add_img("图 6", "队员处理儿童腿部擦伤")
    caption(body, fixture_value('texts.b38d32a6_39'))
    add_img("图 7", "一对一作业辅导")
    caption(body, '合成示例段落：用于验证文档布局与内容转换流程')


def build_section_5(body):
    page_break(body)
    section_title(body, "五、核心发现")
    subsection_title(body, '5.1 合成示例段落：用于验证文档布局与内容转换流程')
    body_para(body,
        fixture_value('texts.b38d32a6_40'))
    body_para(body,
        fixture_value('texts.b38d32a6_41'))
    subsection_title(body, '5.2 合成示例段落：用于验证文档布局与内容转换流程')
    body_para(body,
        fixture_value('texts.b38d32a6_42'))
    body_para(body,
        fixture_value('texts.b38d32a6_43'))
    subsection_title(body, '5.3 合成示例段落：用于验证文档布局与内容转换流程')
    body_para(body,
        fixture_value('texts.b38d32a6_44'))
    body_para(body,
        fixture_value('texts.b38d32a6_45'))
    subsection_title(body, '5.4 合成示例段落：用于验证文档布局与内容转换流程')
    body_para(body,
        fixture_value('texts.b38d32a6_46'))
    body_para(body,
        fixture_value('texts.b38d32a6_47'))


def build_section_6(body):
    page_break(body)
    section_title(body, "六、问题与原因分析")
    body_para(body,
        fixture_value('texts.b38d32a6_48'))
    rows = fixture_value('tables.table_5')
    body.append(make_table(rows, col_widths=[2200, 2400, 2200, 2600], total_width=9400))
    caption(body, '合成示例段落：用于验证文档布局与内容转换流程')
    body_para(body,
        fixture_value('texts.b38d32a6_49'))


def build_section_7(body):
    page_break(body)
    section_title(body, '合成示例段落：用于验证文档布局与内容转换流程')
    body_para(body,
        fixture_value('texts.b38d32a6_50'))
    subsection_title(body, "7.1 三阶分龄适配")
    body_para(body,
        fixture_value('texts.b38d32a6_51'))
    body_para(body, '合成示例段落：用于验证文档布局与内容转换流程', indent=False)
    body_para(body, '合成示例段落：用于验证文档布局与内容转换流程', indent=False)
    body_para(body, '合成示例段落：用于验证文档布局与内容转换流程', indent=False)
    body_para(body,
        fixture_value('texts.b38d32a6_52'))

    subsection_title(body, "7.2 七模块课程库")
    body_para(body,
        fixture_value('texts.b38d32a6_53'))
    rows = fixture_value('tables.table_6')
    body.append(make_table(rows, col_widths=[1500, 2800, 2500, 2600], total_width=9400))
    caption(body, fixture_value('texts.b38d32a6_54'))
    body_para(body,
        fixture_value('texts.b38d32a6_55'))

    subsection_title(body, "7.3 五步服务闭环")
    body_para(body,
        fixture_value('texts.b38d32a6_56'))
    rows = fixture_value('tables.table_7')
    body.append(make_table(rows, col_widths=[1500, 1900, 3500, 2500], total_width=9400))
    caption(body, '合成示例段落：用于验证文档布局与内容转换流程')
    body_para(body,
        fixture_value('texts.b38d32a6_57'))

    subsection_title(body, "7.4 安全 SOP")
    body_para(body,
        fixture_value('texts.b38d32a6_58'))
    body_para(body,
        fixture_value('texts.b38d32a6_59'))


def build_section_8(body):
    page_break(body)
    section_title(body, "八、实践价值")
    body_para(body,
        fixture_value('texts.b38d32a6_60'))
    body_para(body,
        fixture_value('texts.b38d32a6_61'))
    body_para(body,
        fixture_value('texts.b38d32a6_62'))
    body_para(body,
        fixture_value('texts.b38d32a6_63'))
    body_para(body,
        fixture_value('texts.b38d32a6_64'))


def build_section_9(body):
    page_break(body)
    section_title(body, "九、结论与反思")
    body_para(body,
        fixture_value('texts.b38d32a6_65'))
    body_para(body,
        fixture_value('texts.b38d32a6_66'))
    body_para(body,
        fixture_value('texts.b38d32a6_67'))
    body_para(body,
        fixture_value('texts.b38d32a6_68'))


def build_references(body):
    page_break(body)
    centered_title(body, "参考文献")
    refs = [
        fixture_value('texts.b38d32a6_69'),
        fixture_value('texts.b38d32a6_70'),
        fixture_value('texts.b38d32a6_71'),
        fixture_value('texts.b38d32a6_72'),
        fixture_value('texts.b38d32a6_73'),
        "[6] Mahoney, Parente, & Lord (2007). After-School Program Engagement: Links to Child Competence and Program Quality and Content.",
        "[7] Roth, Malone, & Brooks-Gunn (2010). Does the Amount of Participation in Afterschool Programs Relate to Developmental Outcomes?",
        "[8] Levine et al. (2025). Promising Practices of Out-of-School Time Programs for Low-Income Adolescents.",
        "[9] Escartí et al. (2020). Teaching personal and social responsibility after school: A systematic review.",
    ]
    for r_ in refs:
        body.append(make_p(
            align="left", after=0, line=360,
            indent={"firstLineChars": "0", "left": "0", "hanging": "480"},
            text=r_, size=10.5
        ))


def build_appendix(body):
    page_break(body)
    centered_title(body, "附录：证据与数据说明")
    body_para(body,
        fixture_value('texts.b38d32a6_74'),
        indent=False)
    body_para(body,
        fixture_value('texts.b38d32a6_75'),
        indent=False)


# ============================================================
# Finalize document (write back to disk)
# ============================================================

def finalize_document(root, body, saved_sectPr):
    # 把保存的 sectPr（第一个 section，含 header/footer 引用）放到 body 末尾
    if saved_sectPr is not None:
        body.append(etree.fromstring(etree.tostring(saved_sectPr)))
    else:
        # 兜底：手动构造
        sectPr = etree.SubElement(body, w('sectPr'))
        hr = etree.SubElement(sectPr, w('headerReference'))
        hr.set(w('type'), 'default')
        hr.set(r('id'), 'rId3')
        fr = etree.SubElement(sectPr, w('footerReference'))
        fr.set(w('type'), 'default')
        fr.set(r('id'), 'rId4')
        pgsz = etree.SubElement(sectPr, w('pgSz'))
        pgsz.set(w('w'), '11906')
        pgsz.set(w('h'), '16838')
        pgmar = etree.SubElement(sectPr, w('pgMar'))
        pgmar.set(w('top'), '1440')
        pgmar.set(w('right'), '1803')
        pgmar.set(w('bottom'), '1440')
        pgmar.set(w('left'), '1803')
        pgmar.set(w('header'), '720')
        pgmar.set(w('footer'), '720')
        pgmar.set(w('gutter'), '0')
        cols = etree.SubElement(sectPr, w('cols'))
        cols.set(w('space'), '720')
        cols.set(w('num'), '1')
        docGrid = etree.SubElement(sectPr, w('docGrid'))
        docGrid.set(w('linePitch'), '360')
        docGrid.set(w('charSpace'), '0')

    doc_path = f"{UNPACK_DIR}/word/document.xml"
    xml_str = etree.tostring(root, pretty_print=False, encoding='UTF-8',
                              standalone=True, xml_declaration=True)
    with open(doc_path, 'wb') as f:
        f.write(xml_str)
    print(f"Wrote document.xml ({len(xml_str)} bytes)")


def repack_docx():
    # 直接覆盖写入（zipfile 'w' 模式自动覆盖，无需先删除）
    with zipfile.ZipFile(OUTPUT_DOCX, 'w', zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirs, files in os.walk(UNPACK_DIR):
            for fn in files:
                fp = os.path.join(dirpath, fn)
                arcname = os.path.relpath(fp, UNPACK_DIR).replace(os.sep, '/')
                z.write(fp, arcname)
    print(f"Generated: {OUTPUT_DOCX}")
    print(f"Size: {os.path.getsize(OUTPUT_DOCX)} bytes")


# ============================================================
# Main
# ============================================================
def main():
    unpack_template()
    replace_header_logo()
    cover_logo_rId = add_cover_logo()
    img_rids = add_report_images()
    root, body, saved_sectPr = load_document()

    # Cover
    build_cover(body, logo_rId=cover_logo_rId)
    page_break(body)
    # Abstract
    build_abstract(body)
    # TOC
    build_toc(body)
    # Sections
    build_section_1(body)
    build_section_2(body)
    build_section_3(body)
    build_section_4(body, img_rids=img_rids)
    build_section_5(body)
    build_section_6(body)
    build_section_7(body)
    build_section_8(body)
    build_section_9(body)
    # References
    build_references(body)
    # Appendix
    build_appendix(body)

    finalize_document(root, body, saved_sectPr)
    repack_docx()
    print("DONE.")


if __name__ == "__main__":
    main()

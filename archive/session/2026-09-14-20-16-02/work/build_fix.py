# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-14-20-16-02/work/build_fix.py')
# -*- coding: utf-8 -*-
fixture_value('texts.3534730e_1')
import zipfile, re, os, struct
from xml.etree import ElementTree as ET

SRC = session_path('input_10.xlsx')
OUTDIR = session_path('input_11')
OUT = os.path.join(OUTDIR, "26电气工程本科8班花名册_图片修复版.xlsx")
PHOTODIR = os.path.join(OUTDIR, "学生相册_照片导出")

M = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
zin = zipfile.ZipFile(SRC)

# ---------- 1. sharedStrings ----------
sroot = ET.fromstring(zin.read('xl/sharedStrings.xml'))
strings = []
for si in sroot.findall(M + 'si'):
    strings.append(''.join(t.text or '' for t in si.iter(M + 't')))

s3 = zin.read('xl/worksheets/sheet3.xml').decode('utf-8')

# ---------- 2. vm 单元格 -> 位置 ----------
COLIDX = {'A': 0, 'C': 2, 'E': 4, 'G': 6}
CELL_W_CHARS = 18.875

ROW_H = {}
for m in re.finditer(r'<row\s[^>]*>', s3):
    tag = m.group(0)
    rm = re.match(r'<row\s+r="(\d+)"', tag)
    hm = re.search(r'\sht="([\d.]+)"', tag)
    if rm:
        ROW_H[int(rm.group(1))] = float(hm.group(1)) if hm else 14.25
assert ROW_H.get(2) == 152.1, "行高解析异常: %s" % ROW_H.get(2)

vm_cells = re.findall(r'<c r="([A-Z]+\d+)"[^>]*vm="(\d+)"[^>]*>', s3)
print("检测到图片单元格:", len(vm_cells))


def cellstr(col, row):
    m = re.search(r'<c r="%s%d"[^>]*t="s"[^>]*><v>(\d+)</v>' % (col, row), s3)
    return strings[int(m.group(1))] if m else ''


students = []
for i, (ref, vm) in enumerate(vm_cells):
    mm = re.match(r'([A-Z]+)(\d+)', ref)
    col, row = mm.group(1), int(mm.group(2))
    name_raw = cellstr(col, row + 1)
    name = re.sub(r'^姓名[:：]\s*', '', name_raw).strip()
    students.append(dict(idx=i + 1, vm=int(vm), ref=ref, col=col, row=row,
                         name=name, tel=cellstr(col, row + 2),
                         dorm=cellstr(col, row + 3)))
for s in students[:8]:
    print("  ", s['idx'], s['ref'], '->image%d.png' % s['vm'], s['name'], '|', s['tel'])
print("   ... 共", len(students), "位学生")


# ---------- 3. 图片像素尺寸 ----------
def png_size(d):
    return struct.unpack('>II', d[16:24])


def jpg_size(d):
    i = 2
    while i < len(d) - 1:
        if d[i] != 0xFF:
            i += 1
            continue
        mk = d[i + 1]
        if mk in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack('>HH', d[i + 5:i + 9])
            return w, h
        if mk in (0xD8, 0xD9) or 0xD0 <= mk <= 0xD7:
            i += 2
            continue
        ln = struct.unpack('>H', d[i + 2:i + 4])[0]
        i += 2 + ln
    raise ValueError('bad jpg')


def img_size(name):
    d = zin.read('xl/media/' + name)
    return png_size(d) if d[:8] == b'\x89PNG\r\n\x1a\n' else jpg_size(d)


# ---------- 4. 尺寸换算 ----------
CELL_PAD = 5.0
EMU = 9525
INSET = 2.0


def col_px(w):
    return int(((256 * w + int(128 / 7)) / 256) * 7) + CELL_PAD


def row_px(pt):
    return pt * 96.0 / 72.0


# ---------- 5. 重写 sheet3 ----------
new_s3 = s3
for ref, vm in vm_cells:
    old = re.search(r'<c r="%s"[^>]*vm="%s"[^>]*>.*?</c>' % (ref, vm), new_s3, re.S)
    if not old:
        old = re.search(r'<c r="%s"[^>]*vm="%s"[^>]*/>' % (ref, vm), new_s3)
    assert old, ref
    sa = re.search(r's="(\d+)"', old.group(0))
    new_c = '<c r="%s" s="%s"/>' % (ref, sa.group(1) if sa else '0')
    new_s3 = new_s3[:old.start()] + new_c + new_s3[old.end():]

new_s3 = new_s3.replace('</worksheet>', '<drawing r:id="rId1"/></worksheet>')
assert 'vm="' not in new_s3

# ---------- 6. 生成 drawing ----------
anchors, rel_entries = [], []
for s in students:
    img = 'image%d.png' % s['vm']
    w, h = img_size(img)
    cw, ch = col_px(CELL_W_CHARS), row_px(ROW_H.get(s['row'], 152.1))
    scale = min((cw - 2 * INSET) / w, (ch - 2 * INSET) / h)
    dw, dh = w * scale, h * scale
    colOff = (cw - dw) / 2.0
    rowOff = (ch - dh) / 2.0
    assert dw > 20 and dh > 20 and dw <= cw and dh <= ch, \
        fixture_value('texts.3534730e_3') % (s['name'], dw, dh, cw, ch)
    rid = 'rId%d' % s['vm']
    rel_entries.append((rid, img))
    anchors.append(
        fixture_value('texts.3534730e_4')
        % (COLIDX[s['col']], int(round(colOff * EMU)),
           s['row'] - 1, int(round(rowOff * EMU)),
           int(round(dw * EMU)), int(round(dh * EMU)),
           s['idx'] + 1, s['idx'], s['name'], s['name'],
           rid, int(round(dw * EMU)), int(round(dh * EMU))))

drawing_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
               '<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing" '
               'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
               'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
               + ''.join(anchors) + '</xdr:wsDr>')

drawing_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                + ''.join('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/%s"/>' % (r, t) for r, t in rel_entries)
                + '</Relationships>')

sheet3_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
               '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/drawing" Target="../drawings/drawing1.xml"/>'
               '</Relationships>')

# ---------- 7. 清理 workbook.xml ----------
wb = zin.read('xl/workbook.xml').decode('utf-8')
wb2 = re.sub(r'<sheet name="WpsReserved_CellImgList"[^>]*/>', '', wb)
assert wb2 != wb, fixture_value('texts.3534730e_2')

# ---------- 8. 清理 workbook.xml.rels ----------
wbrels = zin.read('xl/_rels/workbook.xml.rels').decode('utf-8')
DROP_TARGETS = ['cellimages.xml', 'metadata.xml', 'richData/rdRichValueTypes.xml',
                'richData/rdrichvaluestructure.xml', 'richData/richValueRel.xml',
                'richData/rdrichvalue.xml', 'worksheets/sheet10.xml']
wbrels2 = wbrels
for t in DROP_TARGETS:
    wbrels2 = re.sub(r'<Relationship [^>]*Target="[^"]*%s"[^>]*/>' % re.escape(t), '', wbrels2)
wbrels2 = re.sub(r'<Relationship Id="rId(10|14|17|18|21|22|23)"[^>]*/>', '', wbrels2)

# ---------- 9. 清理 Content_Types ----------
ct = zin.read('[Content_Types].xml').decode('utf-8')
ct2 = ct
for p in ['/xl/worksheets/sheet10.xml', '/xl/metadata.xml',
          '/xl/richData/rdRichValueTypes.xml', '/xl/cellimages.xml',
          '/xl/richData/rdrichvaluestructure.xml', '/xl/richData/richValueRel.xml',
          '/xl/richData/rdrichvalue.xml']:
    ct2 = re.sub(r'<Override PartName="%s"[^>]*/>' % re.escape(p), '', ct2)

# ---------- 10. 重建包 ----------
DROP_EXACT = set([
    'xl/cellimages.xml', 'xl/_rels/cellimages.xml.rels', 'xl/metadata.xml',
    'xl/richData/rdRichValueTypes.xml', 'xl/richData/rdrichvaluestructure.xml',
    'xl/richData/rdrichvalue.xml', 'xl/richData/richValueRel.xml',
    'xl/richData/_rels/richValueRel.xml.rels',
    'xl/worksheets/sheet10.xml', 'xl/worksheets/_rels/sheet10.xml.rels',
    'xl/drawings/drawing1.xml', 'xl/drawings/_rels/drawing1.xml.rels',
])
# 原文件里还带有 7 张 WPS 早期的高清证件照原图(在 cellimages 中，未出现在相册里)。
# 它们有内容价值，一律保留在包内，不随 XML 引用一起删除。
DROP_JPEG = set()

os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(PHOTODIR, exist_ok=True)
if os.path.exists(OUT):
    os.remove(OUT)

n_ok = 0
zout = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    n = item.filename
    if n in DROP_EXACT or n in DROP_JPEG:
        continue
    if n == 'xl/worksheets/sheet3.xml':
        data = new_s3.encode('utf-8')
    elif n == 'xl/workbook.xml':
        data = wb2.encode('utf-8')
    elif n == 'xl/_rels/workbook.xml.rels':
        data = wbrels2.encode('utf-8')
    elif n == '[Content_Types].xml':
        data = ct2.encode('utf-8')
    else:
        data = zin.read(n)
    zout.writestr(n, data)
    n_ok += 1

zout.writestr('xl/worksheets/_rels/sheet3.xml.rels', sheet3_rels.encode('utf-8'))
zout.writestr('xl/drawings/drawing1.xml', drawing_xml.encode('utf-8'))
zout.writestr('xl/drawings/_rels/drawing1.xml.rels', drawing_rels.encode('utf-8'))
zout.close()

print("\n生成:", OUT)
print("大小:", os.path.getsize(OUT), "bytes  part数:", n_ok + 3)

# ---------- 11. 导出照片 ----------
for f in os.listdir(PHOTODIR):
    if os.path.isfile(os.path.join(PHOTODIR, f)):
        os.remove(os.path.join(PHOTODIR, f))
zin2 = zipfile.ZipFile(SRC)
for s in students:
    safe = re.sub(r'[\\/:*?"<>|]', '_', s['name']) or '未知'
    with open(os.path.join(PHOTODIR, '%02d_%s.png' % (s['idx'], safe)), 'wb') as f:
        f.write(zin2.read('xl/media/image%d.png' % s['vm']))
print("导出照片", len(students), "张 ->", PHOTODIR)

LEFTOVER = os.path.join(PHOTODIR, '合成示例段落：用于验证文档布局与内容转换流程')
if os.path.isdir(LEFTOVER):
    for f in os.listdir(LEFTOVER):
        os.remove(os.path.join(LEFTOVER, f))
os.makedirs(LEFTOVER, exist_ok=True)
for i, j in enumerate(['image1.jpeg', 'image2.jpeg', 'image3.jpeg', 'image4.jpeg',
                       'image5.jpeg', 'image6.jpeg', 'image7.jpeg'], 1):
    with open(os.path.join(LEFTOVER, '高清原图%d.jpeg' % i), 'wb') as f:
        f.write(zin2.read('xl/media/' + j))
print("导出高清原图 7 张 ->", LEFTOVER)

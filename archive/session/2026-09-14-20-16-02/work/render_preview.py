# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-14-20-16-02/work/render_preview.py')
# -*- coding: utf-8 -*-
fixture_value('texts.380883d2_1')
import zipfile, re, os, io
from xml.etree import ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

import sys
_default_out = session_path('input_13.xlsx')
_default_prev = session_path('input_14.png')
OUT = sys.argv[1] if len(sys.argv) > 1 else _default_out
PREVIEW = sys.argv[2] if len(sys.argv) > 2 else _default_prev

M = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
XDR = '{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'

z = zipfile.ZipFile(OUT)
EMU_PX = 9525.0
CELL_PAD = 5.0


def col_px(w):
    if w < 1:
        return int(w * 12 + 0.5)
    return int(((256 * w + int(128 / 7)) / 256) * 7) + CELL_PAD


def row_px(pt):
    return pt * 96.0 / 72.0


# ---- 1. 列宽 ----
s3 = z.read('xl/worksheets/sheet3.xml').decode('utf-8')
cols = {}
for m in re.finditer(r'<col min="(\d+)" max="(\d+)"[^>]*?width="([\d.]+)"', s3):
    a, b, w = int(m.group(1)), int(m.group(2)), float(m.group(3))
    for c in range(a, b + 1):
        cols[c] = w
DEFAULT_W = 9.0
maxcols = 9
colX = [0.0]
for c in range(1, maxcols + 1):
    colX.append(colX[-1] + col_px(cols.get(c, DEFAULT_W)))

# ---- 2. 行高 ----
rows = {}
for m in re.finditer(r'<row\s[^>]*>', s3):
    tag = m.group(0)
    r = int(re.search(r'r="(\d+)"', tag).group(1))
    hm = re.search(r'ht="([\d.]+)"', tag)
    rows[r] = float(hm.group(1)) if hm else 14.25
print("解析到行高条目:", len(rows), " 图片行高 row2 =", rows.get(2))
maxrow = 54
rowY = [0.0]
for r in range(1, maxrow + 1):
    rowY.append(rowY[-1] + row_px(rows.get(r, 14.25)))

W = int(colX[maxcols]) + 20
H = int(rowY[maxrow]) + 20
print("画布尺寸:", W, "x", H)

# ---- 3. 单元格文本 ----
sroot = ET.fromstring(z.read('xl/sharedStrings.xml'))
strings = [''.join(t.text or '' for t in si.iter(M + 't')) for si in sroot.findall(M + 'si')]

cells = {}
sd = ET.fromstring(s3)
for c in sd.iter(M + 'c'):
    ref = c.get('r')
    t = c.get('t')
    v = c.find(M + 'v')
    if v is None or v.text is None:
        continue
    if t == 's':
        cells[ref] = strings[int(v.text)]
    elif t == 'str':
        cells[ref] = v.text

merged = [mc.get('ref') for mc in sd.iter(M + 'mergeCell')]

# ---- 4. 绘制 ----
FONT_PATH = None
for f in [session_path('input_15.ttc'), session_path('input_16.ttf'), session_path('input_17.ttc')]:
    if os.path.exists(f):
        FONT_PATH = f
        break
font = ImageFont.truetype(FONT_PATH, 14) if FONT_PATH else ImageFont.load_default()
font_small = ImageFont.truetype(FONT_PATH, 12) if FONT_PATH else font

img = Image.new('RGB', (W, H), (255, 255, 255))
dr = ImageDraw.Draw(img)

# 网格
for c in range(1, maxcols + 1):
    dr.line([(colX[c], 0), (colX[c], H)], fill=(215, 215, 215), width=1)
for r in range(1, maxrow + 1):
    dr.line([(0, rowY[r]), (W, rowY[r])], fill=(215, 215, 215), width=1)

# 文本
for ref, txt in cells.items():
    m = re.match(r'([A-Z]+)(\d+)', ref)
    if not m:
        continue
    colL = m.group(1)
    r = int(m.group(2))
    ci = 0
    for ch in colL:
        ci = ci * 26 + (ord(ch) - 64)
    if r > maxrow or ci > maxcols:
        continue
    x = colX[ci - 1] + 3
    y = rowY[r - 1] + (rowY[r] - rowY[r - 1]) / 2 - 8
    if '姓名' in txt or '宿舍' in txt:
        dr.text((x, y), txt, fill=(0, 0, 0), font=font)
    elif '电话' in txt:
        dr.text((x, y), txt, fill=(0, 0, 0), font=font_small)

# ---- 5. 贴照片（按 drawing 锚点） ----
d = ET.fromstring(z.read('xl/drawings/drawing1.xml'))
rels = {}
for rel in ET.fromstring(z.read('xl/drawings/_rels/drawing1.xml.rels')):
    rels[rel.get('Id')] = rel.get('Target')

n = 0
check = []
for anc in d.findall(XDR + 'oneCellAnchor'):
    frm = anc.find(XDR + 'from')
    col = int(frm.find(XDR + 'col').text)
    colOff = int(frm.find(XDR + 'colOff').text)
    row = int(frm.find(XDR + 'row').text)
    rowOff = int(frm.find(XDR + 'rowOff').text)
    ext = anc.find(XDR + 'ext')
    if len(check) < 3:
        print("DEBUG anchor#%d col=%d colOff=%d row=%d rowOff=%d ext_tag=%s attrs=%s"
              % (len(check), col, colOff, row, rowOff, ext.tag if ext is not None else None,
                 dict(ext.attrib) if ext is not None else None))
    cx, cy = int(ext.get('cx')), int(ext.get('cy'))
    blip = anc.find('.//' + A + 'blip')
    rid = blip.get(R + 'embed')
    target = rels[rid].replace('../', 'xl/')
    data = z.read(target)
    ph = Image.open(io.BytesIO(data)).convert('RGB')

    x = colX[col] + colOff / EMU_PX
    y = rowY[row] + rowOff / EMU_PX
    w = cx / EMU_PX
    h = cy / EMU_PX
    ph = ph.resize((int(round(w)), int(round(h))), Image.LANCZOS)
    img.paste(ph, (int(round(x)), int(round(y))))
    dr.rectangle([x, y, x + w, y + h], outline=(190, 190, 190), width=1)

    cw = col_px(cols.get(col + 1, DEFAULT_W))
    chh = row_px(rows.get(row + 1, 14.25))
    check.append(dict(n=n, cell='%s%d' % (chr(65 + col), row + 1),
                      x=x, y=y, w=w, h=h, cw=cw, ch=chh,
                      fits=(w <= cw + 0.6 and h <= chh + 0.6),
                      img=target.split('/')[-1]))
    n += 1

print("已贴照片:", n)
over = [c for c in check if not c['fits']]
print("超出单元格的照片:", over if over else "无")
print("\n前 6 个锚点定位(像素):")
for c in check[:6]:
    print(fixture_value('texts.380883d2_2')
          % (c['cell'], c['x'], c['y'], c['w'], c['h'], c['cw'], c['ch'], c['fits'], c['img']))

if len(check) != 44:
    print("!! 锚点数量异常:", len(check))

img.save(PREVIEW)
print("\n预览图:", PREVIEW)

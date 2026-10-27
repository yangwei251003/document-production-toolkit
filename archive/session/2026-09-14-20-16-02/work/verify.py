# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-14-20-16-02/work/verify.py')
# -*- coding: utf-8 -*-
import zipfile, re, os, posixpath
from xml.etree import ElementTree as ET

OUT = session_path('input_18.xlsx')
SRC = session_path('input_19.xlsx')

print("原文件大小:", os.path.getsize(SRC), " 新文件大小:", os.path.getsize(OUT))

z = zipfile.ZipFile(OUT)
bad = z.testzip()
print("Zip 完整性:", "OK" if bad is None else "损坏:"+bad)

names = set(z.namelist())

# 1) 所有 XML 可解析
errs = []
for n in names:
    if n.endswith('.xml') or n.endswith('.rels'):
        try: ET.fromstring(z.read(n))
        except Exception as e: errs.append((n, str(e)[:80]))
print("XML 解析错误:", errs if errs else "无")

# 2) 所有关系目标存在
missing = []
for n in names:
    if n.endswith('.rels'):
        base = posixpath.dirname(posixpath.dirname(n))
        root = ET.fromstring(z.read(n))
        for rel in root:
            tgt = rel.get('Target'); mode = rel.get('TargetMode')
            if mode == 'External' or tgt.startswith('http'): continue
            full = posixpath.normpath(posixpath.join(base, tgt))
            if full not in names: missing.append((n, tgt, full))
print("关系目标缺失:", missing if missing else "无")

# 3) Content_Types 与包一致
ct = z.read('[Content_Types].xml').decode()
overrides = set(re.findall(r'PartName="([^"]+)"', ct))
defaults = set(re.findall(r'Extension="([^"]+)"', ct))
uncov = []
for n in names:
    if n == '[Content_Types].xml': continue
    if '/'+n in overrides: continue
    if n.rsplit('.',1)[-1].lower() in defaults: continue
    uncov.append(n)
print("Content_Types 未覆盖:", uncov if uncov else "无")

# 4) 图片残留检查
print("\n残留检查:")
print("  vm= 出现:", z.read('xl/worksheets/sheet3.xml').decode().count('vm="'))
print("  richData part:", [n for n in names if 'richData' in n] or "已清空")
print("  cellimages part:", [n for n in names if 'cellimages' in n] or "已清空")
print("  sheet10 part:", [n for n in names if 'sheet10' in n] or "已清空")
print("  jpeg 残留:", [n for n in names if n.endswith('.jpeg')] or "已清空")

# 5) drawing 检查
d = z.read('xl/drawings/drawing1.xml').decode()
anchors = re.findall(r'<xdr:oneCellAnchor>', d)
embeds = re.findall(r'r:embed="(rId\d+)"', d)
print("\ndrawing1.xml: 锚点数=", len(anchors), " 图片引用数=", len(embeds), " 去重=", len(set(embeds)))
dr = z.read('xl/drawings/_rels/drawing1.xml.rels').decode()
dmap = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', dr))
print("  rels 条目:", len(dmap), " 全部指向 media:", all('media/' in v for v in dmap.values()))
missing_img = [v for v in dmap.values() if posixpath.normpath(posixpath.join('xl/drawings', v)) not in names]
print("  缺失图片:", missing_img if missing_img else "无")

# 6) sheet3 有 drawing 且顺序正确
s3 = z.read('xl/worksheets/sheet3.xml').decode()
print("\nsheet3 含 <drawing>:", '<drawing r:id="rId1"/>' in s3)
print("sheet3 rels:", z.read('xl/worksheets/_rels/sheet3.xml.rels').decode()[:200])
print("sheet3 尾部:", s3[-160:])

# 7) workbook 表名
wb = z.read('xl/workbook.xml').decode()
print("\n工作表:", re.findall(r'<sheet name="([^"]+)"', wb))
print("WpsReserved 残留:", 'WpsReserved' in wb)

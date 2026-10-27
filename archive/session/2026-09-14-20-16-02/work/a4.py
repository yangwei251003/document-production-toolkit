# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-14-20-16-02/work/a4.py')
import zipfile, re, io
SRC = session_path('input_7.xlsx')
z = zipfile.ZipFile(SRC)
def read(n): return z.read(n).decode('utf-8','ignore')
s3 = read('xl/worksheets/sheet3.xml')

print("=== 行定义（原样） ===")
for m in re.finditer(r'<row [^>]*>', s3):
    print("  ", m.group(0))

print("\n=== sheetFormatPr ===")
print("  ", re.search(r'<sheetFormatPr[^>]*/>', s3).group(0))

# styles: xf 13
st = read('xl/styles.xml')
xfs = re.search(r'<cellXfs count="(\d+)">(.*?)</cellXfs>', st, re.S)
lst = re.findall(r'<xf [^>]*/>|<xf .*?</xf>', xfs.group(2), re.S)
print("\n=== cellXfs 总数:", xfs.group(1))
for i in [8,9,10,13,48,7]:
    if i < len(lst): print(f"  xf[{i}]: {lst[i]}")
borders = re.search(r'<borders count="(\d+)">(.*?)</borders>', st, re.S)
bl = re.findall(r'<border.*?</border>|<border[^>]*/>', borders.group(2), re.S)
print("\n=== borders 数量:", borders.group(1))
fills = re.search(r'<fills count="(\d+)">(.*?)</fills>', st, re.S)
fl = re.findall(r'<fill>.*?</fill>|<fill/>', fills.group(2), re.S)
print("=== fills 数量:", fills.group(1))

# 图片尺寸
try:
    from PIL import Image
    hasPIL = True
except ImportError:
    hasPIL = False
print("\n=== PIL 可用:", hasPIL)

import struct
def png_size(data):
    w,h = struct.unpack('>II', data[16:24]); return w,h
def jpg_size(data):
    i=2
    while i < len(data):
        if data[i]!=0xFF: i+=1; continue
        m=data[i+1]
        if m in (0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF):
            h,w = struct.unpack('>HH', data[i+5:i+9]); return w,h
        if m in (0xD8,0xD9) or 0xD0<=m<=0xD7: i+=2; continue
        ln = struct.unpack('>H', data[i+2:i+4])[0]; i += 2+ln
    return None

print("\n=== media 图片尺寸 ===")
for n in sorted(z.namelist()):
    if '/media/' not in n: continue
    d = z.read(n)
    try:
        if d[:8]==b'\x89PNG\r\n\x1a\n': w,h = png_size(d)
        elif d[:2]==b'\xff\xd8': w,h = jpg_size(d)
        else: w,h = None,None
    except Exception as e: w,h=None,None
    print(f"  {n.split('/')[-1]:16s} {len(d):>8d}B  {w}x{h}")

# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-14-20-16-02/work/make_lite.py')
# -*- coding: utf-8 -*-
fixture_value('texts.b80b6fc6_1')
import zipfile, re, os, io, posixpath
from PIL import Image

SRCDIR = session_path('input_12')
SRC = os.path.join(SRCDIR, "26电气工程本科8班花名册_图片修复版.xlsx")
OUT = os.path.join(SRCDIR, "26电气工程本科8班花名册_手机精简版.xlsx")

MAX_W, MAX_H = 480, 680
QUALITY = 82

z = zipfile.ZipFile(SRC)
names = set(z.namelist())

# 1) drawing1.xml.rels: rId -> 旧 media 路径
rels_txt = z.read('xl/drawings/_rels/drawing1.xml.rels').decode('utf-8')
rid_map = dict(re.findall(r'Id="([^"]+)"[^>]*Target="\.\./media/([^"]+)"', rels_txt))
print("照片引用数:", len(rid_map))

new_media = {}       # 新文件名 -> bytes
new_rels = {}        # rId -> 新文件名
old_media = set()
total_old = total_new = 0

for rid, oldname in rid_map.items():
    data = z.read('xl/media/' + oldname)
    total_old += len(data)
    im = Image.open(io.BytesIO(data))
    if im.mode in ('RGBA', 'LA', 'P'):
        bg = Image.new('RGB', im.size, (255, 255, 255))
        im = im.convert('RGBA')
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert('RGB')
    im.thumbnail((MAX_W, MAX_H), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
    b = buf.getvalue()
    newname = oldname.rsplit('.', 1)[0] + '.jpeg'
    new_media[newname] = b
    new_rels[rid] = newname
    old_media.add(oldname)
    total_new += len(b)

print(fixture_value('texts.b80b6fc6_2') % (total_old / 1048576, total_new / 1048576))

# 2) 重写 rels
new_rels_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                + ''.join('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/%s"/>' % (r, n)
                          for r, n in sorted(new_rels.items(), key=lambda kv: int(re.sub(r'\D', '', kv[0]))))
                + '</Relationships>')

# 3) 重建包：丢弃全部旧 media，写入压缩后的照片
if os.path.exists(OUT):
    os.remove(OUT)
zout = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED)

for item in z.infolist():
    n = item.filename
    if n.startswith('xl/media/'):
        continue
    if n == 'xl/drawings/_rels/drawing1.xml.rels':
        zout.writestr(n, new_rels_xml.encode('utf-8'))
        continue
    zout.writestr(n, z.read(n))

for name, b in new_media.items():
    zout.writestr('xl/media/' + name, b)

zout.close()
z.close()

print("\n生成:", OUT)
print("大小: %.1f MB" % (os.path.getsize(OUT) / 1048576))

# 4) 校验
zz = zipfile.ZipFile(OUT)
nn = set(zz.namelist())
bad = []
for rel in re.findall(r'Target="([^"]+)"', zz.read('xl/drawings/_rels/drawing1.xml.rels').decode()):
    full = posixpath.normpath(posixpath.join('xl/drawings', rel))
    if full not in nn:
        bad.append(full)
print("图片引用缺失:", bad if bad else "无")
print("media 文件数:", len([x for x in nn if x.startswith('xl/media/')]))
print("Zip 完整性:", "OK" if zz.testzip() is None else "异常")

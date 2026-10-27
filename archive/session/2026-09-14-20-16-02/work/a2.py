# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-14-20-16-02/work/a2.py')
import zipfile, re
SRC = session_path('input_5.xlsx')
z = zipfile.ZipFile(SRC)
def read(n): return z.read(n).decode('utf-8','ignore')

s3 = read('xl/worksheets/sheet3.xml')
print("sheet3.xml 长度:", len(s3))
print("DISPIMG 出现次数:", s3.count('DISPIMG'))
print("含 'rv' 元数据单元格:", len(re.findall(r'vm="', s3)))
print("含 '_xlfn' :", s3.count('_xlfn'))
print(fixture_value('texts.fc364c42_1'))
print(s3[:900])
print(fixture_value('texts.fc364c42_2'))
cs = re.findall(r'<c [^>]*/?>(?:.*?</c>)?|<c [^>]*/>', s3, re.S)
for c in cs[:30]:
    print(repr(c[:300]))
print(fixture_value('texts.fc364c42_3'))
print([n for n in z.namelist() if 'sheet3' in n])
print('合成示例段落：用于验证文档布局与内容转换流程:', [n for n in z.namelist() if 'worksheets/_rels' in n])

# 所有 sheet 中 DISPIMG 统计
print(fixture_value('texts.fc364c42_4'))
for n in sorted([x for x in z.namelist() if re.match(r'xl/worksheets/sheet\d+\.xml$', x)]):
    t = read(n)
    print(f"  {n}: DISPIMG={t.count('DISPIMG')}, vm={len(re.findall(chr(34).join(['vm=','']), t))}, len={len(t)}")

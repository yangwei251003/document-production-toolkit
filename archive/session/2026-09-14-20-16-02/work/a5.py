# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-14-20-16-02/work/a5.py')
import zipfile, re
SRC = session_path('input_8.xlsx')
z = zipfile.ZipFile(SRC)
def read(n): return z.read(n).decode('utf-8','ignore')
s3 = read('xl/worksheets/sheet3.xml')
print("=== sheet3 尾部 1200 字符 ===")
print(s3[-1200:])
print("\n=== sheet10.xml 全文 ===")
print(read('xl/worksheets/sheet10.xml'))
print("\n=== sheet10.xml.rels ===")
print(read('xl/worksheets/_rels/sheet10.xml.rels'))
print(fixture_value('texts.69333c79_1'))
print(read('xl/drawings/drawing1.xml')[:1500])
print("\n=== [Content_Types].xml ===")
print(read('[Content_Types].xml'))
print("\n=== 所有 media 数量 ===")
allm = [n for n in z.namelist() if '/media/' in n]
print("总数:", len(allm))
print([n.split('/')[-1] for n in sorted(allm)])

# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-14-20-16-02/work/a3.py')
import zipfile, re
SRC = session_path('input_6.xlsx')
z = zipfile.ZipFile(SRC)
def read(n): return z.read(n).decode('utf-8','ignore')
s3 = read('xl/worksheets/sheet3.xml')

# cols
print("=== cols ===")
for c in re.findall(r'<col [^>]*/>', s3): print("  ", c)
# merge
mc = re.search(r'<mergeCells.*?</mergeCells>', s3, re.S)
print("\n=== mergeCells ===")
if mc:
    for m in re.findall(r'<mergeCell ref="([^"]+)"/>', mc.group(0)): print("  ", m)
else: print("  none")
# rows heights
print("\n=== rows (行高) ===")
rows = re.findall(r'<row r="(\d+)"[^>]*?(?:ht="([\d.]+)")?[^>]*>', s3)
for r,h in rows[:60]:
    print(f"  row{r}: ht={h}")

# vm cells
print("\n=== 所有 vm 单元格 ===")
vmcells = re.findall(r'<c r="([A-Z]+\d+)"([^>]*vm="(\d+)"[^>]*)>', s3)
print("数量:", len(vmcells))
for ref, attrs, vm in vmcells[:50]:
    print(f"  {ref:6s} vm={vm:>3s}  attrs={attrs[:60]}")

# metadata -> rv mapping
md = read('xl/metadata.xml')
bks = re.findall(r'<xlrd:rvb i="(\d+)"/>', md)
print("\n=== metadata bk 数量:", len(bks), "前10:", bks[:10])
rv = read('xl/richData/rdrichvalue.xml')
rvs = re.findall(r'<rv s="(\d+)">(.*?)</rv>', rv, re.S)
print("rv 数量:", len(rvs))
for i,(s,inner) in enumerate(rvs[:8]):
    print(f"  rv[{i}] s={s} inner={inner}")

# richValueRel order
rvrel = read('xl/richData/richValueRel.xml')
rels_order = re.findall(r'<rel r:id="(rId\d+)"/>', rvrel)
print(fixture_value('texts.ca2a5a60_1'), rels_order[:8], " 总数:", len(rels_order))
rvrels = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', read('xl/richData/_rels/richValueRel.xml.rels')))
print("  映射前8:", [(r, rvrels.get(r)) for r in rels_order[:8]])
print("  映射后4:", [(r, rvrels.get(r)) for r in rels_order[-4:]])

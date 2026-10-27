# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-14-20-16-02/work/analyze.py')
import zipfile, re, os, sys, collections
from xml.etree import ElementTree as ET

SRC = session_path('input_9.xlsx')
z = zipfile.ZipFile(SRC)

def read(n):
    return z.read(n).decode('utf-8', 'ignore')

# workbook rels: rId -> sheetN.xml
wb_rels = read('xl/_rels/workbook.xml.rels')
m = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', wb_rels))
print("=== workbook rels ===")
for k,v in m.items(): print(" ", k, "->", v)

wb = read('xl/workbook.xml')
sheets = re.findall(r'<sheet name="([^"]+)"[^>]*r:id="([^"]+)"', wb)
print("\n=== sheet map ===")
for name, rid in sheets:
    print(f"  {name:30s} {rid} -> {m.get(rid)}")

# cellimages: index -> ID -> target
ci = read('xl/cellimages.xml')
ci_rels = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', read('xl/_rels/cellimages.xml.rels')))
pics = re.findall(r'<xdr:cNvPr id="(\d+)" name="(ID_[0-9A-F]+)"[^>]*/>\s*</xdr:nvPicPr><xdr:cNvPicPr/>\s*</xdr:nvPicPr>\s*<xdr:blipFill><a:blip r:embed="([^"]+)"', ci)
print(f"\n=== cellimages 数量: {len(pics)} ===")
id2media = {}
for pid, name, embed in pics:
    med = ci_rels.get(embed,'?')
    id2media[name] = med
    print("  ", name, "->", med)

# richvalue
rv = read('xl/richData/rdrichvalue.xml')
print(fixture_value('texts.a6be56d5_1'))
print(rv[:600])
rvt = read('xl/richData/rdRichValueTypes.xml')
print(fixture_value('texts.a6be56d5_2'))
print(rvt[:800])
print(fixture_value('texts.a6be56d5_3'))
print(read('xl/richData/richValueRel.xml')[:600])
print("\n=== metadata.xml ===")
print(read('xl/metadata.xml')[:800])

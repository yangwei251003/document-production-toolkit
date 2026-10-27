# Sanitized historical source; synthetic prose and portable workspace bindings.
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('career/package_delivery.py')
from pathlib import Path
import json
import shutil
import zipfile
import hashlib

ROOT = workspace_root()
OUT = ROOT / '交付文件'
WORK = ROOT / '工作记录'
checks = json.loads((WORK / '文件检查结果.json').read_text(encoding='utf-8-sig'))
for item in checks:
    assert item['page_count_ok'] and item['A4_ok'] and item['text_complete']
    assert not item['replacement_glyphs']
    item['visual_review'] = 'PASS'
    item['visual_review_notes'] = '合成示例内容：通过项目实践展示文档制作与检查流程.5磅，日期9.5磅，详细版页脚8.5磅。'
(WORK / '文件检查结果.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')

review = OUT / '本人审阅资料'
review.mkdir(exist_ok=True)
shutil.copy2(WORK / '个人事实与证据索引.md', review / '事实与证据索引.md')
shutil.copy2(WORK / '岗位与评分对照.md', review / '岗位与评分对照.md')
files = sorted(p for p in OUT.rglob('*') if p.is_file())
assert len(files) == 11, [str(p) for p in files]
assert len(list(OUT.glob('*.pdf'))) == 4
assert len(list(OUT.glob('*.docx'))) == 4
archive = ROOT / '示例同学_职业规划大赛简历交付包_[示例编号].zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p, Path('示例同学_简历交付包') / p.relative_to(OUT))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.infolist()) == 11
    for p in files:
        name = (Path('示例同学_简历交付包') / p.relative_to(OUT)).as_posix()
        assert hashlib.sha256(z.read(name)).digest() == hashlib.sha256(p.read_bytes()).digest()
manifest = {
    'archive': archive.name,
    'size_bytes': archive.stat().st_size,
    'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
    'crc_test': 'PASS',
    'extracted_bytes_match': True,
    'files': [p.relative_to(OUT).as_posix() for p in files],
}
(WORK / '压缩包检查结果.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
(WORK / '验收记录.md').write_text('# 简历阶段验收记录\n\n日期：2026-10-22。\n\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 正文10.5磅；日期9.5合成示例内容：通过项目实践展示文档制作与检查流程.5合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- ZIP合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n- 合成示例内容：通过项目实践展示文档制作与检查流程\n\n合成示例内容：通过项目实践展示文档制作与检查流程\n\n证据：文件检查结果.json、压缩包检查结果.json、逐页预览目录。\n', encoding='utf-8')
print(json.dumps(manifest, ensure_ascii=False, indent=2))

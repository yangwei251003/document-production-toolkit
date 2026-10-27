# Sanitized historical source; synthetic prose and portable workspace bindings.
from __future__ import annotations
from document_toolkit.runtime import enter_archive, workspace_root, source_path
enter_archive('scholarship/国家奖学金申请表_填写版/04_按原格式去除修订并转DOCX.py')

import json
import os
from pathlib import Path

import pythoncom
import win32com.client


source = Path(source_path('2025－2026学年国家奖学金申请审批表.doc'))
target = source.with_name('2025－2026合成示例内容：通过项目实践展示文档制作与检查流程_无修订_示例同学_24电气工程本科5班.docx')

if not source.is_file():
    raise FileNotFoundError(source)

pythoncom.CoInitialize()
word = None
document = None
try:
    # Start a separate, hidden Word instance. The original .doc is opened as the
    # formatting source and is never saved back to disk.
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    document = word.Documents.Open(
        FileName=str(source),
        ConfirmConversions=False,
        ReadOnly=False,
        AddToRecentFiles=False,
        Visible=False,
        OpenAndRepair=True,
        NoEncodingDialog=True,
    )
    revisions_before = int(document.Revisions.Count)
    if revisions_before:
        document.AcceptAllRevisions()
    document.TrackRevisions = False
    # wdFormatXMLDocument = 16. SaveAs2 preserves the original page setup,
    # tables, fonts, and layout while writing a modern DOCX file.
    document.SaveAs2(
        FileName=str(target),
        FileFormat=16,
        AddToRecentFiles=False,
    )
    print(json.dumps({
        "source": str(source),
        "target": str(target),
        "revisions_before": revisions_before,
        "revisions_after": int(document.Revisions.Count),
        "track_revisions": bool(document.TrackRevisions),
        "pages": int(document.ComputeStatistics(2)),
        "target_exists": target.is_file(),
        "target_bytes": target.stat().st_size if target.is_file() else 0,
    }, ensure_ascii=False))
finally:
    if document is not None:
        document.Close(SaveChanges=0)
    if word is not None:
        word.Quit(SaveChanges=0)
    pythoncom.CoUninitialize()

# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-08-23-38-21/setup_print.py')
import os, sys, time
import win32com.client as win32

SRC = session_path('input_22.xls')
OUT = session_path('input_23.xlsx')
PDFDIR = session_path('input_24')

# margins in points: 1cm = 28.35pt
M_LR = 0.4 * 28.35
M_TB = 0.5 * 28.35

os.makedirs(PDFDIR, exist_ok=True)
app = win32.DispatchEx('KET.Application')
app.Visible = False
app.DisplayAlerts = False
time.sleep(2)
try:
    wb = app.Workbooks.Open(SRC)
    for ws in wb.Sheets:
        ps = ws.PageSetup
        ps.PaperSize = 9            # A4
        ps.Orientation = 1          # portrait
        ps.Zoom = False
        ps.FitToPagesWide = 1
        ps.FitToPagesTall = 1
        ps.LeftMargin = M_LR
        ps.RightMargin = M_LR
        ps.TopMargin = M_TB
        ps.BottomMargin = M_TB
        ps.HeaderMargin = 0
        ps.FooterMargin = 0
        ps.CenterHorizontally = True
        ps.CenterVertically = True
        ps.PrintGridlines = False
        ps.PrintHeadings = False
        print(ws.Name, 'pagesetup done')

    wb.SaveAs(OUT, 51)
    print('saved xlsx:', OUT)

    for ws in wb.Sheets:
        pdf = os.path.join(PDFDIR, ws.Name + '.pdf')
        if os.path.exists(pdf):
            os.remove(pdf)
        ws.ExportAsFixedFormat(0, pdf)
        print('pdf:', pdf, os.path.getsize(pdf) if os.path.exists(pdf) else 'MISSING')

    wb.Close(False)
finally:
    app.Quit()

# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-08-23-38-21/setup_2page.py')
import os, time
import win32com.client as win32

F = session_path('input_20.xlsx')
PDFDIR = session_path('input_21')

# per-sheet column widen factor (content is height-bound on 2 pages, so we
# widen columns to make the table fill the printable width)
K = {'表一': 1.15, '表二': 1.10}
TITLE_ROWS = {'表一': '$4:$4', '表二': '$3:$3'}  # repeat header row on page 2

app = win32.DispatchEx('KET.Application')
app.Visible = False
app.DisplayAlerts = False
time.sleep(2)
try:
    wb = app.Workbooks.Open(F)
    for ws in wb.Sheets:
        k = K[ws.Name]
        ur = ws.UsedRange
        ncols = ur.Columns.Count
        for c in range(1, ncols + 1):
            col = ws.Columns(c)
            col.ColumnWidth = col.ColumnWidth * k
        ps = ws.PageSetup
        ps.Zoom = False
        ps.FitToPagesWide = 1
        ps.FitToPagesTall = 2          # two pages per sheet
        ps.CenterHorizontally = True
        ps.CenterVertically = False
        ps.PrintTitleRows = TITLE_ROWS[ws.Name]  # header repeats on page 2
        print(ws.Name, f'widened x{k}, fit 1w x 2h')

    wb.Save()

    for ws in wb.Sheets:
        pdf = os.path.join(PDFDIR, ws.Name + '.pdf')
        if os.path.exists(pdf):
            os.remove(pdf)
        ws.ExportAsFixedFormat(0, pdf)
        print('pdf:', pdf, os.path.getsize(pdf))

    wb.Close(True)
finally:
    app.Quit()

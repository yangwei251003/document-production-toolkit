# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-08-23-38-21/test_open.py')
import time, os
import win32com.client as win32

SRC = session_path('input_25.xls')

for attempt in range(3):
    try:
        app = win32.DispatchEx('KET.Application')
        app.Visible = False
        app.DisplayAlerts = False
        time.sleep(1.5)
        wb = app.Workbooks.Open(SRC)
        print('OK on attempt', attempt, [s.Name for s in wb.Sheets])
        wb.Close(False)
        app.Quit()
        break
    except Exception as e:
        print('attempt', attempt, 'failed:', e)
        try:
            app.Quit()
        except Exception:
            pass
        time.sleep(3)

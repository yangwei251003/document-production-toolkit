import json
from contextlib import contextmanager
from pathlib import Path
from . import runtime

FIXTURE=Path(__file__).resolve().parents[1]/'fixtures/session-synthetic.json'

def fixture_value(key):
    value=json.loads(FIXTURE.read_text(encoding='utf-8'))
    for part in key.split('.'):value=value[part]
    return value

def session_path(asset_id):
    base=runtime.workspace_root()
    if asset_id.startswith('output_'):return str(base/asset_id)
    return str(base/'inputs'/Path(asset_id).name)

@contextmanager
def synthetic_workbook_session(workspace):
    token=runtime._ACTIVE.set({'script_id':'session/2026-09-03-20-47-16/outputs/gen_xlsx.py','workspace':Path(workspace).resolve()})
    try:yield
    finally:runtime._ACTIVE.reset(token)

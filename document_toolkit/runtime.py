"""Explicit execution gate for archived programs. No Office/network execution API."""
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path

_ACTIVE=ContextVar('document_archive_active',default=None)

def enter_archive(script_id):
    active=_ACTIVE.get()
    if not active or active['script_id']!=script_id:
        raise SystemExit('Historical source is disabled by default. Use: python -m document_toolkit demo --output NEW_DIRECTORY. Office, downloads and original-material workflows are not enabled.')

def workspace_root():
    active=_ACTIVE.get()
    if not active:raise RuntimeError('No explicit synthetic workspace')
    return active['workspace']

def source_path(basename):
    if basename=='fixture-portrait.png':return workspace_root()/'assets'/'fixture-portrait.png'
    return workspace_root()/'external-inputs'/Path(basename).name

@contextmanager
def synthetic_resume_session(workspace):
    """Enable only the reviewed resume generator, never arbitrary archive programs."""
    workspace=Path(workspace).resolve()
    token=_ACTIVE.set({'script_id':'career/build_resumes.py','workspace':workspace})
    try:yield
    finally:_ACTIVE.reset(token)

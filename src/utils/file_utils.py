"""
file_utils.py (patched)
Extract every .py file mentioned in a traceback.
"""
from __future__ import annotations
import re
from pathlib import Path
from typing import List

_TRACE_RE = re.compile(r'File "(.+?\.py)", line')

def files_from_traceback(tb: str) -> List[Path]:
    found: set[Path] = set()
    for m in _TRACE_RE.finditer(tb):
        p = Path(m.group(1)).resolve()
        if p.is_file():
            found.add(p)
    return list(found)

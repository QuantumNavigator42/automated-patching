"""
refactor.py
Uses openai-python ≥ 1.0 interface.

ENV:
  OPENAI_API_KEY_CYC  (primary)  | OPENAI_API_KEY (fallback)
  OPENAI_MODEL        (default: o3-2025-04-16)
  OPENAI_TEMPERATURE  (default: 0.2)
"""

from __future__ import annotations

import os
import re
import textwrap
from typing import List

from openai import OpenAI

# ── environment ──────────────────────────────────────────────────────
_api_key = os.getenv("OPENAI_API_KEY_CYC") or os.getenv("OPENAI_API_KEY")
if not _api_key:
    raise EnvironmentError("Set OPENAI_API_KEY_CYC or OPENAI_API_KEY")

MODEL       = os.getenv("OPENAI_MODEL", "o3-2025-04-16")
TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))

client = OpenAI(api_key=_api_key)

SYSTEM_MSG = (
    "You are an elite Python refactorer. Given a failing traceback "
    "and the file's current contents, return a **complete replacement** "
    "inside one fenced code block."
)

# ── helpers ───────────────────────────────────────────────────────────
_FENCE = re.compile(r"```(?:python)?\s*(.*?)```", re.DOTALL)


def _extract(code_with_fence: str) -> str:
    m = _FENCE.search(code_with_fence)
    if not m:
        raise ValueError("No fenced code block in LLM reply.")
    return m.group(1).rstrip() + "\n"


def _build_prompt(src: str, tb: str) -> str:
    return textwrap.dedent(
        f"""
        ### Traceback
        ```
        {tb}
        ```

        ### Current Source
        ```python
        {src}
        ```
        """
    ).strip()


# ── public ────────────────────────────────────────────────────────────
def refactor_code(source: str, traceback: str) -> str:
    prompt = _build_prompt(source, traceback)

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user",   "content": prompt},
        ],
    )

    reply: str = resp.choices[0].message.content
    return _extract(reply)


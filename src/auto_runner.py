"""
auto_runner.py
Self-healing loop with:  (1) max_file_touches per cycle,  (2) max_cycles cap,
and markdown diff logging.

CLI:
  python auto_runner.py --entry PATH [--max-cycles N] [--max-file-touches M]
"""

from __future__ import annotations

import argparse
import difflib
import logging
import subprocess
import sys
from pathlib import Path

from utils.file_utils import files_from_traceback
from utils.refactor import refactor_code

# ---------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_DIR / "runner.log"),
        logging.StreamHandler(sys.stdout),
    ],
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def run_program(entry: Path) -> tuple[bool, str]:
    """Run the target script; return (success?, combined output)."""
    proc = subprocess.run(
        [sys.executable, str(entry)],
        text=True,
        capture_output=True,
    )
    return proc.returncode == 0, proc.stdout + proc.stderr


def write_diff(old: str, new: str, diff_path: Path) -> None:
    diff = difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile="before",
        tofile="after",
    )
    diff_path.write_text("".join(diff), encoding="utf-8")


def patch_file(path: Path, tb: str, cycle: int, touch_no: int) -> bool:
    """Run LLM refactor on one file. Return True if content changed."""
    old_src = path.read_text(encoding="utf-8")
    new_src = refactor_code(old_src, tb)
    if not new_src or new_src == old_src:
        return False

    path.write_text(new_src, encoding="utf-8")

    diff_dir = LOG_DIR / f"cycle_{cycle}"
    diff_dir.mkdir(exist_ok=True)
    write_diff(old_src, new_src, diff_dir / f"{touch_no}_{path.name}.diff")
    return True


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--entry", required=True, help="Entry script path")
    parser.add_argument("--max-cycles", type=int, default=3)
    parser.add_argument("--max-file-touches", type=int, default=4)
    args = parser.parse_args()

    entry = Path(args.entry).resolve()
    logging.info("Start run | entry=%s | max_cycles=%s | max_file_touches=%s",
                 entry, args.max_cycles, args.max_file_touches)

    total_touches = 0
    for cycle in range(1, args.max_cycles + 1):
        touches_this_cycle = 0
        while touches_this_cycle < args.max_file_touches:
            success, output = run_program(entry)
            if success:
                logging.info("SUCCESS in cycle %s after %s total touches.",
                             cycle, total_touches)
                return

            files = files_from_traceback(output)
            if not files:
                logging.error("Traceback contained no patchable files. Abort.")
                sys.exit(1)

            patched_any = False
            for f in files:
                if touches_this_cycle >= args.max_file_touches:
                    break
                if patch_file(f, output, cycle, touches_this_cycle + 1):
                    touches_this_cycle += 1
                    total_touches += 1
                    patched_any = True
                    break  # re-run program immediately after one patch

            if not patched_any:
                logging.warning("No modifications produced; breaking inner loop.")
                break

        logging.info("Cycle %s complete | touches=%s", cycle, touches_this_cycle)

    logging.error("FAILURE: reached max_cycles=%s (total touches=%s)",
                  args.max_cycles, total_touches)
    sys.exit(1)


if __name__ == "__main__":
    main()


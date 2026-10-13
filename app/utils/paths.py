"""Resolve bundled resources and portable writable data paths."""

import os
import sys
from pathlib import Path


def resource_path(relative_path: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return base / relative_path


def data_dir() -> Path:
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).resolve().parent
    else:
        base = Path(__file__).resolve().parents[2]
    portable = base / "data"
    try:
        portable.mkdir(parents=True, exist_ok=True)
        probe = portable / ".write-test"
        probe.touch(exist_ok=True)
        probe.unlink(missing_ok=True)
        return portable
    except OSError:
        fallback = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "MuthyaraSmartCalculator"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback
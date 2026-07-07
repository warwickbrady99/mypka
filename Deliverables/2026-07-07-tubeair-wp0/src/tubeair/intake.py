"""Fusion247/MyPKA intake paths for TubeAIR captures."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


DEFAULT_INTAKE_ROOT = Path(r"C:\Users\Buggly\OneDrive\Desktop\MyPKA\Team Inbox\TubeAIR")


def dated_intake_dir(root: Path | None = None, captured_at: datetime | None = None) -> Path:
    """Return the YYYY/MM intake folder for a capture."""

    timestamp = captured_at or datetime.now()
    base = root or DEFAULT_INTAKE_ROOT
    return base / f"{timestamp:%Y}" / f"{timestamp:%m}"

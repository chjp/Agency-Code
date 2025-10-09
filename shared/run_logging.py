"""Session logging utilities for Agency Code runs."""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from typing import Any


def _make_json_safe(value: Any) -> Any:
    """Convert value into a JSON-serializable form."""
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, list):
        return [_make_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _make_json_safe(val) for key, val in value.items()}
    if hasattr(value, "model_dump"):
        try:
            return _make_json_safe(value.model_dump())
        except Exception:  # pragma: no cover - fallback path
            pass
    if hasattr(value, "dict") and callable(getattr(value, "dict")):
        try:
            return _make_json_safe(value.dict())
        except Exception:  # pragma: no cover - fallback path
            pass
    if hasattr(value, "__dict__"):
        try:
            return _make_json_safe(vars(value))
        except Exception:  # pragma: no cover - fallback path
            pass
    return repr(value)


class SessionRunLogger:
    """Thread-safe logger that writes structured session events to JSONL."""

    def __init__(self, log_path: str, session_id: str) -> None:
        self.log_path = log_path
        self.session_id = session_id
        self._lock = threading.Lock()

    def log(self, event: str, agent: str | None = None, **payload: Any) -> None:
        """Append a structured log entry to the session file."""
        record: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "event": event,
        }
        if agent is not None:
            record["agent"] = agent
        if payload:
            record["data"] = _make_json_safe(payload)

        line = json.dumps(record, ensure_ascii=False)
        with self._lock:
            with open(self.log_path, "a", encoding="utf-8") as handle:
                handle.write(f"{line}\n")

    def path(self) -> str:
        return self.log_path


def create_session_logger(log_dir: str) -> SessionRunLogger:
    """Create a session logger using a daily log file under log_dir."""
    os.makedirs(log_dir, exist_ok=True)
    now = datetime.now()

    # Daily log file: agentrunlog/20251008.jsonl
    daily_date = now.strftime("%Y%m%d")
    log_path = os.path.join(log_dir, f"{daily_date}.jsonl")

    # Session ID with time: 20251008T214530
    session_id = now.strftime("%Y%m%dT%H%M%S")

    return SessionRunLogger(log_path, session_id)


"""Utilities for persisting structured traces of orchestrations."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from json import dumps
from pathlib import Path
from types import TracebackType
from typing import Any, cast, Mapping, MutableSequence


def _coerce(value: object) -> object:
    if hasattr(value, "to_dict"):
        method = value.to_dict
        if callable(method):  # pragma: no branch - mypy friendly
            result = method()
            return _coerce(result)
    if is_dataclass(value):
        data = asdict(cast(Any, value))
        return {str(k): _coerce(v) for k, v in data.items()}
    if isinstance(value, Mapping):
        return {str(k): _coerce(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_coerce(v) for v in value]
    return value


class Tracer:
    """Collects events and writes them to ``.naestro_runs`` for inspection."""

    def __init__(
        self, root: Path | str | None = None, run_name: str | None = None
    ) -> None:
        self._root = Path(root or ".naestro_runs")
        self._root.mkdir(parents=True, exist_ok=True)
        timestamp = run_name or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self._run_path = self._root / timestamp
        self._run_path.mkdir(parents=True, exist_ok=True)
        self._events: MutableSequence[dict[str, object]] = []

    @property
    def run_path(self) -> Path:
        return self._run_path

    def log_event(
        self, event: str, payload: Mapping[str, object] | None = None
    ) -> None:
        data: Mapping[str, object] = payload if payload is not None else {}
        record = {
            "event": event,
            "payload": _coerce(data),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._events.append(record)

    def flush(self) -> Path:
        target = self._run_path / "trace.json"
        target.write_text(dumps(list(self._events), indent=2), encoding="utf-8")
        return target

    def __enter__(self) -> "Tracer":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.flush()


__all__ = ["Tracer"]

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Callable, Mapping

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:  # pragma: no cover - defensive path setup
    sys.path.insert(0, str(PROJECT_ROOT))

jsonschema = pytest.importorskip("jsonschema")

from naestro.core.bus import (
    LoggingMiddleware,
    MessageBus,
    RedactionMiddleware,
)
from naestro.core.summary import summarize
from naestro.core.trace import build_trace, write_trace


def test_message_bus_middleware_sequence() -> None:
    bus = MessageBus()
    trace: list[str] = []

    def middleware_one(
        event: str,
        payload: dict[str, object],
        forward: Callable[[str, dict[str, object]], tuple[str, dict[str, object]]],
    ) -> tuple[str, dict[str, object]]:
        trace.append(f"mw1:{event}")
        result = forward(event, payload)
        trace.append(f"mw1:post:{event}")
        return result

    def middleware_two(
        event: str,
        payload: dict[str, object],
        forward: Callable[[str, dict[str, object]], tuple[str, dict[str, object]]],
    ) -> tuple[str, dict[str, object]]:
        trace.append(f"mw2:{event}")
        return forward(event, payload)

    def handler(payload: Mapping[str, object]) -> None:
        trace.append(f"handler:{payload.get('value')}")

    bus.use(middleware_one)
    bus.use(middleware_two)
    bus.register_schema(
        "test",
        {
            "type": "object",
            "properties": {"value": {"type": "integer"}},
            "required": ["value"],
            "additionalProperties": False,
        },
    )
    bus.subscribe("test", handler)
    envelope = bus.publish("test", {"value": 3})

    assert trace == [
        "mw1:test",
        "mw2:test",
        "handler:3",
        "mw1:post:test",
    ]
    assert envelope is not None
    assert envelope.event == "test"
    assert dict(envelope.payload) == {"value": 3}
    assert bus.envelopes[-1] == envelope


def test_logging_middleware_records_payloads() -> None:
    bus = MessageBus()
    seen: dict[str, Mapping[str, object]] = {}

    def collector(event: str, payload: Mapping[str, object]) -> None:
        seen[event] = payload

    bus.use(LoggingMiddleware(collector))
    bus.publish("debate.finished", {"summary": "ok", "turns": 1})
    assert "debate.finished" in seen
    assert seen["debate.finished"]["summary"] == "ok"


def test_redaction_middleware_masks_payload_and_records() -> None:
    bus = MessageBus()
    bus.use(RedactionMiddleware({"debate.prompt": ["message.metadata.secret"]}))

    payload = {
        "message": {
            "role": "system",
            "content": "hello",
            "timestamp": "2024-01-01T00:00:00+00:00",
            "metadata": {"secret": "token"},
        }
    }
    envelope = bus.publish("debate.prompt", payload)
    assert envelope is not None
    redacted_message = envelope.payload["message"]
    assert isinstance(redacted_message, Mapping)
    assert redacted_message["metadata"]["secret"] == "***REDACTED***"
    assert envelope.redactions == ("message.metadata.secret",)

    summary = summarize(bus.envelopes)
    assert summary.redaction_counts == {"message.metadata.secret": 1}


def test_trace_builder_produces_serializable_output(tmp_path: Path) -> None:
    bus = MessageBus()
    bus.publish("debate.finished", {"summary": "done", "turns": 2})
    trace = build_trace(bus.envelopes)
    assert trace[0].to_dict()["event"] == "debate.finished"
    target = tmp_path / "trace.json"
    write_trace(bus.envelopes, target)
    written = json.loads(target.read_text(encoding="utf-8"))
    assert written[0]["event"] == "debate.finished"


def test_schema_enforcement() -> None:
    bus = MessageBus()
    with pytest.raises(jsonschema.exceptions.ValidationError):
        bus.publish("debate.finished", {"summary": "oops"})

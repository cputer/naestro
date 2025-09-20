from __future__ import annotations

from json import loads
from pathlib import Path
from sys import path as sys_path
from typing import Callable, Mapping

import pytest

try:
    from naestro.agents.schemas import new_message
    from naestro.core.bus import (
        LoggingMiddleware,
        MessageBus,
        RedactionMiddleware,
    )
    from naestro.core.summary import summarize
    from naestro.core.trace import build_trace, write_trace
except ModuleNotFoundError:  # pragma: no cover - defensive path setup
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    if str(PROJECT_ROOT) not in sys_path:
        sys_path.insert(0, str(PROJECT_ROOT))
    from naestro.agents.schemas import new_message
    from naestro.core.bus import (
        LoggingMiddleware,
        MessageBus,
        RedactionMiddleware,
    )
    from naestro.core.summary import summarize
    from naestro.core.trace import build_trace, write_trace

jsonschema = pytest.importorskip("jsonschema")


def test_message_bus_middleware_records_envelopes() -> None:
    bus = MessageBus()
    trace: list[str] = []

    def middleware_one(
        event: str,
        payload: dict[str, object],
        forward: Callable[[str, dict[str, object]], tuple[str, dict[str, object]]],
    ) -> tuple[str, dict[str, object]]:
        trace.append(f"mw1:{event}")
        forwarded = forward(event, payload)
        trace.append(f"mw1:post:{forwarded[0]}")
        return forwarded

    def middleware_two(
        event: str,
        payload: dict[str, object],
        forward: Callable[[str, dict[str, object]], tuple[str, dict[str, object]]],
    ) -> tuple[str, dict[str, object]]:
        trace.append(f"mw2:{event}")
        return forward(event, payload)

    def handler(payload: Mapping[str, object]) -> None:
        trace.append(f"handler:{payload['message']['role']}")

    bus.use(middleware_one)
    bus.use(middleware_two)
    bus.subscribe("debate.turn", handler)

    message = new_message("analyst", "ready", metadata={"round": 0, "order": 0})
    envelope = bus.publish(
        "debate.turn",
        {"message": message.to_dict(), "round": 0},
    )

    assert trace == [
        "mw1:debate.turn",
        "mw2:debate.turn",
        "handler:analyst",
        "mw1:post:debate.turn",
    ]
    assert envelope is not None
    assert envelope.sequence == 1
    assert envelope.event == "debate.turn"
    assert envelope.timestamp.isoformat() == "2024-01-01T00:00:00.001000+00:00"
    assert envelope.payload["message"]["metadata"]["round"] == 0
    assert "debate.turn" in bus.known_events


def test_middleware_forwarding_halt_propagates() -> None:
    bus = MessageBus()
    handled: list[Mapping[str, object]] = []
    calls: list[str] = []

    def outer_middleware(
        event: str,
        payload: dict[str, object],
        forward: Callable[[str, dict[str, object]], tuple[str, dict[str, object]]],
    ) -> tuple[str, dict[str, object]]:
        calls.append("outer:before")
        result = forward(event, payload)
        calls.append("outer:after")
        return result

    def halting_middleware(
        event: str,
        payload: dict[str, object],
        forward: Callable[[str, dict[str, object]], tuple[str, dict[str, object]]],
    ) -> None:
        calls.append("inner:halt")
        return None

    def handler(payload: Mapping[str, object]) -> None:
        handled.append(payload)

    bus.use(outer_middleware)
    bus.use(halting_middleware)
    bus.subscribe("debate.turn", handler)

    message = new_message("analyst", "ready", metadata={"round": 0, "order": 0})
    envelope = bus.publish(
        "debate.turn",
        {"message": message.to_dict(), "round": 0},
    )

    assert envelope is None
    assert calls == ["outer:before", "inner:halt", "outer:after"]
    assert handled == []
    assert bus.envelopes == ()


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

    message = new_message("system", "hello", metadata={"secret": "token"})
    envelope = bus.publish("debate.prompt", {"message": message.to_dict()})
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
    written = loads(target.read_text(encoding="utf-8"))
    assert written[0]["event"] == "debate.finished"


def test_schema_enforcement() -> None:
    bus = MessageBus()
    with pytest.raises(jsonschema.exceptions.ValidationError):
        bus.publish("debate.finished", {"summary": "oops"})

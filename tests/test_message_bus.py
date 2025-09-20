from __future__ import annotations

from typing import Callable, Dict, List

from naestro.core.bus import LoggingMiddleware, MessageBus


def test_message_bus_middleware_sequence() -> None:
    bus = MessageBus()
    trace: List[str] = []

    def middleware_one(
        event: str, payload: object, forward: Callable[[str, object], None]
    ) -> None:
        trace.append(f"mw1:{event}")
        forward(event, payload)
        trace.append(f"mw1:post:{event}")

    def middleware_two(
        event: str, payload: object, forward: Callable[[str, object], None]
    ) -> None:
        trace.append(f"mw2:{event}")
        forward(event, payload)

    def handler(payload: object) -> None:
        mapping = payload if isinstance(payload, dict) else {}
        trace.append(f"handler:{mapping.get('value')}")

    bus.use(middleware_one)
    bus.use(middleware_two)
    bus.subscribe("test", handler)
    bus.publish("test", {"value": 3})

    assert trace == [
        "mw1:test",
        "mw2:test",
        "handler:3",
        "mw1:post:test",
    ]


def test_logging_middleware() -> None:
    bus = MessageBus()
    seen: Dict[str, object] = {}

    def collector(event: str, payload: object) -> None:
        seen[event] = payload

    bus.use(LoggingMiddleware(collector))
    bus.publish("ping", {"payload": 1})
    assert "ping" in seen

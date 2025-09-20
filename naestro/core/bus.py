"""In-memory synchronous message bus with middleware support."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Protocol

Payload = object


class Middleware(Protocol):
    def __call__(
        self, event: str, payload: Payload, next_call: Callable[[str, Payload], None]
    ) -> None:
        """Process an event or pass it to the next middleware."""


Handler = Callable[[Payload], None]


class MessageBus:
    """Simple synchronous publish/subscribe bus."""

    def __init__(self) -> None:
        self._handlers: Dict[str, List[Handler]] = {}
        self._middleware: List[Middleware] = []

    def subscribe(self, event: str, handler: Handler) -> None:
        self._handlers.setdefault(event, []).append(handler)

    def use(self, middleware: Middleware) -> None:
        self._middleware.append(middleware)

    def publish(self, event: str, payload: Payload) -> None:
        def invoke_middleware(
            index: int, current_event: str, current_payload: Payload
        ) -> None:
            if index < len(self._middleware):
                middleware = self._middleware[index]
                middleware(
                    current_event,
                    current_payload,
                    lambda next_event, next_payload: invoke_middleware(
                        index + 1, next_event, next_payload
                    ),
                )
            else:
                for handler in self._handlers.get(current_event, []):
                    handler(current_payload)

        invoke_middleware(0, event, payload)

    def clear(self) -> None:
        self._handlers.clear()
        self._middleware.clear()


@dataclass
class LoggingMiddleware:
    """Middleware that mirrors events into a collector callable."""

    logger: Callable[[str, Payload], None]

    def __call__(
        self, event: str, payload: Payload, next_call: Callable[[str, Payload], None]
    ) -> None:
        self.logger(event, payload)
        next_call(event, payload)


__all__ = ["LoggingMiddleware", "MessageBus", "Middleware", "Payload"]

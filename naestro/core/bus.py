"""Deterministic in-memory message bus with schema enforcement."""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from importlib import resources
from json import dumps, load, loads
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping, MutableMapping, Protocol, Sequence

try:  # pragma: no cover - handled at runtime in MessageBus
    import jsonschema
except Exception as exc:  # pragma: no cover - lazy error in _SchemaCatalog
    raise RuntimeError(
        "naestro.core.bus requires jsonschema>=4.22. "
        "Install it with `pip install \"jsonschema>=4.22\"`."
    ) from exc

Payload = dict[str, object]


def _deep_copy(value: object) -> object:
    if isinstance(value, Mapping):
        return {str(key): _deep_copy(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_deep_copy(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_deep_copy(item) for item in value)
    return value


def _normalize_payload(payload: object) -> Payload:
    if isinstance(payload, Mapping):
        return {str(key): _deep_copy(value) for key, value in payload.items()}
    raise TypeError("MessageBus payloads must be mapping-like objects")


def _redact_path(value: object, parts: Sequence[str], replacement: object) -> bool:
    if not parts:
        return False
    head, *tail = parts
    if isinstance(value, MutableMapping):
        if head not in value:
            return False
        if not tail:
            value[head] = replacement
            return True
        return _redact_path(value[head], tail, replacement)
    if isinstance(value, list):
        try:
            index = int(head)
        except ValueError:
            return False
        if index < 0 or index >= len(value):
            return False
        if not tail:
            value[index] = replacement
            return True
        return _redact_path(value[index], tail, replacement)
    return False


def _apply_redactions(
    payload: Payload, paths: Sequence[str], replacement: object
) -> tuple[Payload, tuple[str, ...]]:
    if not paths:
        return payload, ()
    sanitized = _normalize_payload(payload)
    applied: list[str] = []
    for path in paths:
        if _redact_path(sanitized, path.split("."), replacement):
            applied.append(path)
    return sanitized, tuple(applied)


def _freeze_payload(payload: Payload) -> Mapping[str, object]:
    return MappingProxyType(
        {str(key): _deep_copy(value) for key, value in payload.items()}
    )


_ENVELOPE_CONTEXT: ContextVar[dict[str, list[str]] | None] = ContextVar(
    "_ENVELOPE_CONTEXT", default=None
)


def _record_redactions(redactions: Iterable[str]) -> None:
    context = _ENVELOPE_CONTEXT.get()
    if not context:
        return
    context.setdefault("redactions", []).extend(redactions)


def _load_default_schema() -> Mapping[str, Any]:
    package = resources.files(__package__)
    with package.joinpath("schemas.json").open("r", encoding="utf-8") as stream:
        return load(stream)


class _SchemaCatalog:
    def __init__(self, schema: Mapping[str, Any]) -> None:
        if jsonschema is None:  # pragma: no cover - dependency guard
            raise RuntimeError(
                "jsonschema is required to use the deterministic message bus"
            )
        if not isinstance(schema, Mapping):
            raise TypeError("schema must be a mapping")
        events = schema.get("events")
        if not isinstance(events, Mapping):
            raise ValueError("schema is missing an 'events' mapping")
        self._schema = dict(schema)
        self._event_schemas: dict[str, Mapping[str, Any]] = {}
        self._validators: dict[str, jsonschema.Validator] = {}
        resolver = jsonschema.RefResolver.from_schema(schema)
        base_cls = jsonschema.validators.validator_for(schema)
        base_cls.check_schema(schema)
        self._resolver = resolver
        for event, subschema in events.items():
            self.register(event, subschema)

    def register(self, event: str, schema: Mapping[str, Any]) -> None:
        if jsonschema is None:  # pragma: no cover
            raise RuntimeError(
                "jsonschema is required to register additional event schemas"
            )
        if not isinstance(event, str):
            raise TypeError("event names must be strings")
        if not isinstance(schema, Mapping):
            raise TypeError("event schema must be a mapping")
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)
        validator = validator_cls(schema, resolver=self._resolver)
        self._event_schemas[event] = dict(schema)
        self._validators[event] = validator

    def validate(self, event: str, payload: Mapping[str, object]) -> None:
        validator = self._validators.get(event)
        if validator is None:
            raise KeyError(f"unknown event '{event}'")
        validator.validate(payload)

    def schema_for(self, event: str) -> Mapping[str, Any]:
        if event not in self._event_schemas:
            raise KeyError(f"unknown event '{event}'")
        return self._event_schemas[event]

    @property
    def events(self) -> Sequence[str]:
        return tuple(sorted(self._event_schemas))


@dataclass(frozen=True, slots=True)
class Envelope:
    sequence: int
    event: str
    payload: Mapping[str, object]
    timestamp: datetime
    redactions: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "sequence": self.sequence,
            "event": self.event,
            "timestamp": self.timestamp.isoformat(),
            "payload": loads(dumps(self.payload, default=str)),
            "redactions": list(self.redactions),
        }


Forward = Callable[[str, Payload], tuple[str, Payload]]


class Middleware(Protocol):
    def __call__(
        self, event: str, payload: Payload, forward: Forward
    ) -> tuple[str, Payload] | None:
        ...


Handler = Callable[[Mapping[str, object]], None]


class MessageBus:
    """Synchronous deterministic bus backed by JSON Schema validation."""

    def __init__(
        self,
        *,
        schema: Mapping[str, Any] | None = None,
        base_timestamp: datetime | None = None,
    ) -> None:
        raw_schema = schema or _load_default_schema()
        self._catalog = _SchemaCatalog(raw_schema)
        self._handlers: dict[str, list[Handler]] = {}
        self._middleware: list[Middleware] = []
        self._envelopes: list[Envelope] = []
        self._sequence = 0
        self._base_timestamp = base_timestamp or datetime(
            2024, 1, 1, tzinfo=timezone.utc
        )

    def subscribe(self, event: str, handler: Handler) -> None:
        self._handlers.setdefault(event, []).append(handler)

    def use(self, middleware: Middleware) -> None:
        self._middleware.append(middleware)

    @property
    def known_events(self) -> Sequence[str]:
        return self._catalog.events

    def register_schema(self, event: str, schema: Mapping[str, Any]) -> None:
        self._catalog.register(event, schema)

    def publish(
        self, event: str, payload: Mapping[str, object] | object
    ) -> Envelope | None:
        normalized = _normalize_payload(payload)
        token = _ENVELOPE_CONTEXT.set({"redactions": []})
        try:
            final_event, final_payload, envelope, forwarded = self._dispatch(
                0, event, normalized
            )
            if not forwarded:
                return None
            if envelope is None:
                envelope = self._deliver(final_event, final_payload)
            return envelope
        finally:
            _ENVELOPE_CONTEXT.reset(token)

    def _deliver(self, event: str, payload: Payload) -> Envelope:
        self._catalog.validate(event, payload)
        context = _ENVELOPE_CONTEXT.get()
        redactions: tuple[str, ...] = ()
        if context:
            redactions = tuple(context.get("redactions", []))
        sequence = self._sequence + 1
        self._sequence = sequence
        timestamp = self._base_timestamp + timedelta(milliseconds=sequence)
        frozen_payload = _freeze_payload(payload)
        envelope = Envelope(
            sequence=sequence,
            event=event,
            payload=frozen_payload,
            timestamp=timestamp,
            redactions=redactions,
        )
        self._envelopes.append(envelope)
        for handler in self._handlers.get(event, []):
            handler(envelope.payload)
        return envelope

    def _dispatch(
        self, index: int, event: str, payload: Payload
    ) -> tuple[str, Payload, Envelope | None, bool]:
        if index >= len(self._middleware):
            envelope = self._deliver(event, payload)
            return event, payload, envelope, True
        forwarded = False
        final_event = event
        final_payload = payload
        envelope: Envelope | None = None

        def forward(next_event: str, next_payload: Payload) -> tuple[str, Payload]:
            nonlocal forwarded, final_event, final_payload, envelope
            forwarded = True
            final_event, final_payload, envelope, inner_forwarded = self._dispatch(
                index + 1, next_event, next_payload
            )
            if not inner_forwarded:
                forwarded = False
            return final_event, final_payload

        result = self._middleware[index](event, payload, forward)
        if result is not None:
            forwarded = True
            final_event, final_payload = result
            if envelope is None:
                envelope = self._deliver(final_event, final_payload)
        return final_event, final_payload, envelope, forwarded

    def clear(self) -> None:
        self._handlers.clear()
        self._middleware.clear()
        self._envelopes.clear()
        self._sequence = 0

    @property
    def envelopes(self) -> Sequence[Envelope]:
        return tuple(self._envelopes)


@dataclass(slots=True)
class LoggingMiddleware:
    """Middleware that mirrors events into a collector callable."""

    logger: Callable[[str, Mapping[str, object]], None]

    def __call__(
        self, event: str, payload: Payload, forward: Forward
    ) -> tuple[str, Payload] | None:
        self.logger(event, MappingProxyType(dict(payload)))
        return forward(event, payload)


class RedactionMiddleware:
    """Middleware that redacts configured keys from payloads."""

    def __init__(
        self,
        rules: Mapping[str, Sequence[str]] | Sequence[str],
        *,
        replacement: object = "***REDACTED***",
    ) -> None:
        if isinstance(rules, Mapping):
            self._rules = {str(event): tuple(paths) for event, paths in rules.items()}
        else:
            self._rules = {"*": tuple(rules)}
        self._replacement = replacement

    def __call__(
        self, event: str, payload: Payload, forward: Forward
    ) -> tuple[str, Payload] | None:
        paths = list(self._rules.get("*", ())) + list(self._rules.get(event, ()))
        if not paths:
            return forward(event, payload)
        sanitized, applied = _apply_redactions(payload, paths, self._replacement)
        if applied:
            _record_redactions(applied)
        return forward(event, sanitized)


def logging_mw(
    logger: Callable[[str, Mapping[str, object]], None]
) -> LoggingMiddleware:
    """Create a :class:`LoggingMiddleware` instance."""

    return LoggingMiddleware(logger)


def redaction_mw(
    rules: Mapping[str, Sequence[str]] | Sequence[str],
    *,
    replacement: object = "***REDACTED***",
) -> RedactionMiddleware:
    """Create a :class:`RedactionMiddleware` with ``rules``."""

    return RedactionMiddleware(rules, replacement=replacement)


__all__ = [
    "Envelope",
    "LoggingMiddleware",
    "MessageBus",
    "Middleware",
    "logging_mw",
    "RedactionMiddleware",
    "redaction_mw",
]

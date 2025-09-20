# Message Bus and Middleware

The :mod:`naestro.core.bus` module provides a synchronous publish/subscribe bus
with pluggable middleware. Middleware is ideal for logging, tracing and
instrumentation.

```python
from naestro.core.bus import LoggingMiddleware, MessageBus

bus = MessageBus()
trace: list[str] = []

bus.use(LoggingMiddleware(lambda event, payload: trace.append(event)))


def handler(payload: object) -> None:
    mapping = payload if isinstance(payload, dict) else {}
    trace.append(f"handled:{mapping.get('value')}")


bus.subscribe("demo", handler)
bus.publish("demo", {"value": 10})
print(trace)  # ['demo', 'handled:10']
```

Middleware receives the event name, payload and a `next_call` callback. It may
transform the payload or stop propagation entirely if needed. The message bus is
small enough to embed in tests and examples while still representing how Naestro
components communicate in production.

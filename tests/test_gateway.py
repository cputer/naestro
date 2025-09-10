import asyncio
import contextlib
import json
import statistics
import sys

import httpx
import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from src.gateway.main import app, sse_endpoint, websocket_endpoint


def test_health():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_orchestrate(monkeypatch):
    response_payload = {"result": "ok"}

    class DummyResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return response_payload

    class DummyAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, url, json):
            self.url = url
            self.sent = json
            return DummyResponse()

    monkeypatch.setattr(httpx, "AsyncClient", DummyAsyncClient)
    client = TestClient(app)
    resp = client.post("/orchestrate", json={"task": "demo"})
    assert resp.status_code == 200
    assert resp.json() == response_payload


def test_orchestrate_connection_error(monkeypatch):
    """Return 502 when orchestrator is unreachable."""

    class DummyAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, url, json):
            raise httpx.RequestError("boom", request=httpx.Request("POST", url))

    monkeypatch.setattr(httpx, "AsyncClient", DummyAsyncClient)
    client = TestClient(app)
    resp = client.post("/orchestrate", json={"task": "demo"})
    assert resp.status_code == 502
    assert resp.json() == {"error": "orchestrator unreachable"}


def test_orchestrate_missing_body():
    client = TestClient(app)
    resp = client.post("/orchestrate")
    assert resp.status_code == 422


def test_unknown_route():
    client = TestClient(app)
    resp = client.get("/doesnotexist")
    assert resp.status_code == 404


def test_system_metrics():
    client = TestClient(app)
    resp = client.get("/api/metrics/system")
    data = resp.json()
    assert resp.status_code == 200
    assert set(data.keys()) == {"cpu_percent", "memory_mb"}


def test_system_metrics_psutil_missing(monkeypatch):
    class MissingPsutil:
        def __getattr__(self, name):
            raise ImportError("psutil not installed")

    monkeypatch.setitem(sys.modules, "psutil", MissingPsutil())
    client = TestClient(app)
    resp = client.get("/api/metrics/system")
    assert resp.status_code == 200
    assert resp.json() == {"cpu_percent": 0.0, "memory_mb": 0.0}


def test_kpi_metrics(monkeypatch):
    class DummyResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"ok": True}

    class DummyAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, url, json):
            return DummyResponse()

    monkeypatch.setattr(httpx, "AsyncClient", DummyAsyncClient)
    client = TestClient(app)
    client.post("/orchestrate", json={"task": "demo"})  # generate metrics
    resp = client.get("/api/metrics/kpis")
    data = resp.json()
    assert resp.status_code == 200
    assert set(data.keys()) == {"latency_p95_ms", "throughput_rps"}


def test_kpi_metrics_quantile(monkeypatch):
    from src.gateway import main as gw

    class DummyResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"ok": True}

    class DummyAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, url, json):
            return DummyResponse()

    gw.REQUEST_LATENCIES[:] = []
    gw.REQUEST_COUNT = 0
    monkeypatch.setattr(httpx, "AsyncClient", DummyAsyncClient)

    client = TestClient(app)
    client.post("/orchestrate", json={"task": "demo"})
    client.post("/orchestrate", json={"task": "demo"})

    gw.REQUEST_LATENCIES[:] = [100.0, 1000.0]
    gw.REQUEST_COUNT = 2

    resp = client.get("/api/metrics/kpis")
    data = resp.json()
    expected = statistics.quantiles([100.0, 1000.0], n=100, method="inclusive")[94]
    assert resp.status_code == 200
    assert data["latency_p95_ms"] == pytest.approx(expected)


@pytest.mark.slow
def test_telemetry_streams(monkeypatch):
    class DummyResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"ok": True}

    class DummyAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, url, json):
            return DummyResponse()

    monkeypatch.setattr(httpx, "AsyncClient", DummyAsyncClient)
    client = TestClient(app)

    with client.websocket_connect("/ws") as ws:
        ws_data = ws.receive_json()

    with client.stream("GET", "/events") as resp:
        for line in resp.iter_lines():
            if line:
                assert line.startswith("data: ")
                sse_data = json.loads(line[6:])
                break

    assert set(ws_data.keys()) == {"timestamp", "system", "kpis"}
    assert ws_data.keys() == sse_data.keys()


@pytest.mark.slow
@pytest.mark.asyncio
async def test_websocket_endpoint_disconnect(monkeypatch):
    """websocket_endpoint should exit cleanly when client disconnects."""

    class DummyWebSocket:
        async def accept(self):
            pass

        async def send_json(self, data):
            raise WebSocketDisconnect()

        async def close(self):
            DummyWebSocket.closed = True

    ws = DummyWebSocket()
    await asyncio.wait_for(websocket_endpoint(ws), timeout=0.1)
    assert getattr(DummyWebSocket, "closed", False)


@pytest.mark.slow
@pytest.mark.asyncio
async def test_sse_endpoint_cancel(monkeypatch):
    """Cancelling the SSE generator should not leak CancelledError."""

    # Stub sleep so the generator awaits indefinitely until cancelled
    real_sleep = asyncio.sleep

    async def never_sleep(_):
        await asyncio.Event().wait()

    monkeypatch.setattr(asyncio, "sleep", never_sleep)

    resp = await asyncio.wait_for(sse_endpoint(), timeout=0.1)
    gen = resp.body_iterator
    await asyncio.wait_for(gen.__anext__(), timeout=0.1)  # prime generator

    task = asyncio.create_task(gen.__anext__())
    await real_sleep(0)
    task.cancel()
    with contextlib.suppress(asyncio.CancelledError, StopAsyncIteration):
        await asyncio.wait_for(task, timeout=0.1)
    assert not isinstance(task.exception(), asyncio.CancelledError)
    await gen.aclose()

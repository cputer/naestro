import httpx
from fastapi.testclient import TestClient
import json

from src.gateway.main import app


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
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, url, json):
            raise httpx.RequestError(
                "boom", request=httpx.Request("POST", url)
            )

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

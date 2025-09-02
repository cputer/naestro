import asyncio
import httpx
import pytest
from fastapi.testclient import TestClient

from src.gateway.main import app, sse_endpoint


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


def test_websocket_disconnect(monkeypatch):
    """WebSocket endpoint exits cleanly when client disconnects."""
    original_sleep = asyncio.sleep

    async def fast_sleep(_):
        await original_sleep(0.01)

    monkeypatch.setattr(asyncio, "sleep", fast_sleep)
    client = TestClient(app)

    with client.websocket_connect("/ws") as websocket:
        msg = websocket.receive_json()
        assert "heartbeat" in msg


def test_sse_disconnect(monkeypatch):
    """SSE generator handles cancellation when client disconnects."""

    async def runner():
        original_sleep = asyncio.sleep

        async def fast_sleep(_):
            await original_sleep(0.01)

        monkeypatch.setattr(asyncio, "sleep", fast_sleep)

        response = await sse_endpoint()
        gen = response.body_iterator

        first = await anext(gen)
        assert first.startswith("data: ")

        task = asyncio.create_task(anext(gen))
        await original_sleep(0.02)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:  # pragma: no cover - unexpected
            pytest.fail("CancelledError bubbled up")

    asyncio.run(runner())

from fastapi.testclient import TestClient

import src.gateway.main as gw
from src.gateway.main import app


def test_orchestrate_increments_metric(monkeypatch):
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

    gw.orchestrate_requests.reset()
    monkeypatch.setattr(gw.httpx, "AsyncClient", DummyAsyncClient)
    client = TestClient(app)
    resp = client.post("/orchestrate", json={"task": "demo"})
    assert resp.status_code == 200
    assert gw.orchestrate_requests.get() == 1


def test_telemetry_event_increments_metric():
    gw.telemetry_events.reset()
    gw._telemetry_event()
    assert gw.telemetry_events.get() == 1

import httpx
from fastapi.testclient import TestClient

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

def test_orchestrate_missing_body():
    client = TestClient(app)
    resp = client.post("/orchestrate")
    assert resp.status_code == 422


def test_unknown_route():
    client = TestClient(app)
    resp = client.get("/doesnotexist")
    assert resp.status_code == 404

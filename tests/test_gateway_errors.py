import httpx
from fastapi.testclient import TestClient

from src.gateway.main import app


def test_orchestrate_unreachable(monkeypatch):
    """Return an error when orchestrator call fails."""

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
    assert resp.status_code in (500, 502)
    assert "error" in resp.json()


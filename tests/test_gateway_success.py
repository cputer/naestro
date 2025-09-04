from fastapi.testclient import TestClient
import src.gateway.main as gw
from src.gateway.main import app


def test_orchestrate_success(monkeypatch):
    async def ok(task):
        return {"result": "ok", "steps": [], "tokens": 123}
    monkeypatch.setattr(gw, "orchestrate", ok)
    for route in app.router.routes:
        if getattr(route, "path", None) == "/orchestrate":
            route.endpoint = ok
            if hasattr(route, "dependant"):
                route.dependant.call = ok
            break
    cli = TestClient(app)
    resp = cli.post("/orchestrate", json={"prompt": "ping"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"] == "ok" and "steps" in data

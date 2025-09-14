from router.collab_policy import CollaborationMode
from router.router import Router
from src.telemetry import metrics


def test_router_records_metric():
    metrics.collab_routes.reset()
    router = Router(CollaborationMode.CONSULT)
    router.route(["a", "b"])
    assert metrics.collab_routes.get("consult") == 1

from router.collab_policy import CollaborationMode
from router.router import Router
from src.gateway.main import _telemetry_event
from src.prompt.composer import add_collab_headers
from src.telemetry import metrics


def _reset_metrics() -> None:
    metrics.collab_routes.reset()
    metrics.collab_prompts.reset()
    metrics.collab_prompt_depth.reset()
    metrics.telemetry_events.reset()


def test_collaboration_metrics_increment() -> None:
    _reset_metrics()

    router = Router(mode=CollaborationMode.COLLABORATE)
    router.route(["a", "b"])
    assert metrics.collab_routes.get("collaborate") == 1

    add_collab_headers("hi", {"mode": "collaborate", "depth": 2})
    assert metrics.collab_prompts.get("collaborate") == 1
    assert metrics.collab_prompt_depth.get("collaborate") == 2

    _telemetry_event()
    assert metrics.telemetry_events.get() == 1

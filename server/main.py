"""FastAPI application exposing orchestrator preference endpoints."""

from fastapi import FastAPI

from .orchestrator.prefs import OrchestratorPrefs, get_prefs, set_prefs

try:  # Import is optional to avoid hard dependency on plugin routes.
    from api.routes.plugins import router as plugins_router
except ModuleNotFoundError:  # pragma: no cover - defensive for optional wiring
    plugins_router = None

app = FastAPI(title="NAESTRO Server")

if plugins_router and getattr(plugins_router, "routes", None):
    app.include_router(plugins_router)


@app.get("/orchestrator/prefs", response_model=OrchestratorPrefs)
def read_prefs() -> OrchestratorPrefs:
    """Return currently stored orchestrator preferences."""

    return get_prefs()


@app.post("/orchestrator/prefs", response_model=OrchestratorPrefs)
def write_prefs(prefs: OrchestratorPrefs) -> OrchestratorPrefs:
    """Persist orchestrator preferences and echo the stored value."""

    return set_prefs(prefs)

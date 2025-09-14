"""FastAPI application exposing orchestrator preference endpoints."""

from fastapi import FastAPI

from .orchestrator.prefs import OrchestratorPrefs, get_prefs, set_prefs

app = FastAPI(title="NAESTRO Server")


@app.get("/orchestrator/prefs", response_model=OrchestratorPrefs)
def read_prefs() -> OrchestratorPrefs:
    """Return currently stored orchestrator preferences."""

    return get_prefs()


@app.post("/orchestrator/prefs", response_model=OrchestratorPrefs)
def write_prefs(prefs: OrchestratorPrefs) -> OrchestratorPrefs:
    """Persist orchestrator preferences and echo the stored value."""

    return set_prefs(prefs)

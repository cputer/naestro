"""Runtime preferences storage for the orchestrator service."""


from pydantic import BaseModel, ConfigDict


class OrchestratorPrefs(BaseModel):
    """User-customisable settings for the orchestrator.

    The model intentionally allows arbitrary keys so callers can persist any
    preference values they need without the server enforcing a schema.  This
    keeps the API flexible for experimentation while still benefiting from
    Pydantic's validation when structured data is supplied.
    """

    model_config = ConfigDict(extra="allow")


# in-memory preference store -------------------------------------------------

_current_prefs = OrchestratorPrefs()


def get_prefs() -> OrchestratorPrefs:
    """Return the currently stored preferences."""

    return _current_prefs


def set_prefs(prefs: OrchestratorPrefs) -> OrchestratorPrefs:
    """Replace the stored preferences with ``prefs`` and return the new value."""

    global _current_prefs
    _current_prefs = prefs
    return _current_prefs


def reset_prefs() -> OrchestratorPrefs:
    """Reset preferences to defaults and return the cleared value."""

    global _current_prefs
    _current_prefs = OrchestratorPrefs()
    return _current_prefs

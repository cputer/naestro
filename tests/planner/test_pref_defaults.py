from orchestrator.planner import DEFAULT_COLLAB_PREFS, clamp_prefs


def test_clamp_prefs_applies_defaults():
    prefs = {"mode": "solo"}
    clamped = clamp_prefs(prefs)
    for key, value in DEFAULT_COLLAB_PREFS.items():
        if key == "mode":
            assert clamped[key] == "solo"
        else:
            assert clamped[key] == value

"""Tests for the DeepCode adapter placeholder implementation."""

from integrations.plugins.deepcode_adapter import DeepCodeAdapter


def test_build_from_source_returns_placeholder_response():
    """The stub should emit the documented placeholder response."""
    adapter = DeepCodeAdapter({"token": "dummy"})
    source = {"branch": "main"}

    result = adapter.build_from_source(source)

    assert adapter.config == {"token": "dummy"}
    assert set(result) == {"status", "message", "source"}
    assert result["status"] == "not_wired"
    assert result["message"] == "DeepCode adapter is not wired yet"
    assert result["source"] == source

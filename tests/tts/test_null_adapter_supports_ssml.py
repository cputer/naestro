from src.voice.adapters.tts_null import NullTTSAdapter

def test_null_adapter_supports_ssml() -> None:
    adapter = NullTTSAdapter()
    assert adapter.supports_ssml() is True

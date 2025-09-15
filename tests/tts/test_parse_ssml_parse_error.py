from src.voice import parse_ssml


def test_parse_ssml_returns_original_on_parse_error():
    malformed = "<emphasis>oops"
    text, controls = parse_ssml(malformed)
    assert text == malformed
    assert controls == {}

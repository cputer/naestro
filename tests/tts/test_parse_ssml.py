import pytest

from src.voice import parse_ssml


def test_parse_ssml_malformed_returns_original_text():
    malformed = "<emphasis>oops"
    text, controls = parse_ssml(malformed)
    assert text == malformed
    assert controls == {}


def test_parse_ssml_break_with_invalid_time():
    text, controls = parse_ssml('<break time="oopsms"/>')
    assert text == ""
    assert controls == {}


def test_parse_ssml_appends_tail_text():
    text, controls = parse_ssml('<break time="1ms"/>after')
    assert text == "after"
    assert controls == {"break.ms": 1}

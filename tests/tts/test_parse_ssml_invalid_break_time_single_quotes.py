from src.voice import parse_ssml


def test_parse_ssml_break_with_invalid_time_single_quotes():
    text, controls = parse_ssml("<break time='oopsms'/>")
    assert text == ""
    assert controls == {}

from src.voice import parse_ssml


def test_parse_ssml_appends_tail_text_single_quotes():
    text, controls = parse_ssml("<break time='1ms'/>after")
    assert text == "after"
    assert controls == {"break.ms": 1}

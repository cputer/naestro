from src.utils import token


def test_tokens_round():
    assert token.round_tokens(0.0) == 0
    assert token.round_tokens(1.49) == 1
    assert token.round_tokens(1.50) == 2

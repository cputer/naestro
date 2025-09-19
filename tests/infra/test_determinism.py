"""Tests for the determinism utilities."""

from __future__ import annotations

import os

import pytest

from infra.determinism import enable


def test_enable_is_idempotent() -> None:
    """Calling ``enable`` with the same seed twice should be a no-op."""

    enable(0)
    enable(0)


def test_transformers_logits_repeatable() -> None:
    """Repeated transformer forward passes should produce identical logits."""

    torch = pytest.importorskip("torch")
    transformers = pytest.importorskip("transformers")

    model_name = os.environ.get("NAESTRO_TEST_MODEL")
    if not model_name:
        pytest.skip("NAESTRO_TEST_MODEL not set")

    enable(0)

    tokenizer = transformers.AutoTokenizer.from_pretrained(model_name)
    model = transformers.AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()

    device = torch.device("cpu")
    model = model.to(device)

    encoded = tokenizer("Deterministic inference.", return_tensors="pt")
    inputs = {key: value.to(device) for key, value in encoded.items()}

    with torch.no_grad():
        first_logits = model(**inputs).logits

    enable(0)

    with torch.no_grad():
        second_logits = model(**inputs).logits

    assert torch.allclose(first_logits, second_logits, atol=0.0, rtol=0.0)

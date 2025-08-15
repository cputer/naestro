import builtins
import importlib
import io
import json
import string

import pytest


def test_entropy_thresholds_and_flags(monkeypatch):
    # Prepare sample dataset with high and low entropy texts
    high_entropy_text = string.ascii_lowercase + string.digits  # 36 unique chars
    low_entropy_text = "a" * 20  # Single repeated char
    sample_data = [
        {"text": high_entropy_text, "label": "key"},
        {"text": low_entropy_text, "label": "email"},
    ]

    original_open = builtins.open

    def fake_open(path, *args, **kwargs):
        if str(path).endswith("pii_calib_set.json"):
            return io.StringIO(json.dumps(sample_data))
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", fake_open)
    module = importlib.reload(importlib.import_module("jobs.pii_calibrate"))

    assert module.calculate_shannon_entropy(high_entropy_text) > module.thresholds["high"]
    assert module.calculate_shannon_entropy(low_entropy_text) < module.thresholds["low"]
    assert module.data[0]["flag"] == "high"
    assert module.data[1]["flag"] == "low"

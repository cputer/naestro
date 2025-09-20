from __future__ import annotations

import importlib.util

import pytest


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if importlib.util.find_spec("torch") is None:
        skip = pytest.mark.skip(reason="requires torch")
        for item in items:
            if "test_hicra" in item.nodeid:
                item.add_marker(skip)

.PHONY: format lint typecheck test examples ci

format:
black naestro packs examples tests/test_debate_basic.py \
tests/test_roles_registry.py tests/test_message_bus.py \
tests/test_governor.py tests/test_router_selection.py \
tests/packs/trading/test_backtest_smoke.py \
tests/packs/trading/test_pipeline_debate_gate.py \
tests/conftest.py tests/training/__init__.py
ruff check --fix naestro packs examples \
tests/test_debate_basic.py tests/test_roles_registry.py \
tests/test_message_bus.py tests/test_governor.py \
tests/test_router_selection.py \
tests/packs/trading/test_backtest_smoke.py \
tests/packs/trading/test_pipeline_debate_gate.py \
tests/conftest.py tests/training/__init__.py

lint:
ruff check naestro packs examples \
tests/test_debate_basic.py tests/test_roles_registry.py \
tests/test_message_bus.py tests/test_governor.py \
tests/test_router_selection.py \
tests/packs/trading/test_backtest_smoke.py \
tests/packs/trading/test_pipeline_debate_gate.py \
tests/conftest.py tests/training/__init__.py

typecheck:
mypy --strict naestro packs examples

test:
pytest

examples:
python examples/debate_quickstart.py
python examples/governed_pipeline.py
python examples/routing_profiles.py
python examples/cli.py
python packs/trading/examples/aapl_demo.py

ci: format lint typecheck test examples

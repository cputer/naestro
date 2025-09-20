# Contributing to Naestro

- Use **Conventional Commits** (feat, fix, docs, refactor, perf, chore, ci, test, build).
- All PRs must pass CI and include docs when user-facing.
- Breaking changes: open an **RFC** issue before implementation.
- Add/update tests or validation scripts for logic changes.
- Keep `providers.yaml` schema-valid (`npm run validate:providers`).
- The canonical roadmap lives in `ROADMAP.md`; update it when changes affect project direction.

## Prerequisites

- Node.js 22 (see `.node-version` and `.nvmrc`; run `nvm use` or `fnm use` to switch automatically).

## Run the UI locally

```bash
cd ui
npm install
npm run dev
```

The dev server runs on <http://localhost:5173>. Set `VITE_SOCKET_BASE_URL` if your backend isn't at
`http://localhost:4000`.

## Run the server tests locally

```bash
npm test -C server
```

Runs the server's Vitest test suite.

### Pre-commit Hooks

We enforce ESLint/Prettier and other checks via [pre-commit](https://pre-commit.com/).

- This repo uses **Node 22** everywhere (`.nvmrc`, `.node-version`).
- Configure your shell to run `nvm use` or `fnm use` on entry so the correct version is loaded.
- To avoid `nodeenv` download issues, we configure pre-commit to use the **system Node**:

```yaml
default_language_version:
  node: system
```

Run once after cloning:

```bash
pre-commit install
pre-commit run --all-files
```

If nodeenv fails to fetch Node during setup, confirm you’re on Node 22 (`node -v`) and re-run with
system Node enabled.

## CI checks

The CI workflow installs Naestro with the development extras and runs linting, type
checking, tests, and a suite of smoke scripts. Reproduce the pipeline locally with:

```bash
python -m pip install --upgrade pip
python -m pip install .[dev]

ruff check naestro packs examples \
  tests/test_debate_basic.py tests/test_roles_registry.py \
  tests/test_message_bus.py tests/test_governor.py \
  tests/test_router_selection.py \
  tests/packs/trading/test_backtest_smoke.py \
  tests/packs/trading/test_pipeline_debate_gate.py \
  tests/conftest.py tests/training/__init__.py

black --check naestro packs examples \
  tests/test_debate_basic.py tests/test_roles_registry.py \
  tests/test_message_bus.py tests/test_governor.py \
  tests/test_router_selection.py \
  tests/packs/trading/test_backtest_smoke.py \
  tests/packs/trading/test_pipeline_debate_gate.py \
  tests/conftest.py tests/training/__init__.py

mypy --strict naestro packs examples

pytest

python examples/debate_quickstart.py
python examples/governed_pipeline.py
python examples/routing_profiles.py
python examples/cli.py
python packs/trading/examples/aapl_demo.py
```

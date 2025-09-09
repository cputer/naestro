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

The dev server runs on http://localhost:5173. Set `VITE_SOCKET_BASE_URL` if your backend isn't at `http://localhost:4000`.

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

If nodeenv fails to fetch Node during setup, confirm you’re on Node 22 (`node -v`) and re-run with system Node enabled.

## CI Profiles: Smoke vs Full Coverage

Run these commands locally to mirror the CI jobs:

- **UI smoke**: `npm ci -C ui && npm run test:smoke -C ui`
- **Python smoke**: `pytest -q -k "health or smoke"`
- **UI full**: `npm ci -C ui && CI=true npm run test:ci -C ui`
- **Python full**: `pytest -m "not slow" --maxfail=1 -q --durations=10 --cov=src --cov-report=xml --cov-fail-under=100`

Codecov uploads use flags `ui` and `python` with 100% targets.


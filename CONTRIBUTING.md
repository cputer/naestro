# Contributing to Naestro
- Use **Conventional Commits** (feat, fix, docs, refactor, perf, chore, ci, test, build).
- All PRs must pass CI and include docs when user-facing.
- Breaking changes: open an **RFC** issue before implementation.
- Add/update tests or validation scripts for logic changes.
- Keep `providers.yaml` schema-valid (`npm run validate:providers`).

## Prerequisites

- Node.js 22 (see `.node-version` and `.nvmrc`).

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


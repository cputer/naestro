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

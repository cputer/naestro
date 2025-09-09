# Apple Models as Sidecars in Naestro

Apple-linked research components are used as _sidecars_ to improve retrieval, routing, and UI
understanding:

- **DFN/CLIP variants** → image/doc embeddings for retrieval/rerank & dedupe.
- **OpenELM (small LMs)** → ultra-cheap router/filters.
- **Ferret-UI 2** → screenshot → structured UI elements for Studio action planning.

## Providers

See `config/providers.yaml` entries:

- `apple_dfn_clip` (HTTP sidecar, vision embeddings)
- `apple_openelm_router` (vLLM OpenAI-compatible text endpoint)
- `apple_ferret_ui` (HTTP sidecar, screenshot → UI elements)

## Running locally

- Vision sidecar: `python tools/vision/dfn_clip_server.py` (port 8601)
- UI adapter: `python tools/ui/ferret_adapter.py` (port 8603)
- Router: vLLM OpenAI server (port 8602) — see `docs/DEPLOY_SINGLE_NODE.md`.

## Usage in orchestration

- If a task includes images/screens: embed via DFN/CLIP → retrieve top-K → attach captions to
  proposer context.
- For Studio “screen actions”: Ferret-UI 2 extracts elements (bbox/label/action); the planner
  converts to clicks/typing.
- For routing: OpenELM labels task (code/web/ui/safety) to pick the best step mix.

Note: Judges/proposers remain your 70B/32B local models. Sidecars accelerate grounding and routing;
they don’t replace main LLMs.

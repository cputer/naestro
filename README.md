# NAESTRO — Orchestrator Platform

[![CI](https://github.com/cputer/naestro/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/cputer/naestro/actions/workflows/ci.yml) [![Release Please](https://github.com/cputer/naestro/actions/workflows/release-please.yml/badge.svg)](https://github.com/cputer/naestro/actions/workflows/release-please.yml) [![Coverage](https://codecov.io/gh/cputer/naestro/branch/main/graph/badge.svg)](https://codecov.io/gh/cputer/naestro)

<p align="center">
  <img src="docs/naestro-logo.svg" alt="NAESTRO Logo" width="300"/>
</p>

**Production-grade LLM orchestrator** with LangGraph-style workflow execution, pgvector-backed RAG,
secure sandboxing, and multi-model routing (NIM / vLLM / SLM).

Naestro is an AI Orchestrator for multi-model collaboration.

📖 Read the full [Whitepaper](./WHITEPAPER.md)

---

## Documentation
- **Whitepaper** → [WHITEPAPER.md](WHITEPAPER.md)
- **Architecture** → [ARCHITECTURE.md](ARCHITECTURE.md)
- **Single-node deployment (DGX Spark desktop)** → [docs/DEPLOY_SINGLE_NODE.md](docs/DEPLOY_SINGLE_NODE.md)
- **Multi-desktop (cells, router, queue)** → [docs/DEPLOY_MULTI_NODE.md](docs/DEPLOY_MULTI_NODE.md)
- **Apple sidecars (vision, routing, UI)** → [docs/APPLE_MODELS.md](docs/APPLE_MODELS.md)
- **Integrations (local-first stack, adapters, providers)** → [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md)
- **Graph Memory (Graphiti) guide** → [docs/GRAPHITI.md](docs/GRAPHITI.md)
- **Studio ↔ Core API contract (REST/WS/SSE, auth)** → [docs/UI_API_CONTRACT.md](docs/UI_API_CONTRACT.md)
- **VS Code add-on (Qoder-style) spec** → [docs/VS_CODE_EXTENSION.md](docs/VS_CODE_EXTENSION.md)
- **No-Replit deployment (Caddy + Cloudflare Tunnel)** → [docs/NO_REPLIT_DEPLOY.md](docs/NO_REPLIT_DEPLOY.md)

### Scale-out from single node
Naestro runs great on a single DGX Spark desktop. When you’re ready to expand across multiple desktops (“cells”), see **[DEPLOY_MULTI_NODE.md](docs/DEPLOY_MULTI_NODE.md)**. Cells register with the router; the scheduler places steps by VRAM headroom, temperature, and queue pressure—local-first with cloud spillover only when needed.

### Naestro Studio (local UI)
First-party dashboard (React + Vite + Tailwind + shadcn/ui) served by Naestro Core on the DGX.  \
Real-time Live Runs, model metrics, GPU health, KV cache hit-rate, cloud spillover %, and incidents.  \
See **[docs/UI_API_CONTRACT.md](docs/UI_API_CONTRACT.md)** and **[docs/DEPLOY_SINGLE_NODE.md](docs/DEPLOY_SINGLE_NODE.md)**.

To configure the WebSocket base URL during build, set `VITE_SOCKET_BASE_URL`:

```bash
VITE_SOCKET_BASE_URL=https://naestro.example.com npm run build
```

### VS Code Extension (Qoder-style)
A lightweight extension that talks to Naestro Core (`/api/runs`, `/ws/live`) to refactor code, explain errors, and generate tests **without leaving the IDE**.  \
Spec and scaffolding guidance in **[docs/VS_CODE_EXTENSION.md](docs/VS_CODE_EXTENSION.md)**.

## ✨ Features
- **Agentic Orchestration** — multi-phase workflows you can trace and audit.
- **Multi-Model Routing** — cost/latency-aware routes across NIM, vLLM, and a small model tier.
- **RAG on Postgres + pgvector** — BM25 + cosine + feedback reranker.
- **Secure Sandbox** — Docker-executed verification with seccomp + no-network.
- **PII Calibration** — Shannon entropy thresholds with a 550-item dataset.
- **Observability First** — OTEL traces, Prometheus metrics, Grafana dashboards (see `config/grafana/dashboards/naestro-dashboard.json`).
- **CI/CD** — GitHub Actions with healthchecks and hooks for shadow/canary logic.
- **Interactive Web UI** — Vite-powered React dashboard with Monaco editor for inspecting workflows, editing prompts, and monitoring runs.
- **SymPy & SciPy Demos** — example scripts for quadratic solving and sine integration.

See [docs/USER_MANUAL.md](docs/USER_MANUAL.md) for a complete manual.

## 🚀 Usage Scenarios
- **RAG-based question answering** — retrieve documents from Postgres + pgvector and synthesize answers through LangGraph-style workflows.
- **Multi-model routing** — pick between NIM, vLLM, and small language models based on cost or latency targets.
- **Sandbox verification for untrusted code** — execute user snippets inside a seccomp-restricted Docker container with no network access.

## Quick Start
```bash
# Core services (gateway, orchestrator, postgres, redis)
docker compose up -d --profile core

# Optional inference tier (requires GPU & NVIDIA NGC login)
docker compose up -d --profile inference

# Optional monitoring
docker compose up -d --profile monitoring

# Health checks
curl http://localhost:8080/health
curl http://localhost:8081/health
```

> **NVIDIA images:** If enabling the **inference** profile (NIM/SLM from `nvcr.io/*`), authenticate first:
> ```bash
> docker login nvcr.io
> # Use your NVIDIA NGC API key/token
> ```

## Local Development
```bash
pip install -r requirements.lock
pip install -r scripts/requirements.txt  # utilities like governor.py

# Start services directly (hot reload)
uvicorn src.orchestrator.main:app --reload --port 8081 &
uvicorn src.gateway.main:app --reload --port 8080 &
```

Dependencies are pinned for reproducibility. After editing any `requirements.txt`,
regenerate the corresponding `*.lock` file with `pip-compile`.

## Local-first DGX Spark (single node)
Naestro favors a local-first deployment model where all orchestrator and inference services run on a single DGX box with Spark. This setup targets self-contained experimentation and prototyping before any scale-out. For connector details see [docs/INTEGRATIONS.md](docs/INTEGRATIONS.md) and for memory semantics see [docs/GRAPHITI.md](docs/GRAPHITI.md). Studio and the VS Code extension are the official interfaces for interacting with this stack.

## DGX Spark Setup
- Use DGX OS (Ubuntu-based).
- Run `sudo apt install nvidia-slm-1.0` for SLM support.
- Execute `hardware/pin-resources.sh` for CPU/GPU pinning.
- Enable MIG with `sudo systemctl start mig-setup`.
- Validate the deployment with `./scripts/validate-dgx-deployment.js`.

## 🧰 Environment
Create a `.env` from the example:
```bash
cp .env.example .env
```
Key variables:
```
PG_DSN=postgresql://postgres:secure@postgres:5432/naestro
REDIS_URL=redis://redis:6379/0
ORCH_URL=http://orchestrator:8081
NIM_BASE_URL=http://nim:8000/v1
VLLM_BASE_URL=http://vllm:8000/v1
SLM_BASE_URL=http://slm:8000/v1
```

To point the gateway at a local orchestrator instead of the Compose service:
```bash
export ORCH_URL=http://localhost:8081
```
## Memory
Naestro now includes Graph Memory with Graphiti  → see [GRAPHITI](docs/GRAPHITI.md) for full overview and setup.

## 🗂 Structure
```
docs/                      # logo (SVG), diagrams
src/gateway/               # FastAPI entry service
src/orchestrator/          # Orchestrator service (workflow scaffold)
sql/schema.sql             # pgvector schema + indexes
etc/docker/sandbox/        # sandbox Dockerfile + seccomp
config/                    # prometheus + otel examples
config/grafana/            # Grafana dashboards
scripts/                   # DGX pinning, governor, validation
jobs/                      # PII calibration
.github/workflows/         # CI
.devcontainer/             # Codespaces dev environment
docker-compose.yml
ARCHITECTURE.md
```

## 🔬 Example Scripts
Sample SymPy and SciPy demonstrations live in `src/examples/`. See [docs/examples.md](docs/examples.md) for setup instructions and troubleshooting tips.

## 📄 Architecture
See **ARCHITECTURE.md** and **docs/architecture.mmd** (Mermaid).

## 🔒 Security
See **SECURITY.md**. Sandbox is network-isolated with a strict seccomp profile.

## 🧹 Pre-commit
Install the git hooks so formatting and lint checks run automatically:

```bash
pip install pre-commit
pre-commit install
```

## Testing
```bash
pre-commit run --files <file>
pytest
```

## 🤝 Contributing
Contributions are welcome! Please open an issue or pull request for any improvements or bug fixes. Please run the tests and linters before submitting.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

### Compatibility Matrix
| Component           | Version | Compatible With                          |
|--------------------|---------|------------------------------------------|
| Core Orchestrator  | v1.4.x  | Studio v0.9+, Providers schema v0.6+     |
| Studio (UI)        | v0.9.x  | Core v1.4+, Graphiti v0.3+               |
| Providers schema   | v0.6+   | Core v1.4+                               |

> Automated dependency updates via **Dependabot** are enabled (npm & GitHub Actions).

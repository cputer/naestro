# NAESTRO — Orchestrator Platform

[![CI](https://github.com/cputer/naestro/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/cputer/naestro/actions/workflows/ci.yml)

<p align="center">
  <img src="docs/naestro-logo.svg" alt="NAESTRO Logo" width="300"/>
</p>

**Production-grade LLM orchestrator** with LangGraph-style workflow execution, pgvector-backed RAG,
secure sandboxing, and multi-model routing (NIM / vLLM / SLM).

Naestro is an AI Orchestrator for multi-model collaboration.

📖 Read the full [Whitepaper](./WHITEPAPER.md)

---

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

## 📦 Quick Start (Docker)
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

**Local dev (no GPU / Codespaces):**
```bash
pip install -r requirements.lock
pip install -r scripts/requirements.txt  # utilities like governor.py

# Start services directly (hot reload)
uvicorn src.orchestrator.main:app --reload --port 8081 &
uvicorn src.gateway.main:app --reload --port 8080 &
```

Dependencies are pinned for reproducibility. After editing any `requirements.txt`,
regenerate the corresponding `*.lock` file with `pip-compile`.

## DGX Spark Setup
- Use DGX OS (Ubuntu-based).
- Run `sudo apt install nvidia-slm-1.0` for SLM support.
- Execute `hardware/pin-resources.sh` for CPU/GPU pinning.
- Enable MIG with `sudo systemctl start mig-setup`.

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

## 🗂 Structure
```
docs/                      # logo (SVG), diagrams
src/gateway/               # FastAPI entry service
src/orchestrator/          # Orchestrator service (workflow scaffold)
sql/schema.sql             # pgvector schema + indexes
etc/docker/sandbox/        # sandbox Dockerfile + seccomp
config/                    # prometheus + otel examples
config/grafana/            # Grafana dashboards
scripts/                   # DGX pinning, governor
jobs/                      # PII calibration
.github/workflows/         # CI
.devcontainer/             # Codespaces dev environment
docker-compose.yml
ARCHITECTURE.md
```

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

## 🤝 Contributing
Contributions are welcome! Please open an issue or pull request for any improvements or bug fixes.
Run formatting and lint checks before submitting:
```bash
pre-commit run --files <file>...
```
If your change touches code, execute the test suite:
```bash
pytest
```

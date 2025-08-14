# NAESTRO — Orchestrator Platform

<p align="center">
  <img src="docs/naestro-logo.svg" alt="NAESTRO Logo" width="300"/>
</p>

**Production-grade LLM orchestrator** with LangGraph workflow execution, pgvector-backed RAG, secure sandboxing,
and multi-model routing (NIM / vLLM / SLM).

---

## ✨ Features
- **LangGraph-based Orchestration** — multi-phase agent workflows you can trace and audit.
- **Multi-Model Routing** — cost/latency-aware routes across NIM, vLLM, and a small model tier.
- **RAG on Postgres + pgvector** — BM25 + cosine + feedback reranker.
- **Secure Sandbox** — Docker-executed verification with seccomp + no-network.
- **Observability First** — OTEL traces, Prometheus metrics, Grafana dashboards.
- **CI/CD** — GitHub Actions with shadow + canary rollouts (hooks provided).

## 📦 Quick Start (Docker)
```bash
# Core services (gateway, orchestrator, postgres, redis)
docker compose up -d --profile core

# Optional inference tier (requires GPU)
docker compose up -d --profile inference

# Health checks
curl http://localhost:8080/health
curl http://localhost:8081/health
```

## 🧰 Environment
Create a `.env` from the example:
```bash
cp .env.example .env
```

Key variables (also set in docker-compose):
```
PG_DSN=postgresql://postgres:secure@postgres:5432/naestro
REDIS_URL=redis://redis:6379/0
NIM_BASE_URL=http://nim:8000/v1
VLLM_BASE_URL=http://vllm:8000/v1
SLM_BASE_URL=http://slm:8000/v1
```

## 🗂 Structure
```
docs/                      # logo, diagrams
src/gateway/               # FastAPI entry service
src/orchestrator/          # Orchestrator service (LangGraph-ready scaffold)
sql/schema.sql             # pgvector schema + indexes
etc/docker/sandbox/        # sandbox Dockerfile + seccomp
config/                    # prometheus + otel examples
.github/workflows/         # CI
.devcontainer/             # Codespaces dev environment
docker-compose.yml
ARCHITECTURE.md
```

## 🧪 Dev (Codespaces)
- GPU inference isn’t available in Codespaces. The devcontainer starts a **mock inference** on `:9000` and runs gateway/orchestrator.
- Point to a remote inference stack by setting `NIM_BASE_URL`, `VLLM_BASE_URL`, `SLM_BASE_URL` in Codespaces secrets and rebuild the container.

## 🔒 Notes
- Replace `docs/naestro-logo.svg` with your real SVG (already in your GitHub repo).
- Keep `ARCHITECTURE.md` and diagrams in sync with implementation.
- License: MIT.

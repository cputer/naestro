# NAESTRO — Orchestrator Platform

[![CI Status](https://github.com/cputer/naestro/workflows/CI/badge.svg)](https://github.com/cputer/naestro/actions)


<p align="center">
  <img src="docs/naestro-logo2.svg" alt="NAESTRO Logo" width="300"/>
</p>

**Production-grade LLM orchestrator** with LangGraph-style workflow execution, pgvector-backed RAG,
secure sandboxing, and multi-model routing (NIM / vLLM / SLM).

---

## ✨ Features
- **Agentic Orchestration** — multi-phase workflows you can trace and audit.
- **Multi-Model Routing** — cost/latency-aware routes across NIM, vLLM, and a small model tier.
- **RAG on Postgres + pgvector** — BM25 + cosine + feedback reranker.
- **Secure Sandbox** — Docker-executed verification with seccomp + no-network.
- **Observability First** — OTEL traces, Prometheus metrics, Grafana dashboards.
- **CI/CD** — GitHub Actions with healthchecks and hooks for shadow/canary logic.

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
# Start services directly (hot reload)
uvicorn src.orchestrator.main:app --reload --port 8081 &
uvicorn src.gateway.main:app --reload --port 8080 &
```

## 🧰 Environment
Create a `.env` from the example:
```bash
cp .env.example .env
```
Key variables:
```
PG_DSN=postgresql://postgres:secure@postgres:5432/naestro
REDIS_URL=redis://redis:6379/0
NIM_BASE_URL=http://nim:8000/v1
VLLM_BASE_URL=http://vllm:8000/v1
SLM_BASE_URL=http://slm:8000/v1
```

## 🗂 Structure
```
docs/                      # logo (SVG), diagrams
src/gateway/               # FastAPI entry service
src/orchestrator/          # Orchestrator service (workflow scaffold)
sql/schema.sql             # pgvector schema + indexes
etc/docker/sandbox/        # sandbox Dockerfile + seccomp
config/                    # prometheus + otel examples
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
```bash
pip install pre-commit
pre-commit install
```

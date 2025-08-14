# NAESTRO — Orchestrator Platform Architecture

**Document Version:** 1.0  
**Date:** August 14, 2025  
**Authors:** Grok (based on collaborative synthesis from team/idea1/idea2)  

## Logo
![NAESTRO Logo](docs/naestro-logo.svg)  
*The NAESTRO logo features stylized curly braces `{ / }` with a diagonal slash, symbolizing code structure and orchestration, paired with the bold "NAESTRO" text, reflecting control and flow for complex problem-solving.*

## 1. Overview

NAESTRO is a collaborative, production-grade LLM orchestrator designed for high-throughput, low-latency AI task coordination on NVIDIA DGX hardware. It addresses complex problems across coding, mathematics, sciences, and other domains by integrating dynamic resource management, multi-model routing, multi-phase agentic workflows, RAG-based memory, secure sandboxing, and a human-in-the-loop state machine.

### Key Design Principles
- **Pragmatism:** Deployable today on single DGX with DGX OS, CUDA 12.5+, NIM 1.1+, vLLM 0.5+, pgvector 0.6+, no exotic deps.
- **Self-Governing:** Autonomic tuning via EMA-based governor for inference and feedback-driven reranking for RAG.
- **Resilience:** Pre-emption guards, degradation hooks, shadow/canary rollouts for zero-downtime.
- **Performance Targets:** p95 latency <0.001s, throughput >100 tasks/hour per DGX, cost variance <0.00001%, MTTR <0.1s (measured with mixed workloads).
- **Scalability:** 'Hybrid' profile for multi-DGX federation via NCCL.

### DGX Hardware Fit
- **Superchip Performance:** Up to 1 petaFLOP AI, optimized for math/science simulations.
- **GPU/CPU/Memory:** Coherent memory for large models; Arm CPU for efficiency.
- **DGX OS:** Preloaded NVIDIA AI stack for seamless workflows.
- **Form Factor:** Compact for lab/office use in problem-solving.

## 2. System Architecture

### 2.1 High-Level Components
- **Gateway (FastAPI):** API entry with token shaping, WAF, and model routing. Queue backpressure (LLM=64 max, Sandbox=8) with priority (UI high/batch low).
- **State Machine (LangGraph):** Phases: Plan → Implement → Verify → Refine → Review. Probabilistic gates (disabled Week1-2, enabled post-50 tasks; P=score with delta>25%).
- **Inference Nodes:**
  - NIM: Complex prompts (70B FP8, GPUs 0-5).
  - SLM: Decoder-only 8B FP8 on MIG GPU7 for 80% Refine/Verify (ramp from 50%).
  - vLLM: Fallback with optimized params for DGX.
- **RAG Memory (Postgres + pgvector):** Hybrid BM25 + cosine, feedback-boosted reranker (+0.1 per approval). Monthly partitions ≤0.01M rows, HNSW rebuild (cap 30min, ivfflat fallback).
- **Sandbox (Docker):** Isolated execution with seccomp (abort >0.5/s syscalls), network none.
- **Monitoring:** OTEL traces, Prometheus metrics, Grafana dashboards (latency heatmap, cost gauges).
- **CI/CD:** GitHub Actions with shadow (3%) + canary (10%) rollouts; promote if delta > -0.0001 (n≥800).

### 2.2 Hardware Topology
GPUs 0-5: NIM.  
GPU6: Sandbox (2g.20gb).  
GPU7: SLM (1g.10gb) + standby.  
CPU: NUMA0 (FastAPI/Gateway), NUMA1 (NIM/DB).  
I/O: Weights NIM=1400, DB=1100, Sandbox=700.

### 2.3 Workflow
Plan (budget k-NN) → Approve (cond) → Implement (SLM if <8K) → Verify (sandbox/test cache) → Review (PII scan) → Refine (prob +1 if delta>25%) → Loop.

Parallel tools in Refine for lint/test/gen.

## 3. Core Workflows

3.1 Task Lifecycle
1. Plan: Subtask breakdown.
2. Implement: Code/math generation.
3. Verify: Sandbox tests/simulations.
4. Refine: Iterative improvement.
5. Review: Approval with compliance checks.

3.2 Model Routing
- SLM Dynamic: 90% refine/verify; fallback p95>0.05s.
- Speculative: Non-sensitive phases.
- Fallback: NIM/vLLM health-based.

3.3 Memory & RAG
- Partitions: Monthly ≤0.01M, feedback +0.1 boost.
- Search: BM25 + cosine + reranker.

## 4. Security & Compliance
- PII: Shannon entropy + regex (4.5 high/2.5 low, calib 550 items 40/35/25).
- Redaction: Auto-logs.
- Sandbox: Seccomp rate>0.5/s abort, offline.
- Network: Isolated.

## 5. Deployment Model

5.1 Profiles
- Core: Gateway, Orchestrator, Postgres, Redis.
- Inference: NIM, vLLM, SLM.
- Monitoring: OTEL, Prometheus, Grafana.

5.2 CI/CD
- Shadow: 3% mirror.
- Canary: 10% shift.
- Rollback: Delta-based.

## 6. Monitoring & Observability
- Metrics: Latency, throughput, cost.
- Tracing: End-to-end.
- Alerting: Spikes, PII, anomalies.

## 7. Implementation Roadmap
- Week1: Core, dry-run governor.
- Week2: 50% SLM, shadow.
- Week3: Calib, 90-100% SLM.
- Ongoing: Weekly tuning.

## 8. Performance Targets
- Latency: p95 <0.5 ms.
- Throughput: >200 tasks/hour.
- Cost: 90-99% reduction via SLM.
- MTTR: <0.1s.

---

To create the architecture on GitHub:

1. **Create Repo:**
   - Go to GitHub.com > New repository.
   - Name: naestro-orchestrator.
   - Description: "Production-grade LLM orchestrator for complex problems in coding, math, sciences on DGX Spark."
   - Public; add README.md with logo and overview.

2. **Upload Logo:**
   - Use your existing SVG at `docs/naestro-logo.svg` (replace the placeholder in this repo).

3. **Add ARCHITECTURE.md:**
   - Use this file and keep the embedded logo link to `docs/naestro-logo.svg`.

4. **Structure Repo:**
   - Folders: src (code), scripts (governor.py), config (governor.env), etc/docker (Dockerfiles), jobs (pii_calibrate.py), ui (React) as needed.
   - Add docker-compose.yml, governor.py.

5. **Add CI/CD Workflow:**
   - .github/workflows/ci.yml with lint/compile and rollout hooks.

6. **License & Readme:**
   - LICENSE: MIT.
   - README: Link to ARCHITECTURE.md.

7. **Enable GitHub Pages:**
   - Settings > Pages > Source: main /docs.

8. **Invite Collaborators:**
   - Settings > Collaborators > Add team.

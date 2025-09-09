# NAESTRO Release v1.0

- Core components implemented (FastAPI gateway, LangGraph orchestrator, Docker sandbox).
- Added secondary language model (SLM) integration and GPU pinning.
- Included governor for dynamic inference tuning.
- PII detection calibration job added.
- 550-item calibration dataset for PII detection included.
- Expanded state machine with full workflow and probabilistic gating.
- Monitoring: Prometheus/Alertmanager configs for backlog/cost/latency.
- Grafana dashboard JSON for latency, GPU utilization, and cost heatmap.
- React UI scaffold for diffs and metrics.
- CI/CD pipeline now supports shadow testing and canary promotion logic.
- Hybrid RAG pipeline with BM25 + cosine search and feedback reranker.

- Updated gateway and orchestrator dependencies (FastAPI, redis, httpx, uvicorn, prometheus-client,
  python-dotenv) to their latest stable versions.
- Added explicit pins for sympy==1.14.0 and scipy==1.16.1 and generated requirements.lock files with
  `pip-compile`. To refresh locks after future upgrades, rerun:
  - `pip-compile requirements.txt -o requirements.lock`
  - `pip-compile src/gateway/requirements.txt -o src/gateway/requirements.lock`
  - `pip-compile src/orchestrator/requirements.txt -o src/orchestrator/requirements.lock`

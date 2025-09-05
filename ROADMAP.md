# Naestro Roadmap

_A living plan for Naestro — a local-first, cloud-augmented LLM orchestration platform that runs on a single NVIDIA DGX Spark (scalable to multiple desktops), coordinates top online models, controls agents, supports voice/vision/multilingual workflows, and maintains strict reliability & test coverage._

---

## 0) Principles

- **Local-first, cloud fallback:** keep latency/cost low on DGX; burst to cloud only for long-context or specialized tasks.  
- **Composable & pluggable:** models, tools, memory, retrieval, evaluators, and UIs are hot-swappable behind stable interfaces.  
- **Deterministic operations:** feature flags, circuit breakers, strict observability, canary rollouts, and 100% per-flag coverage.  
- **Human-in-the-loop (HITL):** every auto action has a pause/revise/resume path with diff and audit trails.  
- **Upgrade without fear:** self-improvement PRs gated by tests, reproducible benches, and instant rollback.

---

## 1) Target Runtime (Single DGX Spark → Multi-Desktop Scale)

- **Hardware baseline (single box):** 128 GB GPU mem, 64 CPU cores; optimized for 3 concurrent local models.  
- **Local model roster (production):**
  - **Llama-3.1-70B (TensorRT-LLM FP8/INT8)** — _Judge / Proposer_
  - **DeepSeek-V3.2-32B** — _Proposer / Synthesizer_
  - **Qwen-3-32B-AWQ** — _Critic / Code assistant_
- **Cloud fallbacks:** GPT-4/5 family, Claude 3.7+, Gemini 2.5+, Mistral Premium, Grok (latest), OpenELM (vLLM).  
- **Routing policy:** Judge local → spill to cloud on OOM or P95 latency breach; Proposer/Synth local; long-context or special tools → cloud.  

**Scale-out (multi-desktop):** labeled runners + job queue + distributed KV-cache; sticky sessions for workflow steps.

---

## 2) Agent Collaboration Model

- **Collab pipeline:** `propose → critique → synthesize → adjudicate`  
- **Consensus:** majority, weighted (per-agent historical win-rate), or single judge.  
- **Agent roles:** _Proposer_ (deep generation), _Critic_ (safety/correctness), _Synthesizer_ (merge/normalize), _Judge_ (final).  
- **HITL:** pause points, patch prompts, accept/override decisions, re-run.  

**Planned extensions**  
- **Crew orchestration:** CrewAI/AutoGen patterns for parallel branches and role chatter.  
- **Graph memory:** Graphiti for episodic + semantic memory graphs (each run becomes a subgraph with artifacts).  
- **ART (OpenPipe):** auto-reflexion/evaluators integrated into Judge step to harden prompts/programs over time.

---

## 3) Interop & External Ecosystem (New 2025 Integrations)

### 3.1 Model Context Protocol (MCP)  
Standard JSON-RPC to expose tools/data across vendors.  
- Add `mcp/` adapter (transport, discovery, auth, timeouts).  
- Feature flag: `MCP_ENABLED=true|false`.

### 3.2 Unified AI APIs (single key)  
Broker such as EdenAI (or equivalent) to normalize text/vision/speech.  
- Add `providers/edenai.ts` with cost/latency-aware routing.  
- Cost telemetry mapped into dashboard cards.

### 3.3 NVIDIA NeMo (optional enterprise backend)  
Microservices for custom agents on open-weights.  
- Add `integrations/nemo/` client; activate only if `NEMO_URL` set.  
- Use for specialized enterprise graphs or compliance-gated pipelines.

### 3.4 Agent Client Protocol (ACP) + IDE panels (Zed/VS Code)  
Embed Naestro Assistant into editors.  
- Add `integrations/acp/` server shim + commands: _orchestrate_, _explain_, _test_, _trace_.  
- Reuse Studio Live Monitor channels for in-IDE telemetry.

### 3.5 AMD Gaia (edge RAG for contributors)  
Local ONNX/Windows path to run RAG without DGX.  
- Add `integrations/gaia/` (optional), flag-gated.

### 3.6 AG-UI (CopilotKit-style)  
Thin web UI with SSE streaming for token/events.  
- Wire to Live Monitor; keep consistent UX with Studio.

---

## 4) Data Plane: Retrieval, Parsing, SEO & Geo

- **RAG:** thread-safe lazy init; FAISS/Milvus/pgvector; per-task context windows; policy-based truncation.  
- **Parsing:** robust DOM extraction, selector learning (CSS/XPath generalization), language/locale detection.  
- **SEO/Geo:** SERP pipelines, entity extraction, geocoding, locale-aware content rewrite.  
- **Structured I/O:** JSON schema validation with retry/backoff; OCR/PDF/LaTeX→JSON pipelines.  

**Unified “1-key” API hubs**  
- Adapters for hubs (e.g., RapidAPI/EdenAI bundles) with per-provider quotas and rate-limiters.

---

## 5) Voice / Vision / Multilingual

- **Voice (local-first):** Zonos/Vosk/Whisper chains; VAD, diarization; streaming transcribe & TTS.  
- **Multilingual:** region-specific models (e.g., Latam-GPT) included in routing policy.  
- **Vision:** image→JSON extract (tables/fields) with confidence thresholds and post-rules.

---

## 6) Naestro Studio (UI) & DevEx

- **Dashboard:** live runs, consensus %, cost, latency P50/P95, KV-cache hit, GPU memory/power/thermals.  
- **Artifacts:** prompts, responses, diffs, traces; run replay.  
- **Studio IDE:** code editor, prompt library, runbooks, workflow templates; “Open in Memory Graph” (Graphiti).  
- **CLI:** `naestro run`, `naestro bench`, `naestro judge`, `naestro trace`.

---

## 7) Reliability, Safety, Self-Improvement

- **Guardrails:** provider circuit breakers, thermal throttling, OOM recovery with step-level reroute; timeouts/retries/jitter.  
- **Self-improvement (safe):**
  - Scheduled “self-PRs” (lint, small refactors, prompt hardening) signed by Naestro,  
  - Fully gated by unit tests + 100% per-flag coverage + canary env,  
  - Single-click rollback; signed artifacts; audit trail.  
- **Policy:** PII scrubbing, configurable redaction, on-prem isolation mode.

---

## 8) Observability & Measurement

- **Metrics:** tok/s, latency P50/P95, success rate by task class, cost/tokens, KV-cache hit, GPU health.  
- **Tracing:** prompt/response spans, tool calls, network latencies; deterministic seeds when possible.  
- **Coverage:** per-flag 100% (UI/Python); project gate disabled until every area is 100%.

---

## 9) Performance

- **TensorRT-LLM:** FP8/INT8 for Llama-70B; batcher + KV-cache reuse; pinned memory.  
- **vLLM:** OpenELM/Gemma/GGUF for quick bring-up; set `--gpu-memory-utilization`.  
- **Mojo (future):** hot-path operators where Python is limiting.

---

## 10) Configuration Flags (initial)

MCP_ENABLED=true|false UNIFIED_AI_ENABLED=true|false EDENAI_API_KEY= ACP_ENABLED=true|false NEMO_URL= GAIA_ENABLED=true|false VOICE_ENABLED=true|false LOCAL_MODELS=llama-3.1-70b-fp8,deepseek-v3.2-32b,qwen-3-32b-awq CONCURRENCY_MAX=8 WS_HEARTBEAT_MS=20000

---

## 11) Milestones & Acceptance

### M1 — Interop & Coverage (Now)  
- MCP adapter (read-only tools)  
- EdenAI connector (unified APIs)  
- UI & Python flags at **100%** coverage; stable Codecov  
**Acceptance:** demos recorded; zero regressions; cloud spill only on long-context; guardrails firing as expected.

### M2 — IDE & Quality  
- ACP panel (Zed/VS Code)  
- AG-UI SSE integration  
- ART in Judge loop (auto-reflexion/evaluators)  
**Acceptance:** IDE quick-actions working; evaluator scores improving prompts/programs; canary passes.

### M3 — Enterprise & Edge  
- Optional NeMo backend  
- AMD Gaia path for local RAG  
- Expanded voice pipelines  
**Acceptance:** NeMo tasks verifiably routed; Gaia RAG reproduces core queries; voice latency within target.

### M4 — Scale & Autonomy  
- Multi-desktop orchestration  
- Safe self-PRs & rollbacks in production  
- Mojo pilot for hot paths  
**Acceptance:** distributed runs steady; self-PRs merged automatically with zero broken builds.

---

## 12) Contribution Notes

- **Tests:** MSW for UI, pytest for server; mock network by default; slow tests marked and skipped in smoke CI.  
- **CI:** split into smoke vs full coverage jobs; Codecov per-flag gates (UI, Python).  
- **Conventional commits** enforced on PR titles; pre-commit hooks with Node 22.

---

## 13) Open Integration Stubs (to implement in separate PRs)

- `integrations/mcp/` — transport, registry, feature flag, examples.  
- `providers/edenai.ts` — unified text/vision/speech with cost telemetry.  
- `integrations/acp/` — editor panel server shim + commands.  
- `integrations/nemo/` — optional client for enterprise agent graphs.  
- `integrations/gaia/` — edge RAG provider.

---

_This roadmap evolves continuously; each milestone includes explicit acceptance criteria, coverage requirements, and demo artifacts._


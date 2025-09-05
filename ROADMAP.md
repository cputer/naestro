# Naestro ROADMAP — Evolving Autonomous System

**North Star**  
Naestro grows from a goal-driven multi-agent orchestrator into a continuously self-improving autonomous system that can:
1) decompose open-ended goals into executable plans;  
2) coordinate local + cloud LLMs and tools;  
3) write, test, and ship production code;  
4) operate with strong safety, observability, and policy gates;  
5) self-improve via guarded self-edits validated by rigorous evaluations.

---

## 0) Current Status (Baseline)

- **Local-first model set (DGX Spark single node):**  
  Llama-3.1-70B (FP8 TRT-LLM) as Judge/Planner; DeepSeek-32B as Proposer/Synth; Qwen-32B-AWQ as Critic/Refactor.  
  Cloud spillover for long-context/specialty (GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, Apple OpenELM via vLLM).

- **Studio (Web UI):**  
  Real-time runs (WS/SSE), dark theme, run details & traces, metrics (latency, cost, success, KV cache hit, spillover %).

- **Quality gates:**  
  Node 22 standardization (.nvmrc/.node-version/CI containers); Conventional Commits automation; Release-Please; Codecov per-flag gates; 100% coverage for UI and growing Python coverage.

- **Guardrails:**  
  VRAM/thermal caps; retry/backoff; step-level re-route on OOM/timeouts; consent prompts for sensitive actions.

---

## 1) Target Properties

- **General goal execution:** natural-language objectives → typed plans (DAGs) with budgets/SLOs/acceptance checks.  
- **Model + tool orchestration:** choose best model/tool per step from live telemetry & historical win-rates.  
- **Formalized self-improvement:** scheduled self-PRs that increase pass-rates and reduce latency/cost.  
- **Safety-first autonomy:** well-scoped capabilities, consent layers, reversible changes.  
- **Observability & provenance:** all actions explainable, replayable, signed, and audited.

---

## 2) Logical Components

- **Planner** — Goal → `Plan.json` (tasks, deps, IO contracts, SLOs).  
- **Router** — Local-first selection with spillover based on latency/cost/context length & win-rates.  
- **Agents** — Researcher, Coder, Reviewer, Runner, DataOps, Evaluator, Reporter (spawned dynamically with scoped permissions).  
- **Policy Engine** — Tool/network/path allowlists, data scopes, rate limits, budget ceilings; emits consent prompts & audit events.  
- **Tool/Skill Registry** — Typed contracts (JSON Schema), versioned adapters (MCP/HTTP/CLI/DB/Browser/PDF/Vision/ASR/TTS/SEO/Geo).  
- **Memory Fabric (Graphiti)** — Episodic/semantic/skill memories with retrieval policies and graph structure.  
- **Evaluators** — Code/test/static/factuality/safety/latency/cost; pass@K; metamorphic/property tests.  
- **Introspector** — Summarizes failures, proposes prompt/route/tool improvements.  
- **Self-PR Bot** — Opens PRs (prompt hardening, router weights, tests, small refactors), runs canary, auto-merges if green.

---

## 3) Self-Rewrite Loop (Guarded)

**Collect → Propose → Validate → Canary → Merge → Learn**

- Collect: failed/slow traces, policy denials, evaluator misses, flaky tests.  
- Propose: minimal diffs only (prompt deltas, router weights, adapters, tests).  
- Validate: 100% coverage unit+property+metamorphic; golden prompt suites; offline replays.  
- Canary: shadow traffic; SLOs for success/latency/cost/safety; auto-rollback on breach.  
- Merge: signed artifacts, release notes, version bump.  
- Learn: update router priors from win-rates; store counter-examples.

*Non-goals:* unbounded self-modification, unsupervised secret/network access, or scope escalation.

---

## 4) Safety & Governance

- **Modes:** Guide (suggest), Copilot (confirm), Auto (approved scopes).  
- **Boundaries:**  
  - Secrets: short-lease vault; never to client; redaction in traces.  
  - Filesystem/network: path/domain allowlists; sandboxed exec; rate limits.  
  - Data: PII classifiers; off-prem toggle; export redaction.  
- **Kill switches:** pause runs; revoke tokens; quarantine tools/models.  
- **Compliance:** immutable audit logs; purpose/consent receipts.

---

## 5) Orchestration & Models

### Local (DGX Spark)
- Llama-3.1-70B FP8 TRT-LLM — Judge/Planner (batching, KV cache).
- DeepSeek-32B — Proposer/Synth (fast code/reasoning).
- Qwen-32B-AWQ — Critic/Refactor (low VRAM).

### Cloud Pool
- GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, Apple OpenELM (via vLLM).

### Routing policy
- Prefer local; spill to cloud for long context, specialty tools, or latency-SLO breaches.  
- Bandit-style updates from evaluator win-rates.

### vLLM Advanced Integration (New)
- **Paged Attention & Continuous Batching** — high concurrency for multi-agent runs.  
- **Prefix Caching** — accelerate shared-context workflows (e.g., SEO audits, PDF pipelines).  
- **Guided / Speculative Decoding** — n-gram, EAGLE, Medusa to reduce latency/cost.  
- **Disaggregated Prefill/Decode** — isolate long prefill from latency-sensitive decode.  
- **MultiProcExecutor + Data Parallel** — scale across GPUs/nodes; router-aware placement.  
- **Async serving** — integrate vLLM async APIs with Naestro Router; ZMQ/RPC under the hood.  
- **Auto-tuning** — use vLLM bench to learn throughput/latency profiles per model and update router.

---

## 6) Advanced Capabilities (Planned/Extending)

- **Voice I/O** — local ASR (Whisper-class) + multilingual NLU; TTS with streaming/barge-in; voice memory.  
- **Vision/PDF/LaTeX** — OCR → structured JSON; formula extraction; table/chart synthesis.  
- **SEO/Geo** — SERP/crawler parsers, sitemap audits, NER/geocoding, local ranking diffing; content/robots PRs.  
- **Prompt/Data-Ops** — prompt regression tracking (OpenPipe/ART-style), dataset curation, drift detection.  
- **Workflow Runtimes** — optional backends (LangGraph, CrewAI) governed by Naestro policies/router.  
- **Unified API Brokers** — single-key access to large tool catalogs (rate-limited, policy-enforced).  
- **Apple OpenELM via vLLM** — OpenAI-compatible local router for Apple models.  
- **OpenPipe ART** — prompt-ops & evaluation harness for regression safety across updates.

---

## 7) Observability & Metrics

- **Traces** — model, tokens, latency, cost, context, policy hits, memory IO, tool effects.  
- **Dashboards** — success/consensus rates, router win-rates, KV hit %, cloud spill %, anomalies, thermo/VRAM.  
- **Benchmarks** — task-specific suites; trendlines; SLO alerts; canary diffing.

---

## 8) Phased Delivery Plan

### Phase A (Weeks 1–6) — Planning, Router v1, Policies
- `schemas/plan.schema.json` (typed goal→plan contract)  
- `orchestrator/planner.py` (re-planning, failure handling)  
- Router v1 (heuristics: latency/cost/context length)  
- Policy engine (YAML rules, consent UI), deny/allow telemetry  
**Exit:** Multi-step tasks run with approvals; green CI; 100% coverage on new code.

### Phase B (Weeks 6–12) — Multi-Agent & Evaluators
- Dynamic role spawning/budgets; rate limiting  
- Evaluators: code/tests/static, factuality, safety; pass@K harness  
- Memory slices per role; link episodes in Graphiti  
**Exit:** Build-and-ship demo completes within SLA; evaluator-weighted routing improves success/latency.

### Phase C (Weeks 12–20) — Self-PRs & Canary
- Self-PR bot (prompt/router/config/test deltas), provenance signing  
- Canary + rollback scripts; changelog synthesis  
- Prompt/data-ops (golden suites; regression dashboards)  
**Exit:** Weekly self-PRs auto-merge when green; automatic rollback proven.

### Phase D (Weeks 20–28) — Multimodal & Domain Skills
- Voice I/O; PDF/LaTeX→tables; vision extraction  
- SEO/Geo tools; safe browsing policies; web automation  
- Cross-device sessions; artifact sharing  
**Exit:** Voice-driven plan edits; PDF→CSV/Charts works; SEO audits produce actionable PRs.

### Phase E (Ongoing) — Adaptive Router & Skill Induction
- Bandit router updates from evaluator win-rates  
- Distill frequent plans into typed, reusable **skills**  
- Public skill registry with safety metadata  
**Exit:** Faster plan convergence; lower tokens/success; richer toolchains with guardrails.

### F. Deep-Research Data Synthesis (InfoSeek-style)

**Goal:** Train a compact, local “InfoSeeker-7B” specialist that matches/beats larger generalists on web research tasks via curated browse traces.

**Deliverables**
- `tools/web_research/*` (SERP, browser, extractors, policies)
- `pipelines/infoseek/{collector,curator,grader,packager}.py`
- `train/infoseek_sft.py` (LoRA/QLoRA, optional DPO/RLAIF)
- `models/infoseeker/*` (vLLM config, AWQ quant)
- `eval/deep_research/*` (citation-aware benchmarks)

**Routing**
- Router prefers `infoseeker-*` for `capability: deep_research` when local VRAM permits; cloud spill for LC/XL context.

**Safety**
- robots.txt compliance, domain allowlist, PII redaction, consent receipts.
- Verifier pass (cross-model) before high-impact actions.

**Success criteria**
- ≥ X% improvement on citation-matched accuracy vs baseline.
- ≤ Y% hallucination/contradiction rate.
- 2–4× lower cost vs cloud model for same tasks.
---

## 9) Engineering Quality Gates (Always-On)

- **Coverage:** Per-area (UI/Server/Python) 100% with branch coverage; bootstrap files excluded.  
- **Static checks:** ESLint/TS-strict, mypy, Semgrep/Bandit, supply-chain scan.  
- **Tests:** Unit + property + metamorphic; MSW/network stubs; golden prompts.  
- **Repro:** Pinned versions & lockfiles; deterministic seeds; snapshot baselines.

---

## 10) File/Module Backlog (Next PRs)

- `schemas/plan.schema.json`  
- `orchestrator/planner.py` + tests  
- `router/policy.yaml` + `policy/engine.ts` + Studio consent banners  
- `registry/tools.json` + adapters (MCP/HTTP/CLI/DB/Browser/PDF/ASR/TTS/SEO/Geo)  
- `integrations/graphiti/*` writers/retrievers  
- `evaluators/*` harness (code/factuality/safety/latency/cost)  
- `self_pr/bot.ts` + `.github/workflows/canary.yml` + rollback  
- `voice/*` (ASR/TTS, streaming UI), `vision/*` (OCR/table/latex)  
- `studio/*` (Plan preview, policy notices, memory timeline, evaluator panels)  
- `inference/vllm/*` (speculative decoding, prefix cache, disaggregated P/D, auto-tuning)

_All new modules must ship with tests, docs, and coverage; merges blocked if any scope < 100%._

---

## 11) Example Use-Cases Unlocked

- End-to-end repo creation from spec (code, tests, CI, container, deploy, docs).  
- PDF/LaTeX data extraction to tables/charts with sanity checks.  
- SEO/Geo audits — crawl, analyze, propose changes, open PRs.  
- Voice-driven sprints — stand-ups, issue updates, PR summaries, plan edits.

---

## 12) Risk Register & Mitigations

- **Model drift/regression** → golden suites; canary + rollback; evaluator gating.  
- **Cost spikes** → local-first; budgets; adaptive routing; KV cache; batch.  
- **Data/secret exposure** → vault leases; redaction; allowlists.  
- **Over-autonomy** → mode gating; consent prompts; kill switches; strict policies.  
- **Supply-chain** → lockfiles; signature verification; SBOM (optional).

---

## 13) Appendices

**A. Local Models (DGX Spark)**  
- Llama-3.1-70B FP8 TRT-LLM — Judge/Planner  
- DeepSeek-32B — Proposer/Synth  
- Qwen-32B-AWQ — Critic/Refactor

**B. Cloud Pool**  
- GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, Apple OpenELM (vLLM)

**C. Key Integrations**  
- Graphiti (graph memory), LangGraph/CrewAI (optional runtime), OpenPipe/ART (prompt-ops), MCP (tool bus), unified API brokers (single-key), SEO/Geo toolkits, Apple OpenELM via vLLM.

---

## 14) Governance & Long-Term Direction

- **Evolving autonomy** under strict policy & consent layers.  
- **Self-improvement** is bounded by tests, evaluations, and canary health.  
- **Local-first** performance via vLLM and TRT-LLM, cloud when necessary.  
- **Reusability**: skills and plans become typed, cached, and shareable building blocks.

> This roadmap is a *living document*. As benchmarks, telemetry, and user feedback arrive, router policies, skill libraries, and evaluator weights will be updated continuously.
```
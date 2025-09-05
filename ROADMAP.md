# Naestro ROADMAP — Evolving Autonomous System (ASI Trajectory)

**North Star**  
Naestro evolves from a goal-driven multi-agent orchestrator into a continuously self-improving autonomous system that can: (1) decompose open-ended goals; (2) coordinate local+cloud LLMs and tools; (3) write, test, and ship production-quality code; (4) operate safely with strong observability and policy gates; (5) self-improve via guarded self-edits validated by rigorous evaluations.

---

## 0) Current Status (Baseline)

- **Local-first model set (DGX Spark single node):** Llama-3.1-70B (FP8 TRT-LLM) as Judge/Planner; DeepSeek-32B as Proposer/Synth; Qwen-32B-AWQ as Critic/Code. Cloud spillover for long-context/specialty tasks (GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM via vLLM).
- **Studio (Web UI):** Real-time runs (WS/SSE), dark theme, metrics (workflows, consensus, latency, KV cache hit, cost), run details and traces.
- **Guardrails:** Thermal/VRAM caps; step-level re-route on OOM/timeouts; retry/backoff; consent prompts for sensitive actions.
- **SDLC quality:** PR linting (commitlint), Release Please, Codecov with per-flag coverage, Node 22 standardization, deterministic UI+Python tests.

---

## 1) Target Properties (what “evolving ASI” means here)

1. **General goal execution** — Turn natural-language objectives into executable plans (DAGs) with budgets, SLAs, and success criteria.
2. **Model+tool orchestration** — Choose the right LLM(s)/tool(s) per step using live telemetry + historical win-rates.
3. **Formalized self-improvement** — Periodic self-proposals (self-PRs) that increase pass-rates, reduce latency/cost, and expand safe capability coverage.
4. **Safety-first autonomy** — Hard capability boundaries, consent layers, and provable rollback; humans remain in control of scopes and secrets.
5. **Observability & provenance** — Every action is explainable, replayable, and signed; drift and regressions are caught early.

---

## 2) System Roles (logical components)

- **Planner** — Compiles Goal → `Plan.json` (tasks, deps, inputs/outputs, budgets, acceptance checks).
- **Router** — Chooses model/provider per step (local vs cloud) using: win-rates, latency, context length, and cost.
- **Agents** — Role types: Researcher, Coder, Reviewer, Runner, DataOps, Evaluator, Reporter. Spawned dynamically with scoped permissions.
- **Policy Engine** — Enforces tool/network/path allowlists, data scopes, rate limits, and cost/time ceilings. Produces consent prompts and audit events.
- **Tool/Skill Registry** — Typed contracts (JSON Schema), versioned adapters (MCP/HTTP/CLI/DB/Browser/PDF/Vision/ASR/TTS/SEO/Geo), deprecation paths.
- **Memory Fabric** — Episodic (runs), semantic (facts/summaries), skill memories (reusable flows), user prefs. Graph-structured (Graphiti) with retrieval policies.
- **Evaluators** — Code/test/typing/static analysis; factuality/consistency; safety; latency/cost; pass@K; metamorphic/program properties.
- **Introspector** — Summarizes failures, extracts lessons, proposes prompt/route/tool upgrades (feeds Self-PR cycle).
- **Self-PR Bot** — Opens PRs (prompt hardening, flaky test fixes, router weights, small refactors), runs canary, signs artifacts, auto-merges if green.

---

## 3) Self-Rewrite Loop (guarded autonomy)

1. **Collect**: Surfacing failures (dropped runs, OOM, policy denials), slow traces (P95 spikes), evaluator misses, flaky tests.
2. **Propose**: Agents generate *minimal* diffs (prompt deltas, router weights, tool config, tests) → PRs.
3. **Validate**:  
   - Unit + property + metamorphic tests (100% coverage).  
   - Golden prompts via prompt-ops (regression suites).  
   - Offline dataset replays; synthetic task suites (coding, agentic, PDF/LaTeX, SEO/Geo, browse).  
4. **Canary**: Shadow traffic; watch SLOs (success, latency, cost, safety incidents). Automatic rollback if any breach.
5. **Merge**: Provenance sign, release notes, version bump.  
6. **Learn**: Update router priors from win-rates; store counter-examples in memory for future planning.

**Non-goals**: unrestricted self-modification, unsupervised network/file access, or secret exfiltration.

---

## 4) Safety & Capability Governance

- **Modes**: `Guide` (suggest), `Copilot` (confirm), `Auto` (approved scopes only).
- **Boundaries**:  
  - Secrets: lease-scoped vault; never to client; redaction in traces.  
  - Filesystem & network: path/domain allowlists; sandboxed exec; rate limits.  
  - Data: PII classifiers; off-prem toggle; export redaction.  
- **Kill switches**: Pause runs; revoke tokens; quarantine models/tools.
- **Compliance**: comprehensive audit logs (immutable), purpose/consent receipts.

---

## 5) Orchestration & Models

- **Local (DGX Spark)**  
  - Llama-3.1-70B FP8 TRT-LLM: Judge/Planner (batching, KV cache).  
  - DeepSeek-32B: Proposer/Synth (fast code/reasoning).  
  - Qwen-32B-AWQ: Critic/Refactor (low VRAM).  
- **Cloud**  
  - GPT-4/5-class (general), Claude 3.7+ (long reasoning), Gemini-2.5+ (long-context/multimodal), Mistral/Grok/OpenELM.  
- **Routing policy**  
  - Prefer local; spill to cloud on long context, specialty tools, or latency SLO breaches.  
  - Bandit-style updates from evaluators’ win-rates.

---

## 6) Advanced Capabilities (to integrate)

- **Voice**: Local ASR (e.g., Zonos/Whisper-class), multilingual NLU; TTS output; streaming barge-in; voice memory.
- **Vision/PDF**: OCR tables → structured JSON; formula/LaTeX extraction; chart/table synthesis.
- **SEO/Geo**: Crawler/SERP parsers, sitemap audits, NER/geocoding, local ranking diffing; content/robots PRs.
- **Prompt/Data-Ops**: Prompt regression tracking (e.g., ART-style), dataset curation, result drift detection.
- **Workflow Runtimes**: Interop with LangGraph/CrewAI as optional backends for complex tool flows (still governed by Naestro policy/router).
- **Unified API brokers**: “Single-key” providers for broad tool coverage (rate-limited through policy engine).

---

## 7) Observability & Metrics

- **Traces**: model, tokens, latency, cost, context, policy hits, memory I/O, tool effects.
- **Dashboards**: success & consensus rates, router win-rates, KV hit %, cloud spill %, anomaly flags, thermo/VRAM.
- **Benchmarks**: project-specific regression suites; public benchmarks proxied via adapters; trendlines and SLA alerts.

---

## 8) Phased Delivery Plan

### Phase A (Weeks 1–6): Autonomous Planning & Policies
- `schemas/plan.schema.json` (typed contract)
- `orchestrator/planner.py` (goal→plan compiler, re-planning)
- `policy/engine` (YAML rules, consent UI), deny/allow telemetry
- Router v1 (heuristics: latency/cost/context)
**Exit**: Complex multi-step tasks run with approvals; green CI; 100% coverage on new code.

### Phase B (Weeks 6–12): Multi-Agent Programs & Evaluators
- Dynamic role spawning/budgets; rate limiting
- Evaluators: code/tests/static, factuality, safety; pass@K harness
- Memory slices per role; episode linking in Graphiti
**Exit**: End-to-end build-and-ship demo finishes within SLA; evaluator-weighted routing improves success/latency.

### Phase C (Weeks 12–20): Self-PRs & Canary Rollouts
- Self-PR bot (prompt/router/config/test deltas), provenance signing
- Canary+rollback scripts; changelog synthesis
- Prompt/data-ops (golden suites; regression dashboards)
**Exit**: Weekly self-PRs auto-merge ≥90% without regressions; clear rollback proofs.

### Phase D (Weeks 20–28): Multimodal & Domain Skills
- Voice I/O; PDF/LaTeX→tables; vision extraction
- SEO/Geo skills; browser tools & safe browsing policies
- Cross-device sessions; artifact sharing
**Exit**: Voice-driven plan edits; PDF→CSV/Charts works; SEO audits produce actionable PRs.

### Phase E (Ongoing): Adaptive Router & Skill Induction
- Bandit router updates from evaluator win-rates
- Distill frequent plans into typed, reusable “skills”
- Public “skill market” with safety metadata
**Exit**: Faster convergence on plans; fewer tokens per success; richer toolchain with guardrails.

---

## 9) Engineering Quality Gates (always-on)

- **Coverage**: Per-area (UI/Server/Python) 100% with branch coverage and exclusions only for bootstrap.
- **Static checks**: TS strict/mypy, ESLint, Semgrep/Bandit, supply-chain scan, IaC lint if infra present.
- **Tests**: Unit + property + metamorphic; MSW/network stubs; golden prompt suites.
- **Repro**: Pinned versions; snapshots for plans & prompts; deterministic seeds.

---

## 10) File/Module Backlog (next PRs)

- `schemas/plan.schema.json`
- `orchestrator/planner.py` + tests
- `router/policy.yaml` + `policy/engine.ts` + Studio consent banners
- `registry/tools.json` + adapters (MCP/HTTP/CLI/DB/Browser/PDF/ASR/TTS)
- `integrations/graphiti/*` writers/retrievers
- `evaluators/*` harness (code/factuality/safety/latency/cost)
- `self_pr/bot.ts` + `.github/workflows/canary.yml` + rollback
- `voice/*` (ASR/TTS, streaming UI), `vision/*` (OCR/table/latex)
- `studio/*` (Plan preview, policy notices, memory timeline, evaluator panels)

_All new modules must ship with tests, docs, and coverage; merges blocked if any scope <100%._

---

## 11) Example Use-Cases Unlocked

- **End-to-end repo creation** from a spec (code, tests, CI, container, deploy, docs).
- **PDF data extraction** (financial/maths) to tables/charts with sanity checks.
- **SEO/Geo audits** — crawl, analyze, propose changes, open PRs.
- **Voice-driven sprints** — stand-ups, issue updates, PR summaries, plan edits.

---

## 12) Risk Register & Mitigations

- **Model drift / regression** → Golden suites, canary + rollback, evaluator gating.
- **Cost spikes** → Local-first, budgets, adaptive routing, KV cache, batch.
- **Data/secret exposure** → Vault leases, redaction, path/domain allowlists.
- **Over-autonomy** → Mode gating, consent prompts, kill switches, strict policies.
- **Supply-chain** → Lockfiles, signature verification, SBOM (optional).

---

### Appendices

**A. Local Models (DGX Spark)**  
- Llama-3.1-70B FP8 TRT-LLM — Judge/Planner  
- DeepSeek-32B — Proposer/Synth  
- Qwen-32B-AWQ — Critic/Refactor

**B. Cloud Pool**  
- GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM via vLLM

**C. Key Integrations**  
- Graphiti (memory graphs), LangGraph/CrewAI (optional runtime), prompt/data-ops (ART-style), Zonos (voice), MCP (tool bus), unified API brokers (single-key), SEO/Geo toolkits.

---
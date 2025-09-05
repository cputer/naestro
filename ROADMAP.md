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

## 3) Mermaid: Orchestrator Map

```mermaid
flowchart TB
    subgraph Studio["Studio (Web UI)"]
      UI[Runs/Traces/Metrics]
      Consent[Consent Banners]
      Panels[Nango SaaS Panel & n8n Export]
    end

    subgraph Core["Naestro Core"]
      Planner
      Router
      Policy[Policy Engine]
      Registry[Tool/Skill Registry (MCP, HTTP, DB, Browser, PDF, ASR/TTS, SEO/Geo, n8n, Nango)]
      Memory[Graphiti Memory Fabric]
      Evaluators
      Introspector
      SelfPR[Self-PR Bot]
    end

    subgraph Engines["Serving Engines"]
      VLLM[vLLM / SGLang]
      TRTLLM[TensorRT-LLM]
      Triton[Triton Inference Server]
    end

    subgraph ModelsLocal["Local Models (DGX Spark)"]
      Llama[Llama-3.1-70B FP8]
      DeepSeek[DeepSeek-32B]
      Qwen[Qwen-32B-AWQ]
      GPTOSS[GPT-OSS 20B/120B]
    end

    subgraph Cloud["Cloud Pool"]
      OpenAI[GPT-4/5 class]
      Claude[Claude 3.7+]
      Gemini[Gemini-2.5+]
      Mistral[Mistral/Grok/OpenELM]
      LFM2[LFM2-350M (JP↔EN)]
    end

    subgraph Integrations["Integrations"]
      MCP[MCP Client/Server]
      Parlant[Parlant + VibeVoice (ASR/TTS)]
      n8n[n8n Flow Export]
      Nango[Nango SaaS API Hub]
      ART[ART Prompt-Ops]
      Tensorlake[Tensorlake Metadata-RAG]
      OmniNova[OmniNova (Planner/Critic)]
      Symphony[Symphony (Decentralized)]
      OCA[Open Computer Agent (Browser/UI)]
      LMCache[LMCache/NIXL KV-Transfer]
    end

    Studio --> |WS/SSE| Core
    Panels --> Registry

    Planner --> Router
    Router --> |selects| Engines
    Policy --> |gates| Router
    Registry --> Agents
    Agents --> Engines
    Agents --> Memory
    Engines --> ModelsLocal
    Engines --> Cloud

    Evaluators --> Introspector
    Introspector --> SelfPR
    SelfPR --> |PRs| Studio

    ART --> Evaluators
    Tensorlake --> Memory
    MCP --> Registry
    n8n --> Registry
    Nango --> Registry
    Parlant --> Registry
    OCA --> Registry
    LMCache --> Engines
```

---

## 4) Self-Rewrite Loop (guarded autonomy)

1. **Collect**: Surfacing failures (dropped runs, OOM, policy denials), slow traces (P95 spikes), evaluator misses, flaky tests.  
2. **Propose**: Agents generate *minimal* diffs (prompt deltas, router weights, tool config, tests) → PRs.  
3. **Validate**:  
   - Unit + property + metamorphic tests (**100% coverage**).  
   - Golden prompts via prompt-ops (**ART integration**).  
   - Offline dataset replays; synthetic task suites (coding, agentic, PDF/LaTeX, SEO/Geo, browse).  
4. **Canary**: Shadow traffic; watch SLOs (success, latency, cost, safety incidents). Automatic rollback if any breach.  
5. **Merge**: Provenance sign, release notes, version bump.  
6. **Learn**: Update router priors from win-rates; store counter-examples in memory for future planning.  

**Non-goals**: unrestricted self-modification, unsupervised network/file access, or secret exfiltration.

---

## 5) Safety & Capability Governance

- **Modes**: `Guide` (suggest), `Copilot` (confirm), `Auto` (approved scopes only).  
- **Boundaries**:  
  - Secrets: lease-scoped vault; never to client; redaction in traces.  
  - Filesystem & network: path/domain allowlists; sandboxed exec; rate limits.  
  - Data: PII classifiers; off-prem toggle; export redaction.  
- **Kill switches**: Pause runs; revoke tokens; quarantine models/tools.  
- **Compliance**: comprehensive audit logs (immutable), purpose/consent receipts.

---

## 6) Orchestration & Models

- **Local (DGX Spark)**  
  - Llama-3.1-70B FP8 TRT-LLM: Judge/Planner (batching, KV cache).  
  - DeepSeek-32B: Proposer/Synth (fast code/reasoning).  
  - Qwen-32B-AWQ: Critic/Refactor (low VRAM).  
  - **GPT-OSS** 20B/120B: open GPT-level local-first options.

- **Cloud**  
  - GPT-4/5-class (general), Claude 3.7+ (long reasoning), Gemini-2.5+ (long-context/multimodal), Mistral/Grok/OpenELM.  
  - **LFM2-350M** (JP↔EN) for efficient high-quality translation.

- **Routing policy**  
  - Prefer local; spill to cloud on long context, specialty tools, or latency SLO breaches.  
  - Bandit-style updates from evaluators’ win-rates.  
  - **Reasoning budget knobs** (think/on/off; effort levels) normalized across providers.

---

## 7) Advanced Capabilities (to integrate)

- **Voice**: **Parlant** + Whisper/Zonos, **VibeVoice** (long-form/emotional TTS), multilingual ASR, streaming TTS, barge-in, voice memory.  
- **Vision/PDF**: OCR tables → structured JSON; formula/LaTeX extraction; chart/table synthesis.  
- **SEO/Geo**: Crawler/SERP parsers, sitemap audits, NER/geocoding, local ranking diffing; content/robots PRs.  
- **Prompt/Data-Ops**: **ART** prompt regression tracking, dataset curation, result drift detection.  
- **Workflow Runtimes**: Interop with **LangGraph/CrewAI** as optional backends for complex tool flows (still governed by Naestro policy/router).  
- **Unified API brokers**: Single-key providers for broad API/tool coverage (RapidAPI-style).  
- **n8n Integration**: Export Naestro workflows to **n8n YAML**, enabling low-code automation (email agents, Telegram bots, Reddit pipelines).  
- **Translation**: **LFM2-350M** integration for efficient JP↔EN translation.  
- **vLLM Enhancements**: Paged attention, prefix caching, speculative decoding, multi-GPU/multi-node serving with auto-tuning.  
- **Elastic scaling**: **LMCache/NIXL** connectors for KV-cache transfer across nodes, disaggregated prefill/decode pipelines.  
- **Metadata RAG**: **Tensorlake**-style metadata enrichment for embeddings; classifying pages (tables/text/terms) to pre-filter retrieval.  
- **MCP (Model Context Protocol)**: Standardized tool & data connectors (client+server).  
- **Open Computer Agent**: Headless browser/UI automation for real-world tasks (SEO/Geo ops).  
- **OmniNova** / **Symphony**: Agent orchestration/consensus frameworks (optional adapters).  
- **Nango SaaS Hub**: 400+ SaaS APIs (CRM/HR/Finance/etc.) via one OAuth, with Studio panel & n8n autogen nodes.

---

## 8) Observability & Metrics

- **Traces**: model, tokens, latency (TTFT/ITL), cost, context, policy hits, memory I/O, tool effects.  
- **Dashboards**: success & consensus rates, router win-rates, KV hit %, cloud spill %, anomaly flags, thermo/VRAM.  
- **Benchmarks**: project-specific regression suites; public benchmarks proxied via adapters; trendlines and SLA alerts (SWE-bench Verified, LiveBench).  
- **OpenTelemetry GenAI** semantic conventions as first-class.

---

## 9) Phased Delivery Plan

### Phase A (Weeks 1–6): Autonomous Planning & Policies
- `schemas/plan.schema.json` (typed contract)  
- `orchestrator/planner.py` (goal→plan compiler, re-planning)  
- `policy/engine` (YAML rules, consent UI), deny/allow telemetry  
- Router v1 (heuristics: latency/cost/context)  
**Exit**: Complex multi-step tasks run with approvals; green CI; **100% coverage** on new code.

### Phase B (Weeks 6–12): Multi-Agent Programs & Evaluators
- Dynamic role spawning/budgets; rate limiting  
- Evaluators: code/tests/static, factuality, safety; pass@K harness  
- Memory slices per role; episode linking in Graphiti  
**Exit**: End-to-end build-and-ship demo finishes within SLA; evaluator-weighted routing improves success/latency.

### Phase C (Weeks 12–20): Self-PRs & Canary Rollouts
- Self-PR bot (prompt/router/config/test deltas), provenance signing  
- Canary+rollback scripts; changelog synthesis  
- Prompt/data-ops (golden suites; regression dashboards via **ART**)  
**Exit**: Weekly self-PRs auto-merge ≥90% without regressions; clear rollback proofs.

### Phase D (Weeks 20–28): Multimodal & Domain Skills
- Voice I/O (**Parlant + VibeVoice**); PDF/LaTeX→tables; vision extraction  
- SEO/Geo skills; browser tools & safe browsing policies  
- Cross-device sessions; artifact sharing  
**Exit**: Voice-driven plan edits; PDF→CSV/Charts works; SEO audits produce actionable PRs.

### Phase E (Ongoing): Adaptive Router & Skill Induction
- Bandit router updates from evaluator win-rates  
- Distill frequent plans into typed, reusable “skills”  
- Public “skill market” with safety metadata  
**Exit**: Faster convergence on plans; fewer tokens per success; richer toolchain with guardrails.

### Phase F (Add-ons): External Automation & APIs
- **n8n** flow exports, low-code pipelines (Telegram, Reddit, Email)  
- Unified API brokers integration for single-key access to thousands of APIs  
- **Nango** integration (Studio panel, MCP bridge, autogen nodes)  
- **ART**-driven prompt regression tracking  
**Exit**: Contributors compose automation via n8n; regression suites harden prompts/tools; SaaS automation in Studio.

### Phase G (Knowledge & Metadata RAG)
- **Tensorlake** metadata-augmented embeddings for context filtering  
- Fine-grained classification (page-level, domain-specific)  
**Exit**: RAG answers become cheaper, faster, more accurate.

### Phase H (Scaling & Performance)
- **vLLM** multi-GPU/multi-node serving (paged attention, prefix caching, speculative decoding)  
- **LMCache/NIXL** connectors for KV transfer and disaggregated P/D pipelines  
- Auto-tuning of latency vs throughput tradeoffs  
**Exit**: Near-linear scaling across nodes with auto-optimized SLOs.

### Phase I — RL & Evolutionary Optimization (builds on C/E)
- **Agent Lightning** offline RL on trace logs (reward events: success, token/ms savings, safety penalties)  
- Evolver in `introspector` for perf (GPU kernels, data transforms) with Pareto selection  
**Exit**: ↑pass@1/↑pass@K, ↓p95 latency/cost, **zero safety regressions**.

### Phase J — Interop & Enterprise Backends (builds on F/H)
- **MCP/Bedrock** backend; Agentic Web handshake; optional **SuperAGI** runtime  
- Full audits, feature flags, domain allowlists, quotas  
**Exit**: Enterprise-ready flows with policy compliance and green SLOs.

---

## 10) Engineering Quality Gates (always-on)

- **Coverage**: Per-area (UI/Server/Python) **100%** with branch coverage (exclusions only for bootstrap).  
- **Static checks**: TS strict/mypy, ESLint, Semgrep/Bandit, supply-chain scan, IaC lint (if infra).  
- **Tests**: Unit + property + metamorphic; MSW/network stubs; golden prompt suites.  
- **Repro**: Pinned versions; snapshots for plans & prompts; deterministic seeds.

---

## 11) File/Module Backlog (next PRs)

- `schemas/plan.schema.json`  
- `orchestrator/planner.py` + tests  
- `router/policy.yaml` + `policy/engine.ts` + Studio consent banners  
- `registry/tools.json` + adapters (MCP/HTTP/CLI/DB/Browser/PDF/ASR/TTS/SEO/Geo/n8n/Nango)  
- `integrations/graphiti/*` writers/retrievers  
- `evaluators/*` harness (code/factuality/safety/latency/cost)  
- `self_pr/bot.ts` + `.github/workflows/canary.yml` + rollback  
- `voice/*` (ASR/TTS, streaming UI), `vision/*` (OCR/table/latex)  
- `studio/*` (Plan preview, policy notices, memory timeline, evaluator panels)  
- `integrations/lmcache/*` (KV transfer), `engines/vllm|trtllm|sglang/*`

_All new modules must ship with tests, docs, and coverage; merges blocked if any scope <100%._

---

## 12) Example Use-Cases Unlocked

- **End-to-end repo creation** from a spec (code, tests, CI, container, deploy, docs).  
- **PDF data extraction** (financial/maths) to tables/charts with sanity checks.  
- **SEO/Geo audits** — crawl, analyze, propose changes, open PRs.  
- **Voice-driven sprints** — stand-ups, issue updates, PR summaries, plan edits.  
- **n8n Pipelines** — Reddit→Claude→Telegram, email responders, content reposters.  
- **Metadata-RAG** — bank statements, contracts, logs filtered by page type.  
- **SaaS automations** — HubSpot→Slack→GitHub via **Nango** in one click.

---

## 13) Risks & Mitigations

- **Model drift / regression** → Golden suites, canary + rollback, evaluator gating.  
- **Cost spikes** → Local-first, budgets, adaptive routing, KV cache, batch.  
- **Data/secret exposure** → Vault leases, redaction, path/domain allowlists.  
- **Over-autonomy** → Mode gating, consent prompts, kill switches, strict policies.  
- **Supply-chain** → Lockfiles, signature verification, SBOM (optional).

---

## 14) New Integrations (Q3–Q4 2025)

### 14.1 Agent Lightning — RL Fine-Tuning for Agents
**Goal.** Auto-improve agent quality & cost via offline RL on Naestro traces.  
**Scope.** Reward events (success, token/ms savings, safety penalties); shadow policies; canary.  
**Exit.** ↑pass@K / ↓p95 latency&cost; no safety regressions.

### 14.2 AlphaEvolve-style Evolvers — Performance-guided Codegen
**Goal.** Evo-оптимизация горячих участков (GPU kernels, parsers).  
**Scope.** `introspector/evolver` + microbench evaluators; Pareto (speed/correctness/stability).  
**Exit.** ≥10–15% ускорение без потери корректности.

### 14.3 AWS Bedrock AgentCore + MCP
**Goal.** Optional enterprise backend for tools/memory/identity with audit.  
**Scope.** MCP adapters; Plan→MCP tools; policy mapping.  
**Exit.** Audit-complete reference flow with feature flags.

### 14.4 Agentic Web — Safe Interop with External Agents
**Goal.** безопасное взаимодействие с внешними агентами.  
**Scope.** Registry, handshakes, scopes, quotas, domain allowlists; full traces in Studio.  
**Exit.** Cross-agent tasks w/o policy/budget violations.

### 14.5 SuperAGI Runtime (Optional)
**Goal.** Pluggable runtime alternative to LangGraph/CrewAI.  
**Scope.** Flow adapter; Plan.json mapping; parity tests.  
**Exit.** Equivalent traces/SLO; opt-in profile.

---

## 15) Roadmap Phases (Addenda)

### Phase I — RL & Evolutionary Optimization (reinforced)
- Agent Lightning offline RL на трейc-логах.  
- Evolver в `introspector` с микробенч-набором.  
- **Acceptance**: ↑pass@K & ↓p95 latency/cost; 0 safety regressий.

### Phase J — Interop & Enterprise Backends (reinforced)
- MCP/Bedrock; Agentic Web; SuperAGI runtime (opt-in).  
- **Acceptance**: full audits; policy compliance; green SLOs.

---

## 16) Appendices

**A. Local Models (DGX Spark)**  
- Llama-3.1-70B FP8 TRT-LLM — Judge/Planner  
- DeepSeek-32B — Proposer/Synth  
- Qwen-32B-AWQ — Critic/Refactor  
- GPT-OSS — open 20B/120B-class

**B. Cloud Pool**  
- GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM, **LFM2-350M** (JP↔EN)

**C. Key Integrations**  
- Graphiti (memory graphs), LangGraph/CrewAI (optional runtime), **ART** (prompt regression), **Parlant + VibeVoice** (voice), **MCP** (tool bus), **OmniNova** (planner/critic), **Symphony** (decentralized), **Open Computer Agent** (UI automation), unified API brokers, **n8n** (low-code pipelines), **Nango** (SaaS hub), **LFM2**, **Tensorlake** (metadata RAG), **GPT-OSS** (open models), **vLLM/LMCache** (scaling stack).
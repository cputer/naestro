# Naestro ROADMAP — Evolving Autonomous System (ASI Trajectory)

**North Star**  
Naestro evolves from a goal-driven multi-agent orchestrator into a continuously self-improving autonomous system that can:  
(1) decompose open-ended goals;  
(2) coordinate local+cloud LLMs and tools;  
(3) write, test, and ship production-quality code;  
(4) operate safely with strong observability and policy gates;  
(5) self-improve via guarded self-edits validated by rigorous evaluations.

---

## 0) Current Status (Baseline)

- **Local-first model set (DGX Spark single node):**  
  Llama-3.1-70B (FP8 TRT-LLM) as Judge/Planner;  
  DeepSeek-32B as Proposer/Synth;  
  Qwen-32B-AWQ as Critic/Code.  
  Cloud spillover for long-context/specialty tasks (GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM via vLLM).

- **Studio (Web UI):**  
  Real-time runs (WS/SSE), dark theme, metrics (workflows, consensus, latency, KV cache hit, cost), run details and traces;  
  **n8n Export** and **Nango SaaS Panel**.

- **Guardrails:**  
  Thermal/VRAM caps;  
  step-level re-route on OOM/timeouts;  
  retry/backoff;  
  consent prompts for sensitive actions.

- **SDLC quality:**  
  PR linting (commitlint), Release Please, Codecov with per-flag coverage, Node 22 standardization, deterministic UI+Python tests.

---

## 1) Target Properties (what “evolving ASI” means here)

1. **General goal execution** — Turn natural-language objectives into executable plans (DAGs) with budgets, SLAs, and success criteria.  
2. **Model+tool orchestration** — Choose the right LLM(s)/tool(s) per step using live telemetry + historical win-rates.  
3. **Formalized self-improvement** — Periodic self-proposals (self-PRs) that increase pass-rates, reduce latency/cost, and expand safe capability coverage.  
4. **Safety-first autonomy** — Hard capability boundaries, consent layers, and provable rollback; humans remain in control of scopes and secrets.  
5. **Observability & provenance** — Every action is explainable, replayable, and signed; drift and regressions are caught early.  
6. **Hallucination-resilience** — The system actively prevents, detects, and corrects unsupported claims via retrieval-first planning, verifiers, uncertainty/abstention, and citation-grounded outputs.  
7. **Long-context acceleration** — **REFRAG compression lane** enables 16× effective context and order-of-magnitude lower TTFT/cost on self-hosted models while preserving accuracy.  
8. **Preference-optimized policies** — Expansion, routing, and planner policies leverage advanced preference optimization methods (PVPO, DCPO, GRPO-RoC, ARPO, TreePO, MixGRPO, DuPO) for stability, efficiency, and reasoning accuracy.  
9. **Runtime interop** — Naestro supports pluggable runtimes (LangGraph, CrewAI, AgentScope, AutoAgent, Agent Squad) with policy/trace parity.

---

## 2) System Roles (logical components)

- **Planner** — Compiles Goal → `Plan.json` (tasks, deps, inputs/outputs, budgets, acceptance checks).  
- **Router** — Chooses model/provider per step (local vs cloud) using: win-rates, latency, context length, and cost.  
- **Agents** — Role types: Researcher, Coder, Reviewer, Runner, DataOps, Evaluator, Reporter. Spawned dynamically with scoped permissions.  
- **Policy Engine** — Enforces tool/network/path allowlists, data scopes, rate limits, and cost/time ceilings. Produces consent prompts and audit events.  
- **Tool/Skill Registry** — Typed contracts (JSON Schema), versioned adapters (MCP/HTTP/CLI/DB/Browser/PDF/Vision/ASR/TTS/SEO/Geo/n8n/Nango/Firecrawl/Gitingest), deprecation paths.  
- **Memory Fabric** — Episodic (runs), semantic (facts/summaries), skill memories (reusable flows), user prefs. Graph-structured (Graphiti) with retrieval policies.  
- **Evaluators** — Code/test/typing/static analysis; factuality/consistency; safety; latency/cost; pass@K; metamorphic/program properties.  
- **Claim Verifier** — Tool-using checker that enforces citation-backed answers, performs chain-of-verification, and can abstain or ask for retrieval when evidence is insufficient.  
- **Introspector** — Summarizes failures, extracts lessons, proposes prompt/route/tool upgrades (feeds Self-PR cycle).  
- **Self-PR Bot** — Opens PRs (prompt hardening, flaky test fixes, router weights, small refactors), runs canary, signs artifacts, auto-merges if green.  
- **Evidence Store** — Short-lived artifact bucket for retrieved passages, URLs, repo digests (from Gitingest), and crawl chunks (from Firecrawl) used by verifiers and provenance signing.  
- **REFRAG Controller** — Orchestrates compression policy: selects chunks to compress/expand, calls encoder+projection, and supplies mixed inputs (tokens + embeddings) to local decoders.  
- **PO Policy Module** — Encapsulates preference optimization strategies (PVPO, DCPO, GRPO-RoC for REFRAG; ARPO for tool agents; TreePO for planner branching; MixGRPO for exploration vs exploitation).  
- **Runtime Adapters** — Plug-in backends: LangGraph, CrewAI, AgentScope, AutoAgent, **Agent Squad**. Unified contract ensures policy gating, trace parity, and conformance with Evaluators.

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
      Registry[Tool/Skill Registry]
      Memory[Graphiti Memory Fabric]
      Evaluators
      Verifier[Claim Verifier & CoVe]
      Introspector
      SelfPR[Self-PR Bot]
      Evidence[Evidence Store]
      REFRAGC[REFRAG Controller]
      PO[PO Policy Module]
    end

    subgraph Engines["Serving Engines"]
      VLLM[vLLM / SGLang]
      TRTLLM[TensorRT-LLM]
      Triton[Triton Inference Server]
      REFRAGE[REFRAG Encoder+Projection]
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
      LFM2[LFM2 multi-language]
    end

    subgraph Integrations["Integrations"]
      MCP[MCP Client/Server]
      Parlant[Parlant + VibeVoice (ASR/TTS)]
      DIA[DIA TTS (multi-speaker)]
      n8n[n8n Flow Export]
      Nango[Nango SaaS API Hub]
      ART[ART Prompt-Ops]
      Tensorlake[Tensorlake Metadata-RAG]
      OmniNova[OmniNova]
      Symphony[Symphony]
      OCA[Open Computer Agent (Browser/UI)]
      LMCache[LMCache/NIXL KV-Transfer]
      AgentScope[AgentScope Runtime]
      GraphRAG[GraphRAG/LazyGraphRAG]
      Firecrawl[Firecrawl (Web Crawl & Extract)]
      Gitingest[Gitingest (Repo → Digest)]
      AutoAgent[AutoAgent (Clustered Agents)]
      AgentSquad[Agent Squad Runtime]
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

    Evaluators --> Verifier
    Verifier --> Evidence
    Evaluators --> Introspector
    Introspector --> SelfPR
    SelfPR --> |PRs| Studio

    ART --> Evaluators
    Tensorlake --> Memory
    MCP --> Registry
    n8n --> Registry
    Nango --> Registry
    Parlant --> Registry
    DIA --> Registry
    OCA --> Registry
    LMCache --> Engines
    AgentScope --> Core
    GraphRAG --> Memory
    Firecrawl --> Evidence
    Gitingest --> Evidence
    AutoAgent --> Core
    AgentSquad --> Core

    Memory --> REFRAGC
    REFRAGC --> REFRAGE
    REFRAGE --> Engines
    PO --> Router
    PO --> Planner
    PO --> REFRAGC
```

---

## 4) Self-Rewrite Loop (guarded autonomy)

1. **Collect**: Surface failures (dropped runs, OOM, policy denials), slow traces (P95 spikes), evaluator misses, flaky tests.  
2. **Propose**: Agents generate *minimal* diffs (prompt deltas, router weights, tool config, tests) → PRs.  
3. **Validate**:  
   - Unit + property + metamorphic tests (100% coverage).  
   - Golden prompts via prompt-ops (ART integration).  
   - Offline dataset replays; synthetic task suites (coding, agentic, PDF/LaTeX, SEO/Geo, browse).  
   - Hallucination red-team suite: contradiction sets, unsupported-claim traps, source-omission tests; require citation coverage for knowledge answers.  
4. **Canary**: Shadow traffic; watch SLOs (success, latency, cost, safety incidents). Automatic rollback if any breach.  
5. **Merge**: Provenance sign, release notes, version bump.  
6. **Learn**: Update router priors from win-rates; store counter-examples in memory for future planning.  

**Non-goals**: unrestricted self-modification, unsupervised network/file access, or secret exfiltration.

___

## 5) Safety & Capability Governance

- **Modes**:  
  - `Guide` (suggest),  
  - `Copilot` (confirm),  
  - `Auto` (approved scopes only).  

- **Boundaries**:  
  - **Secrets**: lease-scoped vault; never to client; redaction in traces.  
  - **Filesystem & network**: path/domain allowlists; sandboxed exec; rate limits.  
  - **Data**: PII classifiers; off-prem toggle; export redaction.  

- **Kill switches**: Pause runs; revoke tokens; quarantine models/tools.  

- **Compliance**: Comprehensive audit logs (immutable), purpose/consent receipts.  

- **Output truthfulness gates**: For knowledge/claims tasks, force retrieval (Firecrawl/Gitingest/GraphRAG), require inline citations, enable abstain-on-uncertainty, and block delivery if verification fails.

---

## 6) Orchestration & Models

- **Local (DGX Spark)**  
  - Llama-3.1-70B FP8 TRT-LLM: Judge/Planner (batching, KV cache).  
  - DeepSeek-32B: Proposer/Synth (fast code/reasoning).  
  - Qwen-32B-AWQ: Critic/Refactor (low VRAM).  
  - GPT-OSS 20B/120B: open GPT-level local-first options.  
  - **REFRAG Compression Lane (local only):** lightweight encoder + projection that compresses retrieved chunks into dense embeddings consumed by local decoders; RL/heuristic expansion preserves critical spans; requires vLLM/TRT-LLM hook for mixed inputs.  
  - **PO Policy Layer:** preference optimization methods integrated (PVPO, DCPO, GRPO-RoC; ARPO, TreePO, MixGRPO, DuPO).  

- **Cloud**  
  - GPT-4/5-class (general), Claude 3.7+ (long reasoning), Gemini-2.5+ (long-context/multimodal), Mistral/Grok/OpenELM.  
  - LFM2 (multi-language) for high-quality translation and multilingual workflows.  
  - **Note:** REFRAG path not applied to closed API models; router will bypass.  

- **Routing policy**  
  - Prefer local; spill to cloud on long context, specialty tools, or latency SLO breaches.  
  - Bandit-style updates from evaluators’ win-rates.  
  - **Reasoning budget knobs** (think/on/off; effort levels) normalized across providers.  
  - **REFRAG routing rule**: if model ∈ {vLLM/TRT-LLM local} and context_len > threshold → use REFRAG lane; else baseline RAG.

---

## 7) Advanced Capabilities (to integrate)

- **Voice**: Parlant + Whisper/Zonos, **VibeVoice** (long-form/emotional TTS), **DIA TTS (multi-speaker one-pass dialogue)**, multilingual ASR, streaming TTS, barge-in, voice memory.  
- **Vision/PDF**: OCR tables → structured JSON; formula/LaTeX extraction; chart/table synthesis.  
- **SEO/Geo**: Crawler/SERP parsers, sitemap audits, NER/geocoding, local ranking diffing; content/robots PRs.  
- **Prompt/Data-Ops**: ART prompt regression tracking, dataset curation, result drift detection.  
- **Workflow Runtimes**: Interop with **LangGraph/CrewAI/AgentScope/AutoAgent/Agent Squad** as optional backends for complex tool flows (still governed by Naestro policy/router).  
- **Unified API brokers**: Single-key providers for broad API/tool coverage (RapidAPI-style).  
- **n8n Integration**: Export Naestro workflows to n8n YAML, enabling low-code automation (email agents, Telegram bots, Reddit pipelines).  
- **Web Ingestion**: **Firecrawl** for crawl→extract→chunk→index pipelines with robots.txt compliance and selector-based extraction.  
- **Knowledge**: **GraphRAG/LazyGraphRAG** modes for graph-aware retrieval.  
- **RAG Quality**: **Tensorlake-style metadata augmentation** (page type/table vs text/section tags) for cheaper, faster, more accurate retrieval.  
- **Scaling**: **vLLM** (paged/prefix/speculative) + **TensorRT-LLM**; **LMCache/NIXL** KV transfer; multi-node disaggregated prefill/decode.  
- **Repo Ingestion**: **Gitingest** to turn any Git repo (or `github.com → gitingest.com` URL swap) into a prompt-friendly **repository digest** (code + docs), feeding **Evidence Store** for coding agents.  
- **Hallucination-Resistant Generation (HRG)**: Retrieval-first planning, **self-consistency**, **chain-of-verification (CoVe)**, **calibrated uncertainty**, **abstention**, **structured outputs** with JSON Schema, and **tool-use preference** for factual queries.  
- **REFRAG Long-Context Acceleration**: compression of retrieved context (k=8–32), KV/cache savings, RL/heuristic expansion of critical spans; metrics wired to Observability.  
- **PO-Optimized Policies**: stability, efficiency, accuracy gains across reasoning, planning, routing, expansion.

---

## 8) Observability & Metrics

- **Traces**: model, tokens, TTFT/ITL latency, cost, context, policy hits, memory I/O, tool effects.  
- **Dashboards**: success & consensus rates, router win-rates, KV hit %, cloud spill %, anomaly flags, thermo/VRAM.  
- **Benchmarks**: project-specific regression suites; public benchmarks proxied via adapters; trendlines and SLA alerts (**SWE-bench Verified**, **LiveBench**).  
- **OpenTelemetry GenAI** semantic conventions as first-class.  
- **Truthfulness KPIs**: hallucination rate (unsupported-claim%), abstention%, citation coverage%, verifier pass rate, evidence freshness, and repo-digest usage rate (Gitingest/Firecrawl).  
- **REFRAG KPIs**: TTFT speedup vs baseline, input-token reduction factor, KV cache memory delta, accuracy parity (exact-match/F1/judge), expansion rate (% tokens bypassing compression), cache hit for precomputed embeddings.  
- **PO KPIs**: policy stability (variance), sample efficiency (improvement vs training data), reasoning accuracy (pass@K uplift).

---

## 9) Phased Delivery Plan

### Phase A (Weeks 1–6): Autonomous Planning & Policies
- `schemas/plan.schema.json` (typed contract).  
- `orchestrator/planner.py` (goal→plan compiler, re-planning).  
- `policy/engine` (YAML rules, consent UI), deny/allow telemetry.  
- Router v1 (heuristics: latency/cost/context).  
**Exit**: Complex multi-step tasks run with approvals; green CI; 100% coverage on new code.

---

### Phase B (Weeks 6–12): Multi-Agent Programs & Evaluators
- Dynamic role spawning/budgets; rate limiting.  
- Evaluators: code/tests/static, factuality, safety; pass@K harness.  
- Memory slices per role; episode linking in Graphiti.  
- **Claim Verifier MVP** (CoVe + abstain).  
- **Evidence Store MVP**.  
**Exit**: End-to-end build-and-ship demo finishes within SLA; evaluator-weighted routing improves success/latency.

---

### Phase C (Weeks 12–20): Self-PRs & Canary Rollouts
- Self-PR bot (prompt/router/config/test deltas), provenance signing.  
- Canary+rollback scripts; changelog synthesis.  
- Prompt/data-ops (golden suites; regression dashboards via ART).  
- **Hallucination red-team tests** wired to canary gates.  
**Exit**: Weekly self-PRs auto-merge ≥90% without regressions; clear rollback proofs.

---

### Phase D (Weeks 20–28): Multimodal & Domain Skills
- Voice I/O (Parlant + VibeVoice + DIA).  
- PDF/LaTeX→tables; vision extraction.  
- SEO/Geo skills; browser tools & safe browsing policies.  
- Cross-device sessions; artifact sharing.  
**Exit**: Voice-driven plan edits; PDF→CSV/Charts works; SEO audits produce actionable PRs.

---

### Phase E (Ongoing): Adaptive Router & Skill Induction
- Bandit router updates from evaluator win-rates.  
- Distill frequent plans into typed, reusable “skills”.  
- Public “skill market” with safety metadata.  
**Exit**: Faster convergence on plans; fewer tokens per success; richer toolchain with guardrails.

---

### Phase F (Weeks 28–36): External Automation & APIs
- n8n flow exports, low-code pipelines (Telegram, Reddit, Email).  
- Unified API brokers integration for single-key access to thousands of APIs.  
- **Nango integration** (Studio panel, MCP bridge, autogen nodes).  
- ART-driven prompt regression tracking.  
**Exit**: Contributors compose automation via n8n; regression suites harden prompts/tools; SaaS automation in Studio.

---

### Phase G (Weeks 36–44): Knowledge & Metadata RAG
- Tensorlake metadata-augmented embeddings for context filtering.  
- Fine-grained classification (page-level, domain-specific).  
- **Firecrawl** ingestion jobs and pipelines.  
- **Gitingest** repo-digest adapter + Studio “Ingest Repo” action.  
- **Evidence Store** wiring.  
**Exit**: RAG answers become cheaper, faster, more accurate.

---

### Phase H (Weeks 44–52): Scaling & Performance
- vLLM multi-GPU/multi-node serving (paged attention, prefix caching, speculative decoding).  
- LMCache/NIXL connectors for KV transfer and disaggregated P/D pipelines.  
- Auto-tuning of latency vs throughput tradeoffs.  
**Exit**: Near-linear scaling across nodes with auto-optimized SLOs.

---

### Phase H.1 (Weeks 52–56): REFRAG Long-Context Acceleration
- Implement **REFRAG Compression Lane** for local models: encoder+projection, mixed-input decode hook (tokens + embeddings).  
- Retriever: store raw chunks + precomputed embeddings; cache keys `(doc_id, chunk_idx, hash)`.  
- Expansion policy: heuristic → RL policy; feature flag + routing rule (local-only).  
- Observability: TTFT, KV delta, accuracy parity dashboards; A/B harness vs baseline RAG.  
**Exit**: ≥10× TTFT improvement on long-doc RAG with accuracy parity; production flag on local models, cloud bypass intact.

---

### Phase I (Weeks 56–64): RL & Evolutionary Optimization
- **Agent Lightning** offline RL on trace logs (reward events: success, token/ms savings, safety penalties).  
- **Evolver** in introspector for perf (GPU kernels, data transforms) with Pareto selection.  
- **PO Policy Training:**  
  - PVPO/DCPO for REFRAG stability.  
  - GRPO-RoC for reasoning calibration.  
  - ARPO for agent routing preferences.  
  - TreePO for planner branching.  
  - MixGRPO/DuPO for exploration balance.  
**Exit**: ↑pass@1/↑pass@K, ↓p95 latency/cost, zero safety regressions, stable policy improvements.

---

### Phase J (Weeks 64–72): Interop & Enterprise Backends
- MCP/Bedrock backend; Agentic Web handshake.  
- **Agent Squad runtime adapter (TS+Py)** with Studio panel.  
- SuperAGI/AgentScope runtime (opt-in).  
- Full audits, feature flags, domain allowlists, quotas.  
**Exit**: Enterprise-ready flows with policy compliance and green SLOs.

---

### Phase K (Weeks 72–80): Clustered Swarms
- **AutoAgent** runtime adapter (clustered multi-agent execution).  
- **Agent Squad** runtime orchestration (multi-agent, routing, context maintenance).  
- Patterns: planner–worker, verifier, debate, MoA ensembles.  
**Exit**: Scalable agent swarms with fault-tolerant coordination and trace parity.

___

## 10) Engineering Quality Gates (always-on)

- **Coverage**: Per-area (UI/Server/Python) 100% with branch coverage (exclusions only for bootstrap).  
- **Static checks**: TS strict/mypy, ESLint, Semgrep/Bandit, supply-chain scan, IaC lint (if infra).  
- **Tests**: Unit + property + metamorphic; MSW/network stubs; golden prompt suites.  
- **Repro**: Pinned versions; snapshots for plans & prompts; deterministic seeds.  
- **Truthfulness CI**: fail PR if hallucination red-team suite regresses; require citation coverage and verifier pass for knowledge tests.  
- **REFRAG CI**: synthetic long-context suite (exact-answer sets); block merges if TTFT regression >X% at target compression (k=16) or accuracy delta >Y%.  
- **PO CI**: policy stability tests (variance thresholds), sample efficiency checks, accuracy regression gates.

---

## 11) File/Module Backlog (next PRs)

- `schemas/plan.schema.json`  
- `orchestrator/planner.py` + tests  
- `router/policy.yaml` + `policy/engine.ts` + Studio consent banners  
- `registry/tools.json` + adapters (MCP/HTTP/CLI/DB/Browser/PDF/ASR/TTS/SEO/Geo/n8n/Nango/Firecrawl/DIA/Gitingest)  
- `integrations/graphiti/*` writers/retrievers  
- `evaluators/*` harness (code/factuality/safety/latency/cost)  
- `self_pr/bot.ts` + `.github/workflows/canary.yml` + rollback  
- `voice/*` (ASR/TTS, streaming UI), `vision/*` (OCR/table/latex)  
- `studio/*` (Plan preview, policy notices, memory timeline, evaluator panels)  
- `integrations/lmcache/*` (KV transfer), `engines/vllm|trtllm|sglang/*`  
- `runtimes/{langgraph,crewai,agentscope,autoagent,superagi,agent-squad}/*` adapters  
- `verifier/*` (claim-checker, abstention, CoVe prompts, calibration)  
- `evidence/*` (Firecrawl/Gitingest/GraphRAG artifact store + provenance signing)  
- `refrag/encoder/*` (lightweight encoder + projection, training scripts)  
- `refrag/controller/*` (compression policy, expansion heuristics/RL, router hook)  
- `refrag/inference-hooks/*` (vLLM/TRT-LLM embedding injection, mixed-input API)  
- `refrag/ab_harness/*` (baseline vs REFRAG, metrics exporters)  
- `po_policies/*` (PVPO, DCPO, GRPO-RoC, ARPO, TreePO, MixGRPO, DuPO implementations, tests, benchmarks).  

_All new modules must ship with tests, docs, and coverage; merges blocked if any scope <100%._

---

## 12) Example Use-Cases Unlocked

- **End-to-end repo creation** from a spec (code, tests, CI, container, deploy, docs).  
- **PDF data extraction** (financial/maths) to tables/charts with sanity checks.  
- **SEO/Geo audits** — crawl, analyze, propose changes, open PRs.  
- **Voice-driven sprints** — stand-ups, issue updates, PR summaries, plan edits (now multi-speaker DIA for agent debates).  
- **n8n Pipelines** — Reddit→Claude→Telegram, email responders, content reposters.  
- **Metadata-RAG** — bank statements, contracts, logs filtered by page type.  
- **SaaS automations** — HubSpot→Slack→GitHub via Nango in one click.  
- **Full-site ingestion** — Firecrawl crawl/extract to vector/graph stores.  
- **Agent swarms** — AutoAgent clustered multi-agent runs.  
- **Codebase Q&A with guarantees** — ingest a GitHub repo via Gitingest → ask questions with citations to specific files/lines; verifier blocks answers without evidence.  
- **Whole-report reasoning at speed** — REFRAG lets local models read entire docs/logs with accuracy parity and dramatically lower latency/cost.  
- **Stable expansion** — PVPO/DCPO keeps REFRAG compression accurate under long-context stress.  
- **Reasoning calibration** — GRPO-RoC improves correctness in deep reasoning tasks.  
- **Planner pruning** — TreePO reduces branching explosion.  
- **Exploration balance** — MixGRPO/DuPO enhances adaptive search.  
- **Agent Squad integration** — multi-agent orchestration with intelligent routing and context maintenance, running under Naestro policy/trace parity.

---

## 13) Risks & Mitigations

- **Model drift / regression** → Golden suites, canary + rollback, evaluator gating.  
- **Cost spikes** → Local-first, budgets, adaptive routing, KV cache, batch.  
- **Data/secret exposure** → Vault leases, redaction, path/domain allowlists.  
- **Over-autonomy** → Mode gating, consent prompts, kill switches, strict policies.  
- **Supply-chain** → Lockfiles, signature verification, SBOM (optional).  
- **Hallucinations** → Retrieval-first, verifier with abstention, citation enforcement, red-team tests, uncertainty calibration.  
- **REFRAG compatibility** → Works only on self-hosted open-weight models; router enforces bypass for closed APIs. Fallback to baseline RAG if expansion policy uncertainty high or KPIs regress.  
- **PO stability** → DCPO clipping, variance checks, MixGRPO/DuPO exploration balance, rollback if instability detected.  
- **Runtime divergence** (Agent Squad / others) → adapter conformance tests, SLO monitoring, trace parity.

---

## 14) New Integrations (Q3–Q4 2025)

**14.1 Agent Lightning — RL Fine-Tuning for Agents**  
*Goal.* Auto-improve agent quality & cost via offline RL on Naestro traces.  
*Scope.* Reward events (success, token/ms savings, safety penalties); shadow policies; canary.  
*Exit.* ↑pass@K / ↓p95 latency&cost; no safety regressions.

**14.2 AlphaEvolve-style Evolvers — Performance-guided Codegen**  
*Goal.* Evo-optimization of hot paths (GPU kernels, parsers).  
*Scope.* `introspector/evolver` + microbench evaluators; Pareto (speed/correctness/stability).  
*Exit.* ≥10–15% speedup with 100% correctness.

**14.3 AWS Bedrock AgentCore + MCP**  
*Goal.* Optional enterprise backend for tools/memory/identity with audit.  
*Scope.* MCP adapters; Plan→MCP tools; policy mapping.  
*Exit.* Audit-complete reference flow with feature flags.

**14.4 Agentic Web — Safe Interop with External Agents**  
*Goal.* Safe interaction with external agents/services.  
*Scope.* Registry, handshakes, scopes, quotas, domain allowlists; full traces in Studio.  
*Exit.* Cross-agent tasks without policy/budget violations.

**14.5 SuperAGI / AgentScope Runtime (Optional)**  
*Goal.* Pluggable runtime alternatives to LangGraph/CrewAI.  
*Scope.* Flow adapters; Plan.json mapping; parity tests.  
*Exit.* Equivalent traces/SLO; opt-in profile.

**14.6 Agent Squad Runtime (Optional)**  
*Goal.* Multi-agent orchestration with intelligent routing and context maintenance.  
*Scope.* TS+Py adapters; Studio runtime panel; parity/conformance tests vs LangGraph/AgentScope; policy/trace parity.  
*Exit.* Optional runtime with green SLOs, adapter conformance, Studio trace integration.

---

## 15) Roadmap Phases (Addenda)

**Phase I — RL & Evolutionary Optimization (reinforced)**  
Agent Lightning offline RL; Evolver with microbench suite; PO policy training.  
*Acceptance:* ↑pass@K & ↓p95 latency/cost; 0 safety regressions; stable PO metrics.

**Phase J — Interop & Enterprise Backends (reinforced)**  
MCP/Bedrock; Agentic Web; SuperAGI/AgentScope/Agent Squad runtimes.  
*Acceptance:* full audits; policy compliance; green SLOs; adapter parity.

**Phase K — Clustered Swarms (reinforced)**  
AutoAgent runtime; Agent Squad orchestration; MoA/consensus templates; resilience tests.  
*Acceptance:* fault-tolerant swarms with reproducible traces, policy/trace parity.

---

## 16) Appendices

**A. Local Models (DGX Spark)**  
- Llama-3.1-70B FP8 TRT-LLM — Judge/Planner  
- DeepSeek-32B — Proposer/Synth  
- Qwen-32B-AWQ — Critic/Refactor  
- GPT-OSS — open 20B/120B-class  
- **REFRAG components** — encoder+projection weights; controller; inference hooks (vLLM/TRT-LLM) with mixed-input support  
- **PO Policy implementations** — PVPO, DCPO, GRPO-RoC, ARPO, TreePO, MixGRPO, DuPO  

**B. Cloud Pool**  
- GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM, LFM2 (multi-language: EN/RU/ES/JP/etc.)  
- **Note:** REFRAG bypass (closed APIs).

**C. Key Integrations**  
- Graphiti (memory graphs)  
- LangGraph/CrewAI/AgentScope/AutoAgent/**Agent Squad** (runtimes)  
- ART (prompt regression)  
- Parlant + VibeVoice + DIA (voice)  
- MCP (tool bus)  
- OmniNova (planner/critic)  
- Symphony (decentralized)  
- OCA (UI automation)  
- Unified API brokers  
- n8n (low-code pipelines)  
- Nango (SaaS hub)  
- Firecrawl (web ingestion)  
- Tensorlake (metadata RAG)  
- GPT-OSS (open models)  
- vLLM/LMCache (scaling stack)  
- GraphRAG/LazyGraphRAG  
- Gitingest (repo → digest for grounded code Q&A)  
- **REFRAG** (local long-context compression lane)  
- **PO Policy Layer** (preference optimization integration)
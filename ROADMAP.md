# Naestro ROADMAP — Evolving Autonomous System (ASI Trajectory)

**North Star**  
Naestro evolves from a goal-driven multi-agent orchestrator into a continuously self-improving autonomous system that can:  
1. Decompose open-ended goals.  
2. Coordinate local + cloud LLMs and tools.  
3. Write, test, and ship production-quality code.  
4. Operate safely with strong observability and policy gates.  
5. Self-improve via guarded self-edits validated by rigorous evaluations.

---

## 0) Current Status (Baseline)

- **Local-first model set (DGX Spark single node):**  
  Llama-3.1-70B (FP8 TRT-LLM) as Judge/Planner; DeepSeek-32B as Proposer/Synth; Qwen-32B-AWQ as Critic/Code.  
  Cloud spillover for long-context/specialty tasks (GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM via vLLM).  
- **Studio (Web UI):** Real-time runs (WS/SSE), dark theme, metrics (workflows, consensus, latency, KV cache hit, cost), run details and traces.  
- **Guardrails:** Thermal/VRAM caps; step-level re-route on OOM/timeouts; retry/backoff; consent prompts for sensitive actions.  
- **SDLC quality:** PR linting (commitlint), Release Please, Codecov with per-flag coverage, Node 22 standardization, deterministic UI+Python tests.

---

## 1) Target Properties (what “evolving ASI” means)

1. **General goal execution** — Natural-language objectives → executable plans (DAGs) with budgets, SLAs, and success criteria.  
2. **Model+tool orchestration** — Optimal model/tool per step using live telemetry and historical win-rates.  
3. **Formalized self-improvement** — Periodic self-PRs that increase pass-rates, reduce latency/cost, and expand safe capability coverage.  
4. **Safety-first autonomy** — Capability boundaries, consent layers, and provable rollback; humans remain in control of scopes and secrets.  
5. **Observability & provenance** — Every action is explainable, replayable, and signed; regressions caught early.

---

## 2) System Roles (logical components)

- **Planner** — Compiles Goal → `Plan.json` (tasks, dependencies, budgets, acceptance checks).  
- **Router** — Chooses model/provider per step (local vs cloud) based on win-rates, latency, context length, and cost.  
- **Agents** — Roles: Researcher, Coder, Reviewer, Runner, DataOps, Evaluator, Reporter. Spawned dynamically with scoped permissions.  
- **Policy Engine** — Enforces allowlists, scopes, rate limits, ceilings; produces consent prompts and audit events.  
- **Tool/Skill Registry** — Typed contracts (JSON Schema), versioned adapters (MCP/HTTP/CLI/DB/Browser/PDF/Vision/ASR/TTS/SEO/Geo).  
- **Memory Fabric** — Episodic (runs), semantic (facts/summaries), skill memories (flows), user prefs. Graph-structured with retrieval policies.  
- **Evaluators** — Code/test/static analysis; factuality; safety; latency/cost; pass@K; metamorphic properties.  
- **Introspector** — Summarizes failures, extracts lessons, proposes upgrades.  
- **Self-PR Bot** — Opens PRs (prompt hardening, router weights, refactors), runs canary, signs artifacts, auto-merges if green.

---

## 3) Self-Rewrite Loop (guarded autonomy)

1. **Collect**: Failures, slow traces, evaluator misses, flaky tests.  
2. **Propose**: Minimal diffs → PRs.  
3. **Validate**: Unit + property + metamorphic tests; golden prompts; offline replays; synthetic task suites.  
4. **Canary**: Shadow traffic; SLO checks; rollback if breach.  
5. **Merge**: Signed, versioned, released.  
6. **Learn**: Update router priors; store counter-examples in memory.

**Non-goals**: unrestricted self-modification, unsupervised network/file access, secret exfiltration.

---

## 4) Safety & Governance

- **Modes**: `Guide` (suggest), `Copilot` (confirm), `Auto` (scoped).  
- **Boundaries**: Secrets vault; path/domain allowlists; sandboxed exec; PII classifiers; redactions.  
- **Kill switches**: Pause, revoke, quarantine.  
- **Compliance**: Immutable logs, consent receipts.

---

## 5) Orchestration & Models

- **Local (DGX Spark)**  
  - Llama-3.1-70B FP8 TRT-LLM (Planner).  
  - DeepSeek-32B (Proposer/Synth).  
  - Qwen-32B-AWQ (Critic/Refactor).  
- **Cloud**  
  - GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM (served via vLLM).  
- **Routing policy**  
  - Prefer local; spill to cloud on long context or latency breaches.  
  - Bandit-style updates from evaluator win-rates.

---

## 6) Advanced Capabilities (to integrate)

- **Voice**: Parlant + Whisper/Zonos, multilingual ASR, streaming TTS, VibeVoice for long-form/emotional speech.  
- **Vision/PDF**: OCR → JSON; formula/LaTeX extraction; charts/tables.  
- **SEO/Geo**: Crawler/SERP parsers, sitemap audits, NER/geocoding, ranking diffing, content PRs.  
- **Prompt/Data-Ops**: ART regression tracking, dataset curation, drift detection.  
- **Workflow runtimes**: LangGraph/CrewAI optional backends.  
- **Unified API brokers**: “Single-key” providers (RapidAPI/Together-style).  
- **n8n integration**: Export workflows to n8n YAML (low-code automation).  
- **Translation**: LFM2-350M JP↔EN (efficient, open weights).  
- **vLLM enhancements**: Paged attention, prefix caching, speculative decoding, multi-GPU/multi-node with auto-tuning.  
- **Elastic scaling**: LMCache/NIXL KV-cache transfer, disaggregated prefill/decode.  
- **Tensorlake metadata-RAG**: Metadata-augmented embeddings for accuracy & cost reduction.  
- **OmniNova**: Planner/Critic synergy orchestration framework.  
- **Symphony**: Decentralized consensus-based agent coordination.  
- **MCP (Model Context Protocol)**: Standardized tool/API integration.  
- **Open Computer Agent**: Browser/UI automation for real-world interaction.  
- **GPT-OSS**: Open 20B/120B models to strengthen local-first stack.

---

## 7) Observability & Metrics

- **Traces**: model, tokens, latency, cost, policies, memory I/O, tool effects.  
- **Dashboards**: success rates, router win-rates, KV %, anomalies.  
- **Benchmarks**: regression suites, public benchmarks, SLA alerts.

---

## 8) Phased Delivery

### Phase A (Weeks 1–6): Planning & Policies  
- Planner, Policy Engine, Router v1.  
**Exit**: Multi-step tasks with approvals.

### Phase B (Weeks 6–12): Multi-Agent & Evaluators  
- Role spawning, evaluators, memory slices.  
**Exit**: End-to-end demo within SLA.

### Phase C (Weeks 12–20): Self-PR & Canary  
- Self-PR bot, canary, rollback, ART.  
**Exit**: ≥90% self-PRs auto-merge.

### Phase D (Weeks 20–28): Multimodal & Domain Skills  
- Voice (Parlant/VibeVoice), PDF/vision, SEO/Geo.  
**Exit**: Voice-driven edits, SEO audits.

### Phase E (Ongoing): Adaptive Router & Skills  
- Bandit updates, skill induction.  
**Exit**: Faster convergence, fewer tokens.

### Phase F: External Automation & APIs  
- n8n flows, API brokers, ART regression.  
**Exit**: Contributors compose automation via n8n.

### Phase G: Knowledge & Metadata RAG  
- Tensorlake metadata augmentation.  
**Exit**: Cheaper, faster, more accurate RAG.

### Phase H: Scaling & Performance  
- vLLM multi-node, LMCache/NIXL.  
**Exit**: Near-linear scaling, auto-optimized SLOs.

### Phase I: RL & Evolutionary Optimization  
- Agent Lightning RL loop, Evolver.  
**Exit**: Better pass@K, lower p95 latency/cost.

### Phase J: Interop & Enterprise Backends  
- MCP/Bedrock, Agentic Web, SuperAGI runtime.  
**Exit**: Audited cross-agent scenarios.

---

## 9) Quality Gates

- 100% coverage, static checks, golden suites, pinned versions, deterministic seeds.

---

## 10) Backlog (Next PRs)

- `schemas/plan.schema.json`  
- `orchestrator/planner.py` + tests  
- `router/policy.yaml` + Studio consent  
- `registry/tools.json` + adapters  
- `integrations/graphiti/*` retrievers  
- `evaluators/*` harness  
- `self_pr/bot.ts` + canary.yml  
- `voice/*`, `vision/*`  
- `studio/*` UI panels

---

## 11) Use-Cases

- End-to-end repo creation (code, tests, CI, deploy).  
- PDF→tables/charts with sanity checks.  
- SEO/Geo audits → PRs.  
- Voice-driven sprints.  
- n8n pipelines (Reddit→Claude→Telegram, email responders).  
- Metadata-RAG for bank statements/contracts/logs.

---

## 12) Risks & Mitigations

- **Model drift** → golden suites, rollback.  
- **Cost spikes** → local-first, budgets.  
- **Data/secret exposure** → vault, redactions.  
- **Over-autonomy** → consent modes, kill switches.  
- **Supply chain** → lockfiles, SBOM.

---

## 13) New Integrations (Q3–Q4 2025)

- **Agent Lightning RL** — RL fine-tuning on traces.  
- **AlphaEvolve Evolvers** — Evolutionary GPU/data kernel optimization.  
- **MCP + AWS Bedrock** — Enterprise reference backend.  
- **Agentic Web** — Safe interop with external agents.  
- **SuperAGI runtime** — Optional runtime adapter.

---

## 14) Roadmap Extensions

- **Phase I** — RL + Evolvers.  
- **Phase J** — Interop & Enterprise Backends.

---

## 15) Backlog Tasks

- RL scripts (`evaluators/rl/`), Evolver (`introspector/evolver/`), MCP adapters, Agentic Web registry, SuperAGI adapter.  
- Studio panels for RL/Evolver/Agentic Web.

---

## 16) Risks (Extended)

- RL instability → offline only + rollback.  
- Benchmark noise → fixed seeds, datasets.  
- External backends → feature flags, allowlists.  
- Interop security → sandbox, quotas, consent prompts.

---

### Appendices

**A. Local Models**  
- Llama-3.1-70B FP8 TRT-LLM (Planner)  
- DeepSeek-32B (Synth)  
- Qwen-32B-AWQ (Refactor)  

**B. Cloud Pool**  
- GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM  

**C. Key Integrations**  
- Graphiti, LangGraph/CrewAI, ART, Parlant + VibeVoice, MCP, OmniNova, Symphony, Open Computer Agent, unified API brokers, SEO/Geo toolkits, n8n, LFM2, Tensorlake metadata RAG, GPT-OSS, vLLM stack.
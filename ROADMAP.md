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
- **Agents** — Researcher, Coder, Reviewer, Runner, DataOps, Evaluator, Reporter (spawned dynamically with scoped permissions).  
- **Policy Engine** — Tool/network/path allowlists, scopes, rate limits, cost/time ceilings.  
- **Tool/Skill Registry** — JSON Schema contracts, adapters (MCP/HTTP/CLI/DB/Browser/PDF/Vision/ASR/TTS/SEO/Geo).  
- **Memory Fabric** — Episodic, semantic, skill memories, user prefs. Graph-structured (Graphiti).  
- **Evaluators** — Code/test/typing/static analysis, factuality, safety, latency/cost, pass@K.  
- **Introspector** — Summarizes failures, proposes prompt/route/tool upgrades (feeds Self-PR).  
- **Self-PR Bot** — Opens PRs (prompt deltas, router weights, tool config, tests), runs canary, merges if green.  

---

## 3) Self-Rewrite Loop (guarded autonomy)

1. **Collect** failures, slow traces, evaluator misses.  
2. **Propose** minimal diffs (prompts, weights, configs, tests).  
3. **Validate** with unit/property/metamorphic tests, golden prompts (ART), dataset replays, synthetic suites.  
4. **Canary** on shadow traffic with rollback.  
5. **Merge** with provenance + notes.  
6. **Learn** update priors and store counterexamples.  

*Non-goals:* unrestricted self-modification, unsupervised network/file access, secret exfiltration.  

---

## 4) Safety & Capability Governance

- **Modes:** `Guide` (suggest), `Copilot` (confirm), `Auto` (approved scopes).  
- **Boundaries:** vault-scoped secrets; path/domain allowlists; PII classifiers; sandboxed exec.  
- **Kill switches:** pause runs, revoke tokens, quarantine.  
- **Compliance:** immutable audit logs, consent receipts.  

---

## 5) Orchestration & Models

- **Local (DGX Spark)**: Llama-3.1-70B FP8 TRT-LLM, DeepSeek-32B, Qwen-32B-AWQ.  
- **Cloud**: GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM.  
- **Routing:** prefer local, spillover for long-context/specialty. Bandit updates from evaluator win-rates.  

---

## 6) Advanced Capabilities (to integrate)

- **Voice**: Parlant + Whisper/Zonos, multilingual ASR, streaming TTS, barge-in, voice memory, VibeVoice.  
- **Vision/PDF**: OCR → JSON, LaTeX extraction, chart synthesis.  
- **SEO/Geo**: crawlers, SERP diffing, audits, geocoding.  
- **Prompt/Data-Ops**: ART regression tracking, dataset curation.  
- **Workflow Runtimes**: LangGraph/CrewAI optional backends.  
- **Unified API brokers**: RapidAPI-like single-key providers.  
- **n8n Integration**: Export Plan → n8n YAML for low-code pipelines.  
- **Translation**: LFM2-350M JP↔EN outperforming larger models.  
- **vLLM Enhancements**: Paged attention, prefix caching, speculative decoding, multi-GPU/multi-node.  
- **Elastic scaling**: LMCache/NIXL for disaggregated P/D.  
- **Metadata-RAG**: Tensorlake for metadata-augmented embeddings.  
- **OmniNova**: role-based orchestration (Planner/Critic synergy).  
- **Symphony**: decentralized agent consensus & fault tolerance.  
- **MCP**: standard connector for tools/APIs (clients+servers).  
- **Open Computer Agent**: browser/UI automation.  
- **GPT-OSS**: local-first 20B/120B open GPT-class models.  
- **GraphRAG/LazyGraphRAG**: cost-aware graph retrieval.  
- **Mixture-of-Agents**: ensemble orchestration for diversity/consistency.  

---

## 7) Observability & Metrics

- **Traces**: model, tokens, latency, cost, cache, policy, tool effects.  
- **Dashboards**: consensus %, win-rates, KV hit %, spill %, thermo/VRAM.  
- **OpenTelemetry GenAI**: spans for models/agents/tools.  
- **Budgets**: TTFT, ITL, token/sec, costs.  
- **Benchmarks**: regression suites, SWE-bench Verified, LiveBench, AgentBench.  

---

## 8) Phased Delivery Plan

### Phase A (Weeks 1–6): Planning & Policies  
Planner, policy engine, Router v1.  
**Exit:** complex multi-step tasks run safely.  

### Phase B (Weeks 6–12): Multi-Agent & Evaluators  
Dynamic agents, evaluators, Graphiti memory.  
**Exit:** build-and-ship demo passes SLA.  

### Phase C (Weeks 12–20): Self-PRs & Canary  
Self-PR bot, provenance signing, canary/rollback.  
**Exit:** ≥90% self-PRs merge green.  

### Phase D (Weeks 20–28): Multimodal Skills  
Voice I/O, PDF→CSV, SEO/Geo tools.  
**Exit:** voice edits, PDF→charts, SEO PRs.  

### Phase E (Ongoing): Adaptive Router & Skills  
Bandit updates, reusable skill induction.  
**Exit:** faster convergence, lower token costs.  

### Phase F: Automation & APIs  
n8n exports, API brokers, ART prompt regression.  
**Exit:** external automations safe & tested.  

### Phase G: Knowledge & Metadata RAG  
Tensorlake metadata embeddings, page/domain tags.  
**Exit:** cheaper, faster, more accurate retrieval.  

### Phase H: Scaling & Performance  
vLLM multi-GPU/multi-node, LMCache/NIXL, auto-tune.  
**Exit:** near-linear scaling, optimized SLOs.  

### Phase I: Blackwell Presets & Precision  
FP16/FP8/NVFP4 pipelines, canary validation.  
**Exit:** precision switching safe, throughput ↑.  

### Phase J: MCP Hub + n8n  
MCP client/server, VS Code extension, Composio, n8n exporter.  
**Exit:** plug into MCP ecosystem + low-code ops.  

### Phase K: Reasoning Adapter  
Unified “thinking” controls for DeepSeek-R1, o3/o4-mini, Qwen3.  
**Exit:** reasoning costs visible, error rates ↓.  

### Phase L: GraphRAG & LazyGraphRAG  
Selectable vector vs graph retrieval.  
**Exit:** ↑faithfulness on cross-doc queries.  

### Phase M: Observability & Structured Outputs  
OpenTelemetry GenAI spans, schema-first outputs, OWASP guardrails.  
**Exit:** observability by default, safer APIs.  

### Phase N: Bench Harness & Run Cards  
SWE-bench, LiveBench, AgentBench in CI.  
**Exit:** reproducible scores in PRs/releases.  

---

## 9) Engineering Quality Gates

- 100% per-scope test coverage.  
- Static checks: mypy, ESLint, Semgrep, Bandit.  
- Golden prompt suites, property tests, determinism.  

---

## 10) File/Module Backlog

- `schemas/plan.schema.json`  
- `orchestrator/planner.py`  
- `policy/engine.ts` + `router/policy.yaml`  
- `registry/tools.json`  
- `integrations/graphiti/*`  
- `integrations/mcp/*`  
- `tools/exporters/n8n.ts`  
- `rag/graphrag_adapter.py` + `metadata_pipeline.py`  
- `evaluators/*` harness  
- `self_pr/bot.ts` + `.github/workflows/canary.yml`  
- `inference/engines/{vllm,tensorrt_llm,sglang}/`  
- `observability/otel/*`  
- `bench/{swebench,livebench}/docker/*`  
- `voice/*`, `vision/*`, `studio/*`  

---

## 11) Example Use-Cases

- Repo creation from spec → code+CI+deploy.  
- PDF→tables/charts with sanity checks.  
- SEO/Geo audits with PRs.  
- Voice-driven standups, plan edits.  
- n8n pipelines (Reddit→Claude→Telegram).  
- Metadata-RAG for contracts, bank statements.  
- Bench harness proving regression-free upgrades.  

---

## 12) Risks & Mitigations

- **Model drift:** golden suites, canary, evaluator gates.  
- **Cost spikes:** local-first, budgets, adaptive routing.  
- **Data/secret exposure:** vault leases, redaction, allowlists.  
- **Over-autonomy:** mode gating, consent prompts, kill switches.  
- **RL instability (future):** offline only, canary rollback.  
- **Interop security:** sandboxing, quotas, PII redaction.  

---

## Appendices

**A. Local Models**: Llama-3.1-70B, DeepSeek-32B, Qwen-32B-AWQ.  
**B. Cloud Pool**: GPT-4/5, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM.  
**C. Integrations**: Graphiti, Parlant+VibeVoice, ART, MCP, OmniNova, Symphony, Open Computer Agent, API brokers, SEO/Geo, n8n, LFM2, Tensorlake, GPT-OSS, GraphRAG, Mixture-of-Agents, vLLM/TRT-LLM/SGLang, OTel GenAI, SWE-bench/LiveBench.
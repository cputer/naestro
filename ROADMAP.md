# Naestro ROADMAP — Evolving Autonomous System (ASI Trajectory)

**North Star**  
Naestro evolves from a goal-driven multi-agent orchestrator into a continuously self-improving autonomous system that can:  
1. Decompose open-ended goals  
2. Coordinate local+cloud LLMs and tools  
3. Write, test, and ship production-quality code  
4. Operate safely with strong observability and policy gates  
5. Self-improve via guarded self-edits validated by rigorous evaluations  

---

## 0) Current Status (Baseline)

- **Local-first model set (DGX Spark single node):** Llama-3.1-70B (FP8 TRT-LLM) as Judge/Planner; DeepSeek-32B as Proposer/Synth; Qwen-32B-AWQ as Critic/Code. Cloud spillover for GPT-4/5, Claude 3.7+, Gemini 2.5+, Mistral, Grok, OpenELM via vLLM.  
- **Studio (Web UI):** Real-time runs (WS/SSE), dark theme, metrics (workflows, consensus, latency, KV cache hit, cost), traces.  
- **Guardrails:** Thermal/VRAM caps, step-level re-route on OOM/timeouts, retry/backoff, consent prompts for sensitive actions.  
- **SDLC quality:** PR linting, Release Please, Codecov, Node 22 baseline, deterministic UI+Python tests.  

---

## 1) Target Properties

1. **General goal execution** → plans (DAGs) with budgets, SLAs, and success criteria.  
2. **Model+tool orchestration** → telemetry + win-rates for routing.  
3. **Formalized self-improvement** → periodic self-PRs.  
4. **Safety-first autonomy** → provable rollback, human control, strict boundaries.  
5. **Observability & provenance** → explainable, replayable, signed actions.  

---

## 2) System Roles

- **Planner** — compiles `Plan.json`  
- **Router** — model/provider choice (latency, cost, context, win-rates)  
- **Agents** — Researcher, Coder, Reviewer, Runner, DataOps, Evaluator, Reporter  
- **Policy Engine** — allowlists, quotas, cost/time ceilings  
- **Tool/Skill Registry** — typed contracts, adapters (MCP/HTTP/CLI/DB/Browser/PDF/Vision/ASR/TTS/SEO/Geo)  
- **Memory Fabric** — episodic, semantic, skills, prefs (Graphiti)  
- **Evaluators** — code, factuality, safety, latency, cost  
- **Introspector** — extracts lessons, proposes upgrades  
- **Self-PR Bot** — minimal diffs, canary, merges if green  

---

## 3) Self-Rewrite Loop

1. Collect → failures, OOM, policy denials, regressions  
2. Propose → diffs → PRs  
3. Validate → unit + property + golden suites (incl. ART), offline replays  
4. Canary → shadow traffic, rollback on SLO breach  
5. Merge → signed, release notes  
6. Learn → update router priors  

Non-goals: unrestricted self-mod, unsupervised access, exfiltration.  

---

## 4) Safety & Governance

- **Modes**: Guide / Copilot / Auto  
- **Boundaries**: vault, allowlists, sandbox exec, PII classifiers  
- **Kill switches**: pause runs, revoke tokens, quarantine tools  
- **Compliance**: immutable audit logs  

---

## 5) Orchestration & Models

- **Local (DGX Spark):**  
  - Llama-3.1-70B FP8 TRT-LLM (Planner)  
  - DeepSeek-32B (Proposer)  
  - Qwen-32B-AWQ (Critic)  
- **Cloud:** GPT-4/5, Claude 3.7+, Gemini 2.5+, Mistral, Grok, OpenELM  
- **Routing policy:** local-first, bandit updates  

---

## 6) Advanced Capabilities

- **Voice**: Parlant + Whisper/Zonos + VibeVoice  
- **Vision/PDF**: OCR→JSON, LaTeX, charts  
- **SEO/Geo**: crawler, NER, audits, PRs  
- **Prompt/Data-Ops**: ART regression, drift detection  
- **Workflow runtimes**: LangGraph, CrewAI  
- **Unified API brokers**: RapidAPI-style providers  
- **n8n Integration**: export workflows → n8n YAML  
- **Nango Integration**:  
  - Normalized API gateway with 400+ SaaS connectors  
  - MCP adapters for CRM/ERP/Finance APIs  
  - Studio “Integrations Panel” for OAuth + quotas  
  - n8n nodes auto-generated from Nango catalog  
- **Translation**: LFM2-350M JP↔EN  
- **vLLM Enhancements**: paged attention, prefix caching, speculative decoding  
- **Elastic scaling**: LMCache/NIXL KV transfer  
- **Tensorlake RAG**: metadata-augmented retrieval  
- **OmniNova**: planner/critic synergy  
- **Symphony**: decentralized coordination  
- **MCP**: universal protocol  
- **Open Computer Agent**: supervised browser automation  
- **GPT-OSS**: open 20B/120B models  

---

## 7) Observability

- OTEL spans, metrics (latency, cost, tokens, cache hits)  
- Dashboards (Grafana, Prometheus)  
- Benchmarks: golden suites, trendlines, alerts  

---

## 8) Phased Delivery Plan

- **Phase A (Weeks 1–6):** Planner, Policy Engine, Router v1  
- **Phase B (Weeks 6–12):** Multi-agents, Evaluators, Graphiti memory  
- **Phase C (Weeks 12–20):** Self-PRs, Canary+rollback, Prompt-ops  
- **Phase D (Weeks 20–28):** Multimodal, SEO/Geo, cross-device sessions  
- **Phase E (Ongoing):** Adaptive router, skill induction, public “skill market”  
- **Phase F (Add-ons):** n8n + Nango + Unified API brokers + ART tracking  
- **Phase G (Knowledge RAG):** Tensorlake metadata classification  
- **Phase H (Scaling):** vLLM multi-node, LMCache disaggregation  
- **Phase I:** RL fine-tuning (“Agent Lightning”), Evolvers  
- **Phase J:** MCP/Bedrock enterprise backends, Agentic Web, SuperAGI  

---

## 9) Quality Gates

- 100% coverage (branch)  
- Static checks (TS strict, mypy, ESLint, Bandit, IaC lint)  
- Unit + property + metamorphic tests  
- Pinned versions, deterministic seeds  

---

## 10) File/Module Backlog

- `schemas/plan.schema.json`  
- `orchestrator/planner.py` + tests  
- `router/policy.yaml` + `policy/engine.ts`  
- `registry/tools.json` (MCP/HTTP/DB/Browser/ASR/TTS/SEO/Geo)  
- `integrations/nango/*` (connectors, MCP adapters)  
- `tools/exporters/n8n-nodes/nango-*`  
- `studio/panels/nango-connections.tsx`  
- `evaluators/*` harness  
- `self_pr/bot.ts` + canary workflows  
- `voice/*`, `vision/*`, `studio/*`  

---

## 11) Use-Cases

- End-to-end repo creation  
- PDF data → charts with validation  
- SEO/Geo audits with PRs  
- Voice-driven sprints  
- n8n pipelines (Reddit→Claude→Telegram, Email responders)  
- Metadata-RAG (contracts, bank statements)  
- **Nango flows:** SaaS integration (Hubspot, Salesforce, QuickBooks, Slack) in minutes  

---

## 12) Risks

- Model drift → golden suites, rollback  
- Cost spikes → budgets, cache, adaptive routing  
- Data leaks → vault, redaction, allowlists  
- Over-autonomy → kill switches, consent  
- Supply chain → lockfiles, SBOM  
- **Nango:** OAuth scope leakage, misconfigured quotas, adaptive backoff  

---

## 13) New Integrations (Q3–Q4 2025)

- **Agent Lightning (RL)**  
- **AlphaEvolve Evolvers**  
- **MCP + Bedrock Enterprise backend**  
- **Agentic Web (interop)**  
- **SuperAGI runtime (opt-in)**  

---

## 14) Roadmap Phases (Addenda)

- **Phase I:** RL + Evolvers  
- **Phase J:** MCP/Bedrock + Agentic Web + SuperAGI  

---

## 15) Backlog (PRs)

- `evaluators/rl/*`  
- `introspector/evolver/*`  
- `integrations/mcp/*`  
- `gateway/agents-api/*`  
- `runtimes/superagi/*`  
- Studio: RL panels, Agentic Web traces, Nango panel  

---

## 16) Risks & Mitigations (Addendum)

- RL instability → offline + shadow only  
- Benchmark noise → fixed seeds, datasets  
- External backends → flags, allowlists  
- Interop → quotas, consent prompts  
- Nango → OAuth token rotation, audit logs  

---

### Appendices

**A. Local Models (DGX Spark)**  
- Llama-3.1-70B FP8 TRT-LLM — Planner  
- DeepSeek-32B — Synth  
- Qwen-32B-AWQ — Critic  

**B. Cloud Pool**  
- GPT-4/5, Claude 3.7+, Gemini 2.5+, Mistral, Grok, OpenELM  

**C. Key Integrations**  
- Graphiti, LangGraph, CrewAI, ART, Parlant, VibeVoice, MCP, OmniNova, Symphony, Open Computer Agent, Unified API brokers, SEO/Geo, n8n, **Nango**, LFM2, Tensorlake, GPT-OSS, vLLM
# Naestro ROADMAP — Evolving Autonomous System (ASI Trajectory)

**North Star**  
Naestro evolves from a goal-driven multi-agent orchestrator into a continuously self-improving autonomous system that can:  
1. Decompose open-ended goals into executable plans.  
2. Coordinate local + cloud LLMs and external tools.  
3. Write, test, and ship production-grade code and workflows.  
4. Operate safely with strong observability and policy gates.  
5. Self-improve through guarded self-rewrites validated by rigorous evaluation pipelines.  

---

## 0) Current Status (Baseline)

- **Local-first model set (DGX Spark single node):**  
  - Llama-3.1-70B (FP8 TRT-LLM) — Judge/Planner  
  - DeepSeek-32B — Proposer/Synth  
  - Qwen-32B-AWQ — Critic/Refactor  
  - Cloud spillover: GPT-4/5-class, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM.  

- **Studio (Web UI):** Real-time runs (WS/SSE), dark theme, metrics (workflows, consensus, latency, KV cache hit %, cost), run details and traces.  

- **Guardrails:** Thermal/VRAM caps; re-route on OOM/timeouts; retry/backoff; consent prompts for sensitive actions.  

- **SDLC quality:** Commitlint, Release Please, Codecov with per-flag coverage, Node 22 standardization, deterministic UI + Python tests.  

---

## 1) Target Properties

- **General goal execution:** Translate natural-language objectives into DAGs with budgets, SLAs, and acceptance criteria.  
- **Model + tool orchestration:** Route tasks dynamically based on latency, context, cost, and historical success.  
- **Formalized self-improvement:** Self-PRs proposing config, prompt, and routing updates validated by golden tests.  
- **Safety-first autonomy:** Human-in-the-loop modes, rollback mechanisms, consent prompts, strict policy enforcement.  
- **Observability & provenance:** Full traceability, replayable workflows, signed artifacts, immutable logs.  

---

## 2) System Roles

- **Planner** — compiles Goal → `Plan.json`.  
- **Router** — selects best model/provider for each step.  
- **Agents** — Researcher, Coder, Reviewer, DataOps, Evaluator, Reporter.  
- **Policy Engine** — network/tool/path allowlists, cost/time ceilings, secrets vault.  
- **Tool/Skill Registry** — typed contracts, MCP/HTTP/CLI/DB/Browser/PDF/Vision/ASR/TTS/SEO/Geo.  
- **Memory Fabric** — episodic, semantic, skill memory; Graphiti graphs.  
- **Evaluators** — code quality, factuality, safety, latency/cost.  
- **Introspector** — failure analysis, lesson extraction, upgrade proposals.  
- **Self-PR Bot** — opens PRs, runs canary validation, merges if safe.  

---

## 3) Self-Rewrite Loop

1. **Collect:** Failures, slow traces, OOMs, evaluator misses, flaky tests.  
2. **Propose:** Minimal diffs (prompt/router/config/test changes).  
3. **Validate:** Unit + property + metamorphic tests, golden prompts, dataset replays.  
4. **Canary:** Shadow traffic, rollback if SLOs breached.  
5. **Merge:** Signed artifacts, changelog, version bump.  
6. **Learn:** Router priors updated from win-rates.  

---

## 4) Safety & Governance

- **Modes:** Guide, Copilot, Auto.  
- **Boundaries:** Vault secrets, path/domain allowlists, sandboxed exec.  
- **Kill switches:** Pause, revoke tokens, quarantine unsafe tools/models.  
- **Compliance:** Immutable audit logs, provenance, consent receipts.  

---

## 5) Orchestration & Models

- **Local:** Llama-3.1-70B (Judge), DeepSeek-32B (Proposer), Qwen-32B-AWQ (Critic).  
- **Cloud:** GPT-4/5, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM.  
- **Routing:** Prefer local, spill to cloud on context/latency constraints, bandit policy updates.  

---

## 6) Advanced Capabilities

- **Voice:** Whisper/Zonos ASR, multilingual NLU, TTS streaming.  
- **Vision/PDF:** OCR tables, LaTeX → JSON, chart synthesis.  
- **SEO/Geo:** Crawlers, SERP parsers, audits, geocoding APIs.  
- **Prompt/Data-Ops:** ART-style regression tracking, dataset drift detection.  
- **Workflow runtimes:** LangGraph/CrewAI integration.  
- **Unified API brokers:** Single-key access to thousands of APIs.  
- **Self-evolution:** Guarded self-edits, test-driven rewrites, continuous refactor loops.  

---

## 7) Observability & Metrics

- **Traces:** model, tokens, latency, cost, memory I/O.  
- **Dashboards:** consensus %, anomaly flags, win-rates, VRAM use.  
- **Benchmarks:** regression suites, SLA trendlines, external benchmark adapters.  

---

## 8) Phased Plan

- **Phase A (Weeks 1–6):** Planner + policies + router v1 → multi-step tasks with approval.  
- **Phase B (Weeks 6–12):** Multi-agent programs, evaluators, memory slices → end-to-end demo.  
- **Phase C (Weeks 12–20):** Self-PR bot + canary + rollback → weekly self-improvements.  
- **Phase D (Weeks 20–28):** Voice, PDF, SEO/Geo → multimodal skills.  
- **Phase E (Ongoing):** Adaptive router, reusable skills, public skill market.  

---

## 9) Quality Gates

- 100% coverage per area (UI/Server/Python).  
- TS strict, mypy, ESLint, Bandit, IaC lint.  
- Unit + property + metamorphic tests.  
- Pinned versions, deterministic seeds.  

---

## 10) Backlog

- `schemas/plan.schema.json`  
- `orchestrator/planner.py`  
- `policy/engine.ts`  
- `registry/tools.json` adapters  
- `integrations/graphiti/*`  
- `evaluators/*` harness  
- `self_pr/bot.ts` + workflows  
- `voice/*`, `vision/*` modules  
- `studio/*` upgrades  

---

## 11) Use-Cases

- Repo creation (code, tests, CI/CD, docs).  
- PDF/LaTeX → structured tables/charts.  
- SEO/Geo audits with automated PRs.  
- Voice-driven planning and reporting.  

---

## 12) Risks

- **Model regressions** → golden tests + rollback.  
- **Cost spikes** → budgets, cache, routing.  
- **Data leaks** → vault, redaction, allowlists.  
- **Over-autonomy** → consent layers, kill switches.  
- **Supply-chain** → SBOM, signature verification.  

---

## 13) Agent Control Structure (Governance Model)

Naestro orchestrates its agents in **four layered levels**:  

- **Core Layer:** Planner, Router, Policy Engine — sets direction, applies global rules.  
- **Tactical Layer:** Specialized agents (Coder, Researcher, Reviewer, DataOps).  
- **Operational Layer:** Tools, APIs, adapters (SEO/Geo, PDF/ASR, MCP integrations).  
- **Oversight Layer:** Evaluators, Introspector, Self-PR bot — enforce quality, propose improvements, manage feedback loops.  

This layered orchestration model is inspired by hierarchical coordination patterns once observed in Los Angeles in the 1970s (even informal groups like local gangs adopted military-like structures). In Naestro it is translated into **IT governance terms** for agent control: clear roles, escalation paths, redundancy, and fail-safes.  

---

## Appendix

**Local Models:** Llama-3.1-70B, DeepSeek-32B, Qwen-32B-AWQ  
**Cloud Models:** GPT-4/5, Claude 3.7+, Gemini-2.5+, Mistral, Grok, OpenELM  
**Integrations:** Graphiti, LangGraph, CrewAI, ART (prompt regression), Zonos (voice), MCP (tool bus), unified API brokers, SEO/Geo libraries.
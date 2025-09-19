# Naestro ROADMAP — Evolving Autonomous System (ASI Trajectory)

References for external resources are centralized in [REFERENCES.md](REFERENCES.md).
_This roadmap follows the long-term direction in [Naestro VISION](./VISION.md)._

## What's new

- **REFRAG long-context acceleration (2025)** — The latest REFRAG paper introduces a retrieval-
  aware compression pipeline that unlocks ~30.8× faster TTFT (time-to-first-token) while enabling
  16× effective context windows for open-weight models. Read the full paper here:
  [REFRAG: Retrieval Enhanced Fragmentation for Long-Context LLMs (PDF)](https://arxiv.org/pdf/2509.01092).
- **Modular Self-RAG evolution** — Self-RAG is now organized into pluggable retrieval, planning,
  verification, and critique loops so orchestrated agents can adapt depth, abstention, and
  grounding policies per task—directly addressing the systemic gaps surfaced in [RAG’s Biggest Lie].
- **Naestro integration** — Naestro exposes REFRAG through the dedicated REFRAG Controller coupled
  with vLLM/TensorRT-LLM serving adapters so orchestrated agents can transparently benefit from
  accelerated long-context inference.
- **LLM dataset registry stub** — `configs/datasets/llm_datasets.yaml` documents the
  [mlabonne/llm-datasets][LLMDatasets] catalog with disabled-by-default toggles, governance
  checklists, and plan templates so ingestion only proceeds after legal review.

## North Star

Naestro evolves from a goal-driven multi-agent orchestrator into a continuously self-improving
autonomous system that can:

1. decompose open-ended goals;
2. coordinate local+cloud LLMs and tools;
3. write, test, and ship production-quality code;
4. operate safely with strong observability and policy gates;
5. self-improve via guarded self-edits validated by rigorous evaluations.

---

## Technical Foundation

High-performance async Python backend (FastAPI, Uvicorn, asyncio) with Redis (cache/queues), Celery
(background tasks), PostgreSQL (+pgvector), Kubernetes (Helm), OpenTelemetry + Prometheus + Grafana
(observability), Sentry (errors). Policy & auth via OPA/Casbin, Keycloak, Vault. LLM integration
through AnyLLM (plus official SDKs). Safety via NeMo Guardrails / Guardrails AI.

---

## 1) Target Properties (what “evolving ASI” means)

1. **General goal execution** — NL objectives → typed plans (DAGs) with budgets, SLAs, success
   criteria; agentic RAG and adaptive sources.
2. **Model+tool orchestration** — Router chooses LLM/tools using live telemetry + historical
   win-rates; bandit updates; federated learning for privacy.
3. **Formalized self-improvement** — Self-PRs (prompt/router/config/test deltas) gated by
   evals/canary; AlphaEvolve-style optimization for hot paths (see [Bootstrapping Task Spaces]).
   > Backed by recent research (AlphaXiv 2509.02359v1) showing how autonomous agents can decompose
   > tasks, reuse artifacts, and self-improve toward becoming autonomous software engineers.
4. **Safety-first autonomy** — Capability bounds, consent layers, provable rollback, constitutional
   principles, guardrails, HITL (risk trade-offs noted in [Reasoning Introduces New Poisoning
   Attacks Yet Makes Them More Complicated] and [R2AI]).
5. **Observability & provenance** — Logs, metrics, traces; signed artifacts; time-travel debugging;
   metacognitive narratives.
6. **Hallucination-resilience** — Retrieval-first planning, claim verifier, abstention, CoVe;
   citation-grounded outputs (informed by [Why LMs Hallucinate]) and adoption of noise-aware
   retrieval strategies inspired by insights from [RAG’s Biggest Lie].
7. **Long-context acceleration** — REFRAG lane for open-weights (**16×** effective context, ~30×
   TTFT (time-to-first-token)); bypass for closed APIs.
8. **AgentOps maturity** — Multi-agent plans, HITL evaluation, trajectory/final-response scoring,
   production robustness (mitigates [Tool-space interference in the MCP era]).
9. **Preference-optimized policies** — PVPO/DCPO/GRPO-RoC/ARPO/TreePO/MixGRPO/DuPO for stable,
   efficient routing/reasoning.
10. **Runtime interop** — Pluggable runtimes (LangGraph, CrewAI, AgentScope, AutoGen, Agent Squad,
    SuperAGI, Semantic Kernel) under unified policy/trace contracts.
11. **Strategic autonomy & compute economics** — Tokenomics credits/budgets; marketplace for
    skills/agents/data; decentralized delegation (economic framing from [Virtual Agent Economies]).
12. **Advanced cognitive fusion** — Neuro-symbolic (Z3/Prolog), causal AI, multimodal sensor fusion,
    edge/neuromorphic/quantum hooks (built on [Visual Representation Alignment] and [Causal
    Attention with Lookahead Keys]).
13. **No-code enablement** — n8n/Studio flows to compose agents & tools. UI/UX design may draw inspiration from [Huginn]-style event-driven scenario graphs.
14. **Human-AI partnership** — Strategic Dialogue Engine, Oversight Council, narrative explanations.
15. **Resilience & efficiency** — Retries (Tenacity), fallback routing, Redis caching +
    dogpile/singleflight.
16. **SLM-first efficiency** — Router defaults to small language models for lower cost and latency,
    escalating to larger models only when needed. Router may consult resources like SmolHub for
    up-to-date benchmarks on SLM performance/cost tradeoffs.
17. **Ultra-sparse MoE scaling** — Qwen3-Next-80B-A3B uses an ultra-sparse MoE (~3B active params
    per token; extreme low activation ratio), delivering order-of-magnitude efficiency gains over
    Qwen3-32B at 32K+ context [Qwen3-Next Blog][Qwen3-Next].

---

## 2) System Roles (logical components)

- **Planner** — Goal → `Plan.json` (tasks/deps/budgets/acceptance); TreePO branching; neuro-symbolic
  checks; Strategic Dialogue.
- **Router** — Provider/model selection (win-rates, latency, ctx, cost); tokenomics priority;
  federated peer hints; AnyLLM.
- **Agents** — Researcher/Coder/Reviewer/Runner/DataOps/Evaluator/Reporter/Auditor with scoped
  permissions & self-healing.
- **Policy Engine** — OPA/Casbin rules for tools/net/paths/data/rate/cost/time; consent prompts;
  immutable audit.
- **Tool/Skill Registry** — Typed contracts (JSON Schema), adapters
  (MCP/HTTP/CLI/DB/Browser/PDF/Vision/ASR/TTS/SEO/Geo/[n8n]/[Nango]/[Firecrawl]/[Gitingest]).
  - MCP is a first-class integration target for both read (fetch/search) and write (actions)
    connectors [MCP-DevMode]. Naestro can directly compose MCP tools for workflows like Jira
    updates, GitHub/CI operations, Slack/Email, or Zapier/[n8n] automations—while enforcing Policy
    Engine gates (rate/role/domain allowlists), consent prompts, and full trace/provenance.
    - Supports read/fetch and write/actions (e.g., Jira ticket updates, GitHub ops, Slack/Zapier
      flows); composable in multi-tool chains with policy & audit.
  - Vision embeddings: **MetaCLIP2** adapter (encode image/text queries; multilingual).
  - Read-only `FlowTemplateImporter` entries (inputs: template URL/ID + platform tag; outputs:
    temporary artifact bundle + generated `Plan.json`) with policy gates that require explicit
    consent before touching external webhooks or API keys during hydration.

- **Memory Fabric** — Episodic/semantic/skills; vector+graph (Qdrant/Weaviate/Graph store);
  retrieval policies; decision narratives.
- **Evaluators** — Code/static/factuality/safety/latency/cost; trajectory evaluators; AI Safety
  Index gates. Add **visual-grounding checks**: verify that a claimed fact is supported by an image
  region (IoU threshold) and matching caption text; fail if mismatch or low similarity.
- **Claim Verifier** — Chain-of-verification, citations, abstention, uncertainty calibration.
- **Introspector** — Failure mining; lessons; prompt/route/tool upgrades; AlphaEvolve proposals;
  metacog narratives.
- **Self-PR Bot** — Opens PRs; canary; sign/merge with green; escalates constitutional deltas.
- **Evidence Store** — now supports **multimodal artifacts** (images/screenshots/diagrams) with
  vector indices powered by MetaCLIP2; stores region-level boxes/masks for visual citations.
- **REFRAG Controller** — Compression/expansion policy; encoder+projection; vLLM/TRT-LLM hooks.
- **AgentOps Orchestrator** — Capability→trajectory→final evaluators; HITL gates; multi-agent
  metrics. Selects optimal chunking strategy dynamically.
- **PO Policy Module** — Preference optimization suite (PVPO/DCPO/…); stability/effectiveness
  monitors. Integrates the RLLM experiment lane so LLM-feedback reward shaping can directly inform
  policy updates.
- **Collaboration Modes & Depth** — Per-run preferences for orchestrator collaboration with auto
  escalation, budgets, and answer strategies (see
  [docs/orchestrator_collaboration.md](docs/orchestrator_collaboration.md) for details).
- **Runtime Adapters** — [LangGraph]/[CrewAI]/[AgentScope]/[Contains Agents]/[AutoGen]/[Agent
  Squad]/[Semantic Kernel]/[SuperAGI] with policy/trace parity.
- **Plugin Lanes** — Standardized orchestrator channels for turnkey multi-agent workflows that
  ship with guardrails, eval hooks, and policy bindings.
  - **DeepCode lane** — Researcher→Coder→Reviewer→Runner auto-pipeline that ingests research
    artifacts/specs, drafts architecture plans, scaffolds code + tests, runs regression suites,
    and emits policy-compliant PRs for human-in-the-loop merge.
- **ROMA** — Recursive meta-agent runtime for step-by-step decomposition and parallel sub-agent execution.
- **Tokenomics Engine** — Credits/budgets; marketplace transactions.
- **Fusion Controller** — Multimodal stream fusion; neuro-symbolic solvers; causal graphs.
- **Federation Hub** — Cross-instance delegation; Flower-based updates without data sharing.
- **Debugger Module** — Time-travel, branching sims, CoT/ToT graphs.
- **Oversight Council Module** — Governance UI, voting, escalations.
- **Strategic Dialogue Engine** — Interactive co-planning.
- **Observability Core** — OTel spans, Prom metrics, Langfuse traces, Sentry errors.
- **Task Queue & Cache** — Celery + Redis; dogpile.singleflight; TTL caches.
- **Guardrails Service** — NeMo/Guardrails AI validation/filter/correction.

---

## 3) Orchestrator Map (Mermaid)

```mermaid
flowchart TB
  %% ==== Studio (UI) ====
  subgraph Studio["Studio (Web UI)"]
    UI[Runs / Traces / Metrics]
    Consent[Consent Banners]
    Panels[n8n / Nango Panel]
    Debug[Time-Travel Debugger]
    Dialogue[Strategic Dialogue]
    Governance[Oversight Council]
  end

  %% ==== Core ====
  subgraph Core["Naestro Core"]
    Planner[Planner]
    Router[Router]
    Policy[[Policy Engine (OPA/Casbin)]]
    Registry[Tool/Skill Registry]
    Memory[Memory Fabric]
    Evaluators[Evaluators]
    AgentCompanion[Agent Companion Benchmarks]
    Verifier[Claim Verifier (CoVe/Abstain)]
    Introspector[Introspector]
    SelfPR[Self-PR Bot]
    Evidence[Evidence Store]
    REFRAGC[REFRAG Controller]
    PO[PO Policy Module]
    Tokenomics[Tokenomics Engine]
    Fusion[Fusion Controller]
    Federation[Federation Hub]
    Oversight[Oversight Council Module]
    Strategic[Strategic Dialogue Engine]
    Agents[Agents (Researcher/Coder/Reviewer/Runner/...)]
    Observability[Observability Core]
    QueueCache[Celery + Redis Cache]
    Guardrails[Guardrails Service]
    Debugger[Debugger Module]
  end

  %% ==== Engines (Serving) ====
  subgraph Engines["Serving Engines"]
    vLLM[vLLM / SGLang]
    TRT[TensorRT-LLM]
    Triton[Triton Inference Server]
    REFRAGE[REFRAG Encoder + φ Projection]
    Z3[Z3 / Prolog Solvers]
  end

  %% ==== Models (Local) ====
  subgraph Local["Local Models"]
    SLMs[SmolLM3 / Phi-3-mini / Qwen2.5]
    Llama[Llama-4]
    DeepSeek[DeepSeek-V3.1]
    Qwen[Qwen-32B-AWQ]
    Falcon[Falcon-2 MM]
    GPTOSS[GPT-OSS 20B/120B]
  end

  %% ==== Cloud Pool ====
  subgraph Cloud["Cloud Pool"]
    OpenAI[GPT-5 class]
    Claude[Claude 4]
    Gemini[Gemini 3]
    Mistral[Mistral / Grok 4 / OpenELM]
    OSeries[o3 / o4 / o5]
  end

  %% ==== Integrations ====
  subgraph Integrations["Integrations"]
    MCP[MCP Client/Server (read + write)]
    Parlant[Parlant + VibeVoice (ASR/TTS)]
    DIA[DIA TTS (multi-speaker)]
    n8n[n8n Flow Export]
    FlowTemplate[FlowTemplate (Workflow templates: n8n / Make.com / Zapier)]
    Nango[Nango SaaS Hub]
    ART[ART Prompt-Ops]
    Tensorlake[Tensorlake Metadata-RAG]
    OmniNova[OmniNova]
    Symphony[Symphony]
    OCA[Open Computer Agent (Browser/UI)]
    LMCache[LMCache / NIXL KV-Transfer]
    AgentScope[AgentScope Runtime]
    ContainsAgents[Contains Agents Runtime]
    GraphRAG[GraphRAG / LazyGraphRAG]
    Firecrawl[Firecrawl (Web Crawl & Extract)]
    Gitingest[Gitingest (Repo → Digest)]
    NanoBrowser[Nanobrowser (Browser/Web Automation)]
    AutoAgent[AutoAgent (Clustered Agents)]
    AgentSquad[Agent Squad Runtime]
    SuperAGI[SuperAGI Runtime]
    SemKernel[Semantic Kernel]
  end

  %% ==== Experiments ====
  RLLM[RLLM Experiment Lane]

  %% ==== Flows ====
  Studio -->|WS/SSE| Core
  Dialogue --> Planner
  Governance --> Oversight
  Oversight --> Policy
  Planner --> Router
  Policy --> Router
  Registry --> Agents
  Agents --> Engines
  Agents --> Memory
  Evaluators --> Verifier
  Evaluators --> AgentCompanion
  Verifier --> Evidence
  Introspector --> SelfPR
  SelfPR --> Studio
  Memory --> REFRAGC
  REFRAGC --> REFRAGE --> Engines
  PO --> Planner
  PO --> Router
  PO --> REFRAGC
  RLLM --> PO
  Router -->|default| SLMs
  Router -->|escalate| Local
  Router -->|escalate| Cloud
  Tokenomics --> Policy
  Fusion --> Agents
  Federation --> Router
  Observability --> Studio
  Guardrails --> Router
  Debugger --> Studio
  QueueCache --> Agents

  Engines --> Local
  Engines --> Cloud

  %% ==== Integration Wiring ====
  MCP --> Registry
  Agents --> MCP
  Parlant --> Registry
  DIA --> Registry
  n8n --> Panels
  Nango --> Panels
  ART --> Evaluators
  Tensorlake --> Memory
  OCA --> Agents
  LMCache --> Engines
  AgentScope --> Core
  ContainsAgents --> Core
  GraphRAG --> Memory
  Firecrawl --> Evidence
  Gitingest --> Evidence
  AutoAgent --> Core
  AgentSquad --> Core
  SuperAGI --> Core
  SemKernel --> Core
```

---

## 4) Self-Rewrite Loop (guarded autonomy)

Inspired by [Paper2Agent] and [All You Need Is A Fuzzing Brain] for automated self-PR exploration.

1. **Collect**: dropped runs, OOM, policy denials, P95 spikes, evaluator misses, flaky tests; cost
   flags; federated failure sharing.
2. **Propose**: minimal diffs (prompt/router/config/tests) → PRs; AlphaEvolve evo-optimization for
   hot paths.
3. **Validate**: unit/property/metamorphic; golden prompts; offline replays; synthetic suites;
   hallucination red-team; neuro-symbolic checks; constitutional audits; causal validations.
4. **Canary**: shadow traffic; SLO watch (success/latency/cost/safety); auto-rollback on breach;
   proofs for merges.
5. **Merge**: sign artifacts, release notes, version bump; council ratification for flagged PRs.
6. **Learn**: update router priors; store counter-examples; offline RL on traces; federated updates.

**Non-goals**: unrestricted self-modification, unsupervised network/files, secret exfiltration,
constitutional bypass.

---

## 5) Safety & Capability Governance

- **Modes**: Guide (suggest), Copilot (confirm), Auto (approved scopes). Federated (privacy).
  Dialogue (co-planning).
- **Boundaries**: Vault-managed secrets; path/domain allowlists; sandboxed exec;
  FastAPI-Limiter+Redis; PII classifiers; off-prem toggle; export redaction.
- **AuthN/Z**: Keycloak (OIDC/SSO), OPA/Casbin RBAC/ABAC.
- **Kill switches**: pause runs; revoke tokens; quarantine models/tools.
- **Compliance**: immutable audit logs; consent receipts; Safety Index alignment; council audits.
- MCP write actions require explicit scopes, dry-run preview when available, and rollback metadata;
  actions are blocked if provenance or consent is missing.
- **Truthfulness gates**: retrieval-first, inline citations, abstain-on-uncertainty, post-validation
  with NeMo Guardrails.
- **Formal proofs**: TLA+/Coq for Policy Engine & Self-PR merge gate.

---

## 6) Orchestration & Models

### Cloud

- **GPT-5**
- **Gemini-2.5 Pro**
- **Claude**
- **Grok 4** — …
  Currently the closest model …
  Integrated as a cloud escalation lane …
- **Qwen3-Next-80B-A3B** — Ultra-sparse MoE (~3B active params per token; extreme low activation
  ratio). Order-of-magnitude efficiency gains (internal benchmarks show much lower cost/latency than
  Qwen3-32B, especially at 32K+ context) [Qwen3-Next Blog][Qwen3-Next]
- **Ling-flash-2.0 MoE lane** — 100B total parameters with ~6.1B activated (~4.8B non-embedding),
  providing a dedicated sparse MoE route for high-throughput long-context reasoning workloads;
  orchestrator can tap this lane when REFRAG compression demands sparse scaling
  [Ling-flash-2.0][Ling-flash-2.0] — [Ling-flash-2.0 Paper][Ling-flash-2.0 Paper].
- **ERNIE X1.1 (Baidu API, Qianfan)** — agent-tuned reasoning model with strong factuality and
  instruction following; performs on par with GPT-5/Gemini-2.5 Pro [Reuters][ERNIE-Reuters]
  [PRNewswire][ERNIE-PRN].

#### Routing policy

- ERNIE X1.1 is selectable under the Cloud Pool for reasoning/verification tasks, subject to API
  access, latency, and cost.
- Router prefers **MetaCLIP2** for cross-modal queries; falls back to text-only retrieval if no
  visual candidates or low similarity.

### Local

- **Default SLM workers:** SmolLM3 3B, Qwen2.5 3B/7B, Phi-3-mini.

---

## 7) Advanced Capabilities (to integrate)

- **RAG Quality:** …
  - **Post-chunking**: embed whole docs first, split at query-time only on retrieved docs; cache
    chunks for faster reuse; enables query-specific segmentation.
  - **Adaptive & Agentic Chunking**: agents dynamically choose between fixed-size, semantic,
    recursive, hierarchical, or LLM-based splits depending on query, context length, and accuracy
    needs.
  - **Hybrid Pre + Post strategy**: hot paths keep pre-chunks for speed; cold/complex queries use
    post-chunking for accuracy.
  - **Noise-Aware Retrieval Policies**: calibrate embedding scores, rescoring, and fusion to
    suppress noisy passages using diagnostic patterns surfaced in [RAG’s Biggest Lie].
  - **Self-Retrieval Triggers (Self-RAG)**: orchestrator agents introspect reasoning traces and
    confidence signals to autonomously fire follow-up retrieval rounds when coverage gaps mirror
    the failure modes mapped in [RAG’s Biggest Lie].
  - **RAG Evaluation Suite**: dedicated harness tracking retrieval precision/recall, grounding, and
    abstention adherence across synthetic + live corpora informed by the taxonomies in
    [RAG’s Biggest Lie].
- **Hallucination-Resistant Generation (HRG):** Retrieval-first planning, self-consistency,
  chain-of-verification (CoVe), calibrated uncertainty, abstention, structured outputs with JSON
  Schema, and tool-use preference for factual queries.
- **REFRAG Long-Context Acceleration:** compression of retrieved context (k=8–32), KV/cache savings,
  RL/heuristic expansion of critical spans; metrics wired to Observability.
- **Scientific Code Pipelines:** agentic planning → code generation → experiment orchestration →
  evaluation loops tailored for empirical/scientific software; design informed by recent research on
  AI systems that help scientists write expert-level empirical software.
- **Multimodal Search & Retrieval (MetaCLIP2)** — multilingual image↔text embeddings for
  cross-modal search, screenshot/diagram grounding, and gallery/asset retrieval. Integrates with
  Evidence Store so citations can reference an image region + text span. Enables hybrid RAG where
  visual evidence is retrieved alongside text passages.
- **Workflow Template Import** — Naestro can ingest FlowTemplate catalogs (n8n/Make/Zapier) and
  auto-convert them to `Plan.json` while preserving triggers, actions, and policy constraints.
- **MoE-aware routing** — Router ingests expert-activation telemetry/costs to prefer sparse MoE
  lanes (e.g., Ling-flash-2.0) when they yield better quality-per-dollar for long-context runs
  [Ling-flash-2.0][Ling-flash-2.0].

### REFRAG Integration Plan (Naestro)

- **Core components**
  - REFRAG Controller manages compression policies, routing, and observability hooks.
  - Encoder + projection service packages the REFRAG encoder, projection heads, and quantized
    adapters for vLLM/SGLang and TensorRT-LLM backends.
  - Serving hooks expose streaming APIs (AnyLLM/vLLM) with TTFT (time-to-first-token)-aware
    scheduling and KV cache hydration.
  - RL-driven expansion policy selects fragments for reinflation using reward models + bandit
    feedback from downstream evaluators.
  - Multi-tier cache (Redis + disk + object storage) stores compressed fragments, expansion hints,
    and decoder-ready tensors for hot workloads.
- **Pipeline: ingest → query → decode**
  1. Ingest: documents/code/telemetry are chunked, encoded via REFRAG encoder, projected, and stored
     in the Memory Fabric with cache metadata.
  2. Query: retrieval assembles fragment sets, applies compression policies, and hands KV-ready
     packets to serving adapters with policy/audit tags.
  3. Decode: serving hooks hydrate KV cache, apply RL expansion, and stream tokens through
     Guardrails/observability before final responses.
- **Expected wins** — ~30× faster TTFT (time-to-first-token), 16× effective context, and lower
  memory/KV footprints for long-horizon plans.
- **Safety & rollout** — gated by policy toggles, offline eval suites, canary traffic, and HITL
  sign-off; fallback path keeps standard decoding for regressions or safety triggers.

---

## 8) Phased Delivery Plan

### Phase A (Weeks 1–6): Foundational Backend, Planning & Policies

**Goal:** Core API, planner, router, policies.  
**Deliverables:**

- `schemas/plan.schema.json`
- Planner (goal → `Plan.json`)
- Router v1 (heuristics)
- Policy engine (OPA/Casbin rules)
- AnyLLM integration  
  **Exit Criteria:**
- API container deployed
- CI green, >90% coverage
- Goals decomposed → routed to provider
- API key auth working  
  **SLOs:** P95 ≤ 2.5s on baseline; cost logged; no secrets in logs.

---

### Phase B (Weeks 6–12): Observability, Resilience & Multi-Agent Foundations

**Goal:** Monitoring, retries, basic agents.  
**Deliverables:**

- OpenTelemetry + Prometheus + Grafana dashboards
- Tenacity retries + fallback logic
- Memory slice (Qdrant/Weaviate)
- Claim Verifier MVP (citations/abstain)  
  **Exit Criteria:**
- Traces in Jaeger/Tempo
- Metrics (latency, tokens, costs) visible
- Survives provider 429/5xx
- Executes simple multi-agent plan

---

### Phase C (Weeks 12–20): Caching, Self-PRs & Canary Rollouts

**Goal:** Efficiency + self-improvement loop.  
**Deliverables:**

- Redis cache, in-flight dedup (dogpile/singleflight)
- Celery background tasks (analytics/logging)
- Self-PR bot (prompt/router/test PRs)
- Canary + rollback, golden prompt/data suites  
  **Exit Criteria:**
- 90% latency reduction on repeat queries
- Auto-PR merged without regressions
- Canary A/B visible in Grafana

---

### Phase D (Weeks 20–28): Multimodal & Domain Skills

**Goal:** Expand into voice/vision/web.  
**Deliverables:**

- ASR/TTS (Parlant/VibeVoice/DIA)
  - SV2TTS / Real-Time Voice Cloning is prototype-only and not suitable for production.
  - Preferred production TTS: NVIDIA Riva, Coqui XTTS v2, Piper, ElevenLabs, PlayHT, Azure TTS,
    Google TTS, Amazon Polly.
- PDF/OCR (PyMuPDF/Tesseract)
- Playwright browser agent
- Fusion Controller (multimodal I/O)
- **MetaCLIP2** embedding service + vector index; image region extraction (saliency or OCR blocks);
  Studio preview for visual citations. **Exit Criteria:**
- Voice roundtrip working
- PDF → structured JSON
- Browser agent completes form
- Cross-modal search demo (“find the whiteboard with graph about revenue”); answer includes **image
  region citation** and supporting text.

---

### Phase E (Weeks 28–36): Adaptive Router & Skill Induction

**Goal:** Dynamic routing, reusable skills.  
**Deliverables:**

- Bandit router (Thompson sampling)
- Introspector: detect reusable subplans
- Skill registry (typed, versioned)
- RLLM experiment lane — run Reinforcement Learning from LLM feedback to refine preference signals
  that flow into the PO Policy Module.
- InfoSeek evaluation lane — integrate [InfoSeek][InfoSeek] tasks via [InfoSeek Framework][InfoSeek
  Framework] to benchmark deep research planning, researcher evals, and Agentic RAG stress tests.
  **Exit Criteria:**
- Router converges to cheaper/better models
- ≥5 skills encapsulated as registry items

#### Phase E addendum — Scientific Pipelines (MVP)

- Add auto-instrumentation for empirical code (structured logs/metrics, progress events).
- Provide experiment runner adapter (e.g., Hydra or simple CLI runner) with result capture to
  Evidence Store.
- Introduce a scientific-eval harness (sanity checks, unit/metric thresholds; fail-fast on
  regressions). **Exit:** A simple empirical software task (e.g., small dataset experiment) runs
  end-to-end via Naestro agents, logs metrics, and produces a short report.

---

### Phase F (Weeks 36–44): External Automation & Enterprise Auth

**Goal:** SaaS automation + enterprise-ready auth.  
**Deliverables:**

- n8n/Nango adapters
- Keycloak SSO (OAuth2/OIDC)
- Service/tenant accounts
- MCP write-action connectors (Jira/GitHub/Slack/Zapier) with Policy Engine gates and Studio consent
  prompts **Exit Criteria:**
- Export Naestro plan to n8n YAML
- SaaS auth handshake works
- Users log in via SSO
- An MCP-only demo flow (e.g., “parse PR → open Jira → notify Slack”) completes with audit trail,
  consent receipt, and reversible actions

---

### Phase G (Weeks 44–52): Advanced RAG & Ingestion

**Goal:** Metadata RAG + automated ingestion.  
**Deliverables:**

- Metadata-based retrieval (Tensorlake-style)
- Firecrawl (web crawl/extract)
- Gitingest (repo digests)
- FlowTemplate ingestion: parse → map to Tool/Skill Registry → emit Plan.json + consent/policy
  gates.
  **Exit Criteria:**
- Faster, more accurate RAG vs baseline
- URL/repo ingestion → Q&A with citations

---

### Phase H (Weeks 52–60): Scaling & Long Context

**Goal:** Horizontal scale + REFRAG lane.  
**Deliverables:**

- vLLM/TRT multi-node with LMCache KV-transfer
- Helm charts (K8s deployment)
- REFRAG compression lane A/B harness **Exit Criteria:**
- Near-linear throughput scaling
- P95 stable under load
- ≥10× TTFT speedup on long-context with accuracy parity

#### Emerging GPU Kernel Optimizations

Projects like Standard Kernel demonstrate that lightweight, hand-tuned CUDA+PTX kernels can
outperform vendor libraries:

- Matmul at 102–105% cuBLAS in ~100 LOC
- Attention at 104% FlashAttention-3 in ~500 LOC
- Fused LLaMA-3 FFN at 120% PyTorch performance (gpt-fast)

**Relevance to Naestro**: These efforts suggest future router lanes may incorporate
community-optimized kernels (for matmul, attention, FFN) as drop-in backends. Naestro’s REFRAG
Controller and Scaling phases can benefit directly from kernel-gen research, especially in BF16
regimes on H100/next-gen accelerators.

---

### Phase I (Weeks 60–68): Agentic RAG

**Goal:** Multi-agent retrieval & verification.  
**Deliverables:**

- Researcher/Validator agents
- FlowTemplate bootstrap — Researcher/Runner agents import FlowTemplate workflows to accelerate
  plan composition before handing tasks to validators.
- Multi-hop query expansion + evidence synth
- Self-RAG-aligned iterative retrieval loops (retrieve → critique → refine)
- Embedded self-critique routines with traceable verifier feedback cycles
  **Exit Criteria:**
- Complex multi-source Qs solved with documented critique/refine iterations
- Full trace in Studio UI capturing retrieval loops and critique artifacts
- Multi-turn web agent demo (DeepDive-inspired KG+RL data) shows measurable accuracy gains vs. naive
  retrieval, including ablation evidencing the self-critique + iterative retrieval uplift.

---

## 9) Observability & Metrics (OTel + Prometheus)

Evaluator metric design builds on [Statistical Methods in Generative AI]. Instrumentation maintains Agent Companion alignment so benchmark traces map cleanly into the Kaggle reference dashboards.

Every LLM span must include:

- `llm.provider`, `llm.model`
- `llm.input_tokens`, `llm.output_tokens`
- `llm.cost_usd`, `llm.latency_ms`
- `llm.retry_count`, `llm.fallback_provider`
- `llm.cache_hit`, `llm.verifier_pass`
- `llm.citation_count`
- `run.id`, `plan.step`, `agent.role`

**Prometheus exemplars:** allow direct trace drilldowns in Grafana.

- **SLM Utilization KPI** — track SLM vs LLM usage and cost savings.
- MCP Action KPIs — success rate, mean time to apply (MTTA), rollback rate, and policy-blocked
  action rate; link each action to a trace span with tool, scope, and target resource.
- Chunking metrics — track chunking strategy usage (pre vs post vs adaptive), retrieval latency, and
  accuracy uplift.
- **Multimodal KPIs** — image↔text retrieval latency, top‑k recall@{1,5}, cross‑modal MRR,
  visual-grounding pass rate (IoU≥τ), % answers with image citations, storage hit rate for cached
  region crops.
- `rag.context_precision` — measure how much of the retrieved context is actually cited or grounded
  in the final answer, surfacing when retrieval packs spans with irrelevant filler.
- `rag.context_recall` — quantify the fraction of required facts that existed in retrieval but
  failed to appear in the answer, spotlighting when agents ignored pertinent evidence.
- `rag.noise_tolerance_score` — track answer quality as controlled noise is injected into context to
  understand how robust the chain is to distractors versus “RAG’s Biggest Lie” hallucination.
- `rag.leakage_risk` — estimate sensitive or policy-scoped content passed through to answers from
  retrieved context, alerting reviewers when guardrails are bypassed by RAG payloads.
- Template import metrics — instrument FlowTemplate ingestion via `workflow.template_source`,
  `workflow.import_warnings_count`, `workflow.sanitized_nodes_count`, and
  `workflow.simulated_success_rate`.

---

## 10) Caching & Dedup (MVP specifics)

- **Redis cache**: key = hash(model + normalized_prompt + params); TTL; only deterministic (temp=0).
- **In-flight dedup**: asyncio registry + dogpile lock.
- **Background tasks**: non-critical ops via Celery (analytics, log export).
- **Fallback rules**: only cache when safe; mark uncertain results.

---

## Phase J (Weeks 68–76): Enterprise Interop & Advanced Runtimes

**Goal:** Support enterprise ecosystems + modern runtimes.  
**Deliverables:**

- MCP adapter for AWS Bedrock
- Runtime adapters: Agent Squad, SuperAGI, Semantic Kernel, ADK  
  **Exit Criteria:**
- Complex workflow runs on Agent Squad under Naestro’s policies
- Secure delegation via Agentic Web protocol

---

## Phase K (Weeks 76–84): Clustered Swarms & Self-Healing

**Goal:** Fault-tolerant agent swarms.  
**Deliverables:**

- AutoAgent runtime adapter
- Swarm patterns (debate, planner–worker)
- Health checks, auto-respawn, re-routing  
  **Exit Criteria:**
- 100-agent swarm completes large task despite 10% failures
- Self-healing visible in Studio traces

---

## Phase L (Weeks 84–92): Neuro-Symbolic & Sensor Fusion

**Goal:** Formal reasoning + multimodal real-time.  
**Deliverables:**

- Z3/Prolog solver tools
- Fusion Controller: real-time multimodal streams (video/audio, depth, pose, motion masks)
- Evaluation datasets include SpatialVID (7K hours with depth, pose, object masks, motion trends)
  **Exit Criteria:**
- Sudoku/logistics solved with 100% accuracy via solver
- Live video → real-time description by agent

---

## Phase M (Weeks 92–100): Federation, Tokenomics & Marketplace

**Goal:** Decentralization + credits + ecosystem.  
**Deliverables:**

- Flower federated learning (router optimization)
- Tokenomics Engine (credits per action, quotas, budget dashboards)
- Marketplace prototype for agents/tools/skills  
  **Exit Criteria:**
- Two Naestro instances improve routing collaboratively (no data sharing)
- Credits deducted for every agent action
- User rents marketplace agent successfully

---

## Phase N (Weeks 100–108): Constitutional AI & Provable Safety

**Goal:** Safety & ethical guarantees.  
**Deliverables:**

- `constitution.yaml` (principles)
- Evaluator + Policy Engine run compliance checks
- TLA+/Coq proofs for Policy Engine & Self-PR merge  
  **Exit Criteria:**
- Violating plan blocked by Policy Engine, reason logged
- CI includes formal verification step; merges blocked on failure

---

## Phase O (Weeks 108–116): Developer Experience & Debugging

**Goal:** Advanced debugging & visualization.  
**Deliverables:**

- Time-travel debugger (rewind, branch)
- Interactive CoT/ToT graphs in Studio  
  **Exit Criteria:**
- Operator rewinds failing run, modifies state, resumes successfully
- Developer bug resolution time reduced >50%

---

## Phase P (Weeks 116–124): Causal, Neuromorphic & Quantum

**Goal:** Experiment with frontier paradigms.  
**Deliverables:**

- Causal inference (DoWhy) in Introspector
- Hooks for neuromorphic (Intel Loihi) & quantum (D-Wave) inference  
  **Exit Criteria:**
- Introspector distinguishes cause vs correlation in failure analysis
- Demo run completes on neuromorphic/quantum backend

---

### Key Enhancements in Phases J–P

- **Swarms:** resilient, large-scale, explainable multi-agent collaboration.
- **Formal logic:** provable solvers for deterministic tasks.
- **Federation & Tokenomics:** towards a decentralized ecosystem.
- **Governance:** constitutional AI + proofs → highest safety tier.
- **DX:** deep debugging tools for operators.
- **Research Track:** early neuromorphic/quantum hooks gated by feature flags.

---

## Phase Q (Weeks 124–132): No-Code & Hyperautomation

**Goal:** Empower non-technical users + automate full business processes.  
**Deliverables:**

- Studio no-code builder (drag & drop → `Plan.json`)
- Adapters for SAP, Salesforce, long-running workflows  
  **Exit Criteria:**
- User builds agent (e.g., “read email → summarize”) via UI
- Full onboarding workflow automated end-to-end

---

## Phase R (Weeks 132–140): Edge, Robotics & Custom Hardware

**Goal:** Push Naestro beyond data centers.  
**Deliverables:**

- Lightweight agent on Jetson Thor
- Robotics sim with DeepMind Genie 3
- Inference adapters for custom AI chips (Broadcom, OpenAI-designed)  
  **Exit Criteria:**
- Robot completes navigation task in sim
- Latency cut via chip acceleration

---

## Phase S (Weeks 140–148): Pathways to AGI/ASI

**Goal:** Early signs of durable general intelligence.  
**Deliverables:**

- Self-improving “researcher” agents (scientific discovery)
- Long-running meta-agents monitoring/improving Naestro  
  **Exit Criteria:**
- Research agent discovers novel algorithmic improvement
- System shows multi-week goal-directed behavior

---

## Phase T (Weeks 148–156): Governance & Oversight Integration

**Goal:** Mature human oversight layer.  
**Deliverables:**

- Studio module for council voting/audits
- Auditor Agent (impact reports)  
  **Exit Criteria:**
- Major self-PR ratified via council UI before merge
- Auditor report integrated into governance flow

---

## Phase U (Weeks 156–164): Deep Explainability & Introspection

**Goal:** Move from transparency → understanding.  
**Deliverables:**

- Metacognitive narratives (“I chose X because…”)
- Causal failure graphs in debugger  
  **Exit Criteria:**
- Every run has narrative explanation attached
- Visual causal graph for last 5 production failures

### Educational & Introspective References

To support operator understanding and research prototyping, we track minimal, from-scratch LLM
builds that expose gradients and attention at a granular level (scalar autograd / micrograd
lineage). These toy models are not production code; they are used for pedagogy, causal
interventions, and instrumented explanations aligned to Phase U goals.

- [Scalar-Autograd LLM from scratch][ScalarAutogradLLM]

---

## Phase V (Weeks 164–172): Marketplace Ecosystem Launch

**Goal:** Vibrant third-party ecosystem.  
**Deliverables:**

- Public registry for agents/tools/skills
- Tokenomics-based transactions & payouts  
  **Exit Criteria:**
- ≥10 third-party agents available
- First successful credit-based trade executed

---

## Phase W (Weeks 172–180): Full Human-AI Partnership

**Goal:** Seamless co-planning and collaboration.  
**Deliverables:**

- Strategic Dialogue Engine (interactive planning UI)
- “Co-Pilot” default mode for complex workflows  
  **Exit Criteria:**
- Human + Naestro co-create a multi-month plan in one session
- Significant boost in user satisfaction metrics

---

## Always-On Engineering Quality Gates

- **Coverage:** 100% branch coverage (excl. bootstrap).
- **Static checks:** mypy, ESLint, Semgrep/Bandit, IaC lint.
- **Tests:** Unit, property, metamorphic, golden prompt suites.
- **Determinism:** Guard enforces deterministic inference for golden and canary suites.
- **Truthfulness CI:** fail on citation/CoVe regression.
- **REFRAG CI:** block merges on latency/accuracy regressions.
- **Policy CI:** stability & efficiency thresholds enforced.
- **Safety CI:** constitutional checks, Coq/TLA+ proofs.
- **Tokenomics CI:** budget overrun sims.

---

## 11) File/Module Backlog

- `integrations/vision/metaclip2/*` (encoder service, batching, health checks)
- `evidence/vision/*` (image region store, thumbnails, mask/box metadata)
- `evaluators/vision_grounding/*` (IoU, similarity thresholds, tests)
- `studio/components/vision-citation/*` (UI overlay for boxes/masks)
- `fusion/datasets/spatialvid/*` (benchmark loaders, evaluation harness for pose/depth/masks)
- `configs/datasets/llm_datasets.yaml` ([mlabonne/llm-datasets][LLMDatasets] catalog toggle; stay disabled until governance &
  licensing sign-off completes)
- `integrations/datasets/llm_datasets_registry.py` (plan/export helper that keeps mlabonne catalog interactions manual-only)
- `refrag/encoder_service/*` (REFRAG encoder service components for compression/expansion)
- `refrag/policy/*` (reinforcement learning policy modules for routing/optimization)
- `refrag/adapters/vllm/*` (vLLM adapter wiring REFRAG into serving stack)
- `refrag/adapters/trtllm/*` (TensorRT-LLM adapter for REFRAG deployment)
- `refrag/evals/*` (evaluation harnesses validating REFRAG performance)
- `integrations/flowtemplate/*` (catalog connectors, ingestion jobs, consent receipts)
- `converters/flowtemplate/{n8n,make,zapier}/*` (template translators to `Plan.json`)
- `policies/flowtemplate_sanitizers/*` (guardrails for imported triggers/actions/webhooks)
- `evaluators/flowtemplate/*` (dry-run simulators and policy compliance checks)
- `studio/components/flowtemplate-import/*` (Copilot previews, diffing, consent prompts)

---

## 12) Example Use-Cases

- Repo creation from spec (code+tests+CI+deploy).
- PDF → tables/charts with sanity checks.
- SEO/Geo audits + auto-PRs.
- Voice-driven sprints (multi-speaker agent debates).
- SaaS automations (HubSpot→Slack→GitHub).
- Import → Adapt → Run — bring in a FlowTemplate automation (e.g., AI chatbot / HTTP tool /
  web-search agent), preview it in Copilot mode, evaluate the run, then promote it to Auto once the
  evaluators pass.
- Repo ingestion → Q&A with citation-guarantees.
- Whole-report reasoning at speed — REFRAG lets local models read entire docs/logs with accuracy
  parity and dramatically lower latency/cost.
- Complex, evolving knowledge tasks — Agentic RAG refines queries, decomposes steps, and validates
  evidence before answering, increasing accuracy and explainability.
- High-stakes delivery — Contract-adhering agents use precise deliverables/specs, negotiation, and
  subcontracts to achieve production-grade outcomes.
- Scientific / Empirical software assistance — multi-agent workflows that help scientists author,
  instrument, and validate empirical codebases, including automatic experiment setup, metric
  logging, and result sanity checks.
- Autonomous software engineering: Naestro orchestrates coder/reviewer/runner agents in line with
  recent research (AlphaXiv 2509.02359v1), reducing developer effort on large engineering tasks.
- Federated task delegation between orgs.
- Marketplace rentals of expert agents.
- Strategic dialogues for corporate planning.
- **Cross-modal incident triage** — search logs + screenshots ("error dialog about OAuth on
  staging") with visual box citation.
- **Docs & diagrams** — retrieve architecture diagram segments that support a claim and cite the
  exact region.
- **Noise-enhanced retrieval** — inject 10–20% intentionally irrelevant documents into candidate
  pools so Self-RAG’s verifier/planner loops learn to reject spurious hits, a robustness tactic born
  from the [RAG’s Biggest Lie] insight that “perfect retrieval” is a myth and resilience requires
  stress-testing grounding.
- **Agency Automation (n8n + Naestro)** — Kick off Naestro plans from n8n triggers (webhooks, CRM
  updates, incident pings), stream progress back into the FlowTemplate library, and require
  evaluators plus consent prompts before flows escalate from “Copilot” to fully autonomous runs.
- **DeepCode Research→Codebase** — Research agents capture novel papers/specs, auto-summarize
  findings into structured design docs, hand off to coder/reviewer lanes for implementation and
  verification, then raise a policy-compliant PR with test results, documentation, and citations
  ready for human sign-off.

## 13) Risks & Mitigations

- **Visual hallucinations / weak grounding** → require region-level evidence with IoU≥τ and cosine
  similarity≥σ; block delivery if evaluator fails; fall back to text-only RAG.
- **Storage growth** → thumbnail + region-crop tiering; TTL for rarely accessed artifacts;
  object-store lifecycle rules.

---

[Qwen3-Next]: REFERENCES.md#models--architectures
[ERNIE-Reuters]: REFERENCES.md#models--architectures
[ERNIE-PRN]: REFERENCES.md#models--architectures
[MCP-DevMode]: REFERENCES.md#tooling--connectors--protocols
[n8n]: REFERENCES.md#tooling--connectors--protocols
[Nango]: REFERENCES.md#tooling--connectors--protocols
[Ling-flash-2.0]: REFERENCES.md#models--architectures
[Ling-flash-2.0 Paper]: REFERENCES.md#models--architectures
[LLMDatasets]: REFERENCES.md#datasets
[InfoSeek]: REFERENCES.md#datasets
[InfoSeek Framework]: REFERENCES.md#datasets
[RAG’s Biggest Lie]: REFERENCES.md#ref-rags-biggest-lie
[Firecrawl]: REFERENCES.md#retrieval--rag
[Gitingest]: REFERENCES.md#retrieval--rag
[LangGraph]: REFERENCES.md#agent-runtimes--frameworks--interop
[CrewAI]: REFERENCES.md#agent-runtimes--frameworks--interop
[AgentScope]: REFERENCES.md#agent-runtimes--frameworks--interop
[AutoGen]: REFERENCES.md#agent-runtimes--frameworks--interop
[Agent Squad]: REFERENCES.md#agent-runtimes--frameworks--interop
[Semantic Kernel]: REFERENCES.md#agent-runtimes--frameworks--interop
[SuperAGI]: REFERENCES.md#agent-runtimes--frameworks--interop
[Bootstrapping Task Spaces]: REFERENCES.md#research--concepts
[Why LMs Hallucinate]: REFERENCES.md#research--concepts
[Virtual Agent Economies]: REFERENCES.md#research--concepts
[Tool-space interference in the MCP era]: REFERENCES.md#research--concepts
[Reasoning Introduces New Poisoning Attacks Yet Makes Them More Complicated]:
  REFERENCES.md#research--concepts
[R2AI]: REFERENCES.md#research--concepts
[Visual Representation Alignment]: REFERENCES.md#research--concepts
[Causal Attention with Lookahead Keys]: REFERENCES.md#research--concepts
[Paper2Agent]: REFERENCES.md#research--concepts
[All You Need Is A Fuzzing Brain]: REFERENCES.md#research--concepts
[Statistical Methods in Generative AI]: REFERENCES.md#research--concepts
[ScalarAutogradLLM]: REFERENCES.md#educational--introspection

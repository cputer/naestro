# Naestro Roadmap

## 7) Advanced Capabilities (to integrate)

**(Added)** - **Hallucination-Resistant Generation (HRG)**: Retrieval-first planning, **self-consistency**, **chain-of-verification (CoVe)**, **calibrated uncertainty**, **abstention**, **structured outputs** with JSON Schema, and **tool-use preference** for factual queries.  
**(Added)** - **REFRAG Long-Context Acceleration**: compression of retrieved context (k=8–32), KV/cache savings, RL/heuristic expansion of critical spans; metrics wired to Observability.
**(New)** - **Scientific Code Pipelines**: agentic planning → code generation → experiment orchestration → evaluation loops tailored for empirical/scientific software; design informed by recent research on AI systems that help scientists write expert-level empirical software (see References: arXiv:2509.06503).

## 9) Phased Delivery Plan

### Phase E (Ongoing): Adaptive Router & Skill Induction
- Bandit router updates from evaluator win-rates  
- Distill frequent plans into typed, reusable “skills”  
- Public “skill market” with safety metadata  
**Exit**: Faster convergence on plans; fewer tokens per success; richer toolchain with guardrails.

#### Phase E addendum — Scientific Pipelines (MVP)
- Add **auto-instrumentation** for empirical code (structured logs/metrics, progress events).
- Provide **experiment runner adapter** (e.g., Hydra or simple CLI runner) with result capture to Evidence Store.
- Introduce a **scientific-eval harness** (sanity checks, unit/metric thresholds; fail-fast on regressions).
**Exit**: A simple empirical software task (e.g., small dataset experiment) runs end-to-end via Naestro agents, logs metrics, and produces a short, cited report.

## 12) Example Use-Cases Unlocked

**(Added)** - **Whole-report reasoning at speed** — REFRAG lets local models read entire docs/logs with **accuracy parity** and **dramatically lower latency/cost**.
**(Added)** - **Complex, evolving knowledge tasks** — Agentic RAG refines queries, decomposes steps, and validates evidence before answering, increasing accuracy and explainability.
**(Added)** - **High-stakes delivery** — Contract-adhering agents use precise deliverables/specs, negotiation, and subcontracts to achieve production-grade outcomes.
**(New)** - **Scientific / Empirical software assistance** — multi-agent workflows that help scientists author, instrument, and validate empirical codebases (pipelines inspired by “An AI system to help scientists write expert-level empirical software”, arXiv:2509.06503), including automatic experiment setup, metric logging, and result sanity checks.

# REFERENCES

This file centralizes all links to external resources referenced in the Naestro roadmap and related docs. Keep it authoritative and in sync with `docs/Naestro_ROADMAP.md`.

---

## Retrieval & RAG
- **REFRAG (Long-context acceleration)** — https://arxiv.org/abs/2509.01092
- **GraphRAG** — https://github.com/microsoft/graphrag
- **LazyGraphRAG** — https://github.com/microsoft/graphrag
- **Firecrawl (crawl → extract → chunk → index)** — https://github.com/mendableai/firecrawl
- **Gitingest (repo → digest)** — https://github.com/kurtosis-tech/gitingest
- **Tensorlake (metadata-augmented RAG)** — https://github.com/tensorlakeai/tensorlake
- **Agentic RAG (patterns/overview)** — *(internal)* Agents Companion (Feb 2025)

## Scaling / Serving / Optimization
- **vLLM** — https://github.com/vllm-project/vllm
- **TensorRT-LLM** — https://github.com/NVIDIA/TensorRT-LLM
- **TensorRT Model Optimizer (NVIDIA)** — https://github.com/NVIDIA/TensorRT-Model-Optimizer
- **LMCache** — https://github.com/SafeAILab/LMCache
- **Nixl (KV / cache transfer)** — https://github.com/nixl-ai/nixl
- **NVIDIA DGX Spark (Marketplace)** — https://marketplace.nvidia.com/en-us/developer/dgx-spark/
- **NVIDIA DGX Spark Datasheet (PDF)** — https://nvdam.widen.net/s/tlzm8smqjx/workstation-datasheet-dgx-spark-gtc25-spring-nvidia-us-3716899-web

## Agent Runtimes / Frameworks & Interop
- **LangGraph** — https://github.com/langchain-ai/langgraph
- **CrewAI** — https://github.com/joaomdmoura/crewai
- **AgentScope** — https://github.com/modelscope/agentscope
- **AutoGen** — https://github.com/microsoft/autogen
- **SuperAGI** — https://github.com/TransformerOptimus/SuperAGI
- **AutoAgent (clustered swarms)** — https://github.com/SylphAI-Inc/AutoAgent
- **Agent Squad (AWS Labs)** — https://github.com/awslabs/agent-squad
- **Open Computer Agent (OCA)** — https://github.com/oc-agent/oc-agent
- **OmniNova** — https://github.com/omninova-ai/omninova
- **Symphony** — https://github.com/symphony-llm/symphony
- **ART Prompt-Ops** — https://github.com/promptslab/ART
- **finllm-apps (cross-framework finance agents)** — https://github.com/tinztwins/finllm-apps
- **Nebius UDR (Universal Deep Research prototype)** — https://github.com/demianarc/nebiusaistudiodeepresearch
- **Awesome-Nano-Banana-images (edge/device OS images; reference-only)** — https://github.com/PicoTrex/Awesome-Nano-Banana-images

## Voice / Speech
- **Parlant** — https://github.com/parlant-io
- **VibeVoice** — https://github.com/vibevoice
- **DIA TTS** — https://github.com/diattss
- **Qwen3-ASR (Multilingual ASR)**  
  - Blog — https://qwen.ai/blog?id=41e4c0  
  - Hugging Face Demo — https://huggingface.co/spaces/Qwen/Qwen3-ASR  
  - ModelScope Studio — https://modelscope.cn/studios/Qwen/Qwen3-ASR  
  - API (Bailian) — https://bailian.console.alibabacloud.com/?tab=doc#/doc/  
  - Main site — https://qwen.ai/  
  - Model card — https://huggingface.co/Qwen/Qwen3-ASR

## Safety / Policy / AuthN/Z
- **NeMo Guardrails** — https://github.com/NVIDIA/NeMo-Guardrails
- **Guardrails AI** — https://github.com/shreyar/guardrails
- **OPA (Open Policy Agent)** — https://github.com/open-policy-agent/opa
- **Casbin** — https://github.com/casbin/casbin
- **Keycloak** — https://www.keycloak.org/

## Agent Learning / RL / Evolution
- **Agent Lightning** — https://huggingface.co/papers/2409.00422
- **AlphaEvolve (performance-guided codegen)** — https://arxiv.org/abs/2409.00567
- **Reinforcement Learning for ML Engineering Agents** — https://arxiv.org/abs/2509.01684

## Preference Optimization (PO) — policies we reference
- **PVPO** — https://arxiv.org/abs/2406.02800  
- **DCPO** — https://arxiv.org/abs/2406.09275  
- **GRPO-RoC** — https://arxiv.org/abs/2407.01599  
- **ARPO** — https://arxiv.org/abs/2407.06580  
- **TreePO** — https://arxiv.org/abs/2407.04012  
- **MixGRPO** — https://arxiv.org/abs/2407.11000  
- **DuPO** — https://arxiv.org/abs/2408.01999  
> If your team prefers different canonical papers for these, replace links in a follow-up commit and update `po_policies/README.md`.

## Federation / Causality
- **Flower (federated learning)** — https://github.com/adap/flower
- **DoWhy (causal inference)** — https://github.com/py-why/dowhy

## Model Architecture Overviews
- **Sebastian Raschka — The Big LLM Architecture Comparison (2025)** — https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison

---

Maintenance:
- Keep this list in sync with `docs/Naestro_ROADMAP.md` sections **Integrations**, **Advanced Capabilities**, **Phases**, and **Appendices**.
- CI link-check ensures URLs stay alive; see `.github/workflows/reference-link-check.yml`.

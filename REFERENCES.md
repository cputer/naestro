# REFERENCES

This file centralizes all links to external resources referenced in the Naestro roadmap and related
docs. Keep it authoritative and in sync with `ROADMAP.md`. For collaboration modes, consult the
[orchestrator collaboration guide](docs/orchestrator_collaboration.md).

---

## Research & Concepts

- Tool-space interference in the MCP era
- Paper2Agent
- Virtual Agent Economies
- Bootstrapping Task Spaces for Self-Improvement
- The Illusion of Diminishing Returns: Measuring Long Horizon Execution in LLMs
- Why Language Models Hallucinate
- Reasoning Introduces New Poisoning Attacks Yet Makes Them More Complicated
- All You Need Is A Fuzzing Brain
- R2AI: Towards Resistant and Resilient AI in an Evolving World
- Statistical Methods in Generative AI
- Language Self-Play For Data-Free Training
- Causal Attention with Lookahead Keys
- Visual Representation Alignment for Multimodal LLMs
- “Curated by TuringPost (Sept 2025): <https://turingpost.com/p/fod118>”

## Models / Architectures

- **ERNIE X1.1 (Wave Summit 2025 release)**
  - Main site — <https://ernie.baidu.com>
  - Press — Reuters —
    <https://www.reuters.com/technology/artificial-intelligence/chinas-baidu-launches-two-new-ai-models-industry-competition-heats-up-2025-03-16/>
  - Press — PRNewswire —
    <https://www.prnewswire.com/news-releases/baidu-unveils-reasoning-model-ernie-x1-1-with-upgrades-in-key-capabilities-302551170.html>

- **NVIDIA — Small Language Models for Agentic AI (2025)** —
  <https://www.vectrix.ai/blog-post/understanding-large-and-small-language-models-key-differences-and-applications>
- **SmolLM3** — <https://huggingface.co/HuggingFaceTB/SmolLM3-3B>
- **SmolHub (SLM Benchmark/Directory)** — <https://www.smolhub.com/smolhub>
- **Phi-3-mini** — <https://huggingface.co/microsoft/phi-3-mini-4k-instruct>
- **Qwen2.5** — <https://huggingface.co/Qwen>
- **Qwen3-Next (A3B series)**
  - Blog —
    <https://qwen.ai/blog?from=research.latest-advancements-list&id=4074cca80393150c248e508aa62983f9cb7d27cd>
  - vLLM support — <https://blog.vllm.ai/2025/09/11/qwen3-next.html>
  - NVIDIA Model Card — <https://build.nvidia.com/qwen/qwen3-next-80b-a3b-thinking/modelcard>

## Datasets

- **SpatialVID** — *A Large-Scale Video Dataset with Spatial Annotations* (NJU-3DV, 2025).
  ~7K hours of video with annotations: camera pose, depth maps, dynamic object masks, scene text descriptions (camera, motion trends, summary).
  Project — <https://nju-3dv.github.io/projects/SpatialVID>

## Retrieval & RAG

- **REFRAG: Rethinking RAG based Decoding** — Xiaoqiang Lin et al. (Meta Superintelligence Labs; NUS; Rice) — arXiv:2509.01092 (1 Sep 2025)
  - PDF — <https://arxiv.org/pdf/2509.01092>
  - Code — _link TBD_
  - Summary — Reuses retrieval across decoding to accelerate streaming RAG, yielding ~30.8× faster TTFT, 16× longer context handling, and no accuracy loss.
- **GraphRAG** — <https://github.com/microsoft/graphrag>
- **LazyGraphRAG** — <https://github.com/sanikacentric/LazyGraphRAG>
- **Firecrawl (crawl → extract → chunk → index)** — <https://github.com/mendableai/firecrawl>
- **Gitingest (repo → digest)** — <https://github.com/coderamp-labs/gitingest>
- **Tensorlake (metadata-augmented RAG)** — <https://github.com/tensorlakeai/tensorlake>
- **Agentic RAG (patterns/overview)** — _(internal)_ Agents Companion (Feb 2025)
- **Advanced Chunking Strategies for RAG (Weaviate Blog, 2025)** —
  <https://weaviate.io/blog/chunking-strategies-for-rag>

## Scaling / Serving / Optimization

- **vLLM** — <https://github.com/vllm-project/vllm>
- **TensorRT-LLM** — <https://github.com/NVIDIA/TensorRT-LLM>
- **TensorRT Model Optimizer (NVIDIA)** — <https://github.com/NVIDIA/TensorRT-Model-Optimizer>
- **LMCache** — <https://github.com/LMCache/LMCache>
- **NIXL (KV / cache transfer)** — <https://github.com/ai-dynamo/nixl>
- **NVIDIA DGX Spark (Workstation page)** —
  <https://www.nvidia.com/en-us/products/workstations/dgx-spark/>
- **NVIDIA DGX Spark Datasheet (PDF)** —
  <https://nvdam.widen.net/s/tlzm8smqjx/workstation-datasheet-dgx-spark-gtc25-spring-nvidia-us-3716899-web>

## Agent Runtimes / Frameworks & Interop

- **LangGraph** — <https://github.com/langchain-ai/langgraph>
- **CrewAI** — <https://github.com/joaomdmoura/crewai>
- **AgentScope** — <https://github.com/modelscope/agentscope>
- **AutoGen** — <https://github.com/microsoft/autogen>
- **SuperAGI** — <https://github.com/TransformerOptimus/SuperAGI>
- **AutoAgent (clustered swarms)** — <https://github.com/Link-AGI/AutoAgents>
- **Agent Squad (AWS Labs)** — <https://github.com/awslabs/agent-squad>
  - Docs — <https://awslabs.github.io/agent-squad/>
- **Semantic Kernel** — <https://github.com/microsoft/semantic-kernel>
- **Open Computer Agent (OCA)** — _link unavailable_
- **OmniNova** — <https://github.com/LuChenCornell/OmniNova>
- **Symphony** — _link unavailable_
- **ART Prompt-Ops** — _link unavailable_
- **finllm-apps (cross-framework finance agents)** — <https://github.com/tinztwins/finllm-apps>
- **Nebius UDR (Universal Deep Research prototype)** —
  <https://github.com/demianarc/nebiusaistudiodeepresearch>
- **SFR-DeepResearch (self-factored retrieval)** — _link unavailable_
- **Awesome-Nano-Banana-images (edge/device OS images; reference-only)** —
  <https://github.com/PicoTrex/Awesome-Nano-Banana-images>

## Vision / Multimodal

- **MetaCLIP2 (multilingual vision-text embeddings)** —
  <https://huggingface.co/docs/transformers/model_doc/metaclip2>
- **Transformers (integration docs)** — <https://huggingface.co/docs/transformers/index>
- **Text↔Image search notebook (example)** —
  <https://github.com/huggingface/notebooks/blob/main/examples/image_similarity.ipynb>

## Voice / Speech

- **Parlant** — <https://github.com/parlant-io>
- **VibeVoice** — <https://github.com/vibevoice>
- **DIA TTS** — <https://github.com/diatts>
- **Qwen3-ASR (Multilingual ASR)**
  - Blog — <https://qwen.ai/blog?id=41e4c0f2a632d9ec23a7c51a47f0f16f>
  - Announcement Tweet — <https://x.com/Alibaba_Qwen/status/1965068737297707261>
  - Coverage —
    <https://www.marktechpost.com/2025/09/09/alibaba-qwen-team-releases-qwen3-asr-a-new-speech-recognition-model-built-upon-qwen3-omni-achieving-robust-speech-recogition-performance/>
  - Hugging Face Demo — <https://huggingface.co/spaces/Qwen/Qwen3-ASR-Demo>
  - ModelScope Studio — <https://modelscope.cn/studios/Qwen/Qwen3-ASR>
  - API (Bailian) — <https://bailian.console.alibabacloud.com/?tab=doc#/doc/>
  - Main site — <https://qwen.ai/>
  - Model card — <https://modelscope.cn/models/Qwen/Qwen3-ASR/summary>
- **NVIDIA Riva TTS** — <https://developer.nvidia.com/riva>
- **Coqui XTTS v2** — <https://huggingface.co/coqui/XTTS-v2>
- **Piper** — <https://github.com/rhasspy/piper>
- **ElevenLabs** — <https://elevenlabs.io>
- **PlayHT** — <https://play.ht>
- **Azure Neural TTS** — <https://azure.microsoft.com/products/ai-services/text-to-speech>
- **Google WaveNet / Studio Voices** — <https://cloud.google.com/text-to-speech>
- **Amazon Polly** — <https://aws.amazon.com/polly/>

## Safety / Policy / AuthN/Z

- **NeMo Guardrails** — <https://github.com/NVIDIA/NeMo-Guardrails>
- **Guardrails AI** — <https://github.com/shreyar/guardrails>
- **OPA (Open Policy Agent)** — <https://github.com/open-policy-agent/opa>
- **Casbin** — <https://github.com/casbin/casbin>
- **Keycloak** — <https://www.keycloak.org/>

## Agent Learning / RL / Evolution

- **Agent Lightning** — <https://arxiv.org/abs/2409.00422>
- **AlphaEvolve (performance-guided codegen)** — <https://arxiv.org/abs/2409.00567>
- **Reinforcement Learning for ML Engineering Agents** — <https://arxiv.org/abs/2509.01684>

## Preference Optimization (PO) — policies we reference

- **PVPO** — <https://arxiv.org/abs/2406.02800>
- **DCPO** — <https://arxiv.org/abs/2406.09275>
- **GRPO-RoC** — <https://arxiv.org/abs/2407.01599>
- **ARPO** — <https://arxiv.org/abs/2407.06580>
- **TreePO** — <https://arxiv.org/abs/2407.04012>
- **MixGRPO** — <https://arxiv.org/abs/2407.11000>
- **DuPO** — <https://arxiv.org/abs/2408.01999>
  > If your team prefers different canonical papers for these, replace links in a follow-up commit
  > and update `po_policies/README.md`.

## Federation / Causality

- **Flower (federated learning)** — <https://github.com/adap/flower>
- **DoWhy (causal inference)** — <https://github.com/py-why/dowhy>

## Tooling / Connectors / Protocols

- **Model Context Protocol (MCP)** — <https://modelcontextprotocol.io/>
- **OpenAI adds powerful but dangerous support for MCP in ChatGPT Dev Mode (VentureBeat)** — _link
  unavailable_
- **Zapier Platform** — <https://platform.zapier.com/>
- **Jira Cloud Platform** — <https://developer.atlassian.com/cloud/jira/platform/>
- **n8n (workflow automation)** — <https://n8n.io>
- **Nango (SaaS integrations)** — <https://nango.dev>
- **Nanobrowser** — open-source Chrome extension for AI-powered web automation.
  - Runs multi-agent workflows via user-supplied LLM API keys.
  - GitHub — <https://github.com/nanobrowser/nanobrowser>

## Model Architecture Overviews

- **Sebastian Raschka — The Big LLM Architecture Comparison (2025)** —
  <https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison>

## Code Generation / Scientific Software

- **An AI system to help scientists write expert-level empirical software** —
  <https://arxiv.org/abs/2509.06503>

## Autonomous Software Engineering / Research Foundations

- **Foundations for Artificial Autonomous Software Engineers** —
  <https://www.alphaxiv.org/abs/2509.02359v1>
  - PDF — <https://papers-pdfs.assets.alphaxiv.org/2509.02359v1.pdf>

---

Maintenance:

- Keep this list in sync with `ROADMAP.md` sections **Integrations**, **Advanced Capabilities**,
  **Phases**, and **Appendices**.
- CI link-check ensures URLs stay alive; see `.github/workflows/reference-link-check.yml`.

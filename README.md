# NAESTRO — Orchestrator Platform

<p align="center">
  <img src="docs/naestro-logo.svg" alt="NAESTRO Logo" width="300"/>
</p>

**Production-grade LLM orchestrator** with [LangGraph](https://www.langchain.com/langgraph) workflow execution, [pgvector](https://github.com/pgvector/pgvector) powered RAG, secure code sandboxing, and multi-model routing.

---

## ✨ Key Features

- **LangGraph-based Orchestration** – Design, execute, and monitor multi-step AI workflows using the LangGraph execution model.
- **Multi-Model Routing** – Dynamically route queries to the most appropriate model (OpenAI, Anthropic, local LLMs, etc.) based on context and performance.
- **pgvector RAG** – Store and retrieve embeddings directly in Postgres with pgvector for high-performance retrieval augmented generation.
- **Secure Sandbox** – Execute untrusted code or model tools in an isolated, resource-controlled environment.
- **Event-Driven Architecture** – Subscribe to and trigger workflow events via queues and webhooks.
- **Plugin System** – Extend orchestration with custom tools, memory modules, and connectors.

---

## 🏗 Architecture

**NAESTRO** is composed of:

1. **Workflow Engine** — built on LangGraph, defining execution nodes and edges.
2. **RAG Layer** — Postgres + pgvector for context retrieval and augmentation.
3. **Routing Layer** — multi-LLM routing with performance and cost-aware strategies.
4. **Sandbox** — containerized execution environment for code/tools.
5. **API Gateway** — REST & WebSocket endpoints for clients and integrations.
6. **UI Dashboard** — monitor workflows, inspect logs, and manage configurations.

```
[ Client Apps ] ⇄ [ API Gateway ] ⇄ [ Workflow Engine (LangGraph) ]
                                         ⇣
                                     [ RAG Layer (pgvector) ]
                                         ⇣
                                   [ Multi-Model Router ]
                                         ⇣
                                   [ Secure Sandbox ]
```

---

## 📦 Installation

```bash
git clone https://github.com/<your-org>/naestro.git
cd naestro
cp .env.example .env   # set environment variables
docker-compose up -d   # run Postgres + pgvector + other deps
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### 1. Start the Orchestrator
```bash
python -m naestro.server
```

### 2. Create a Workflow
Example in `examples/basic_workflow.py`:
```python
from naestro import Workflow, Node

wf = Workflow("demo")
wf.add(Node("input"))
wf.add(Node("process", model="gpt-4"))
wf.add(Node("output"))

wf.run("Hello, NAESTRO!")
```

### 3. Use the RAG Layer
```python
from naestro.rag import RAG

rag = RAG()
rag.add_document("The Eiffel Tower is in Paris.")
print(rag.query("Where is the Eiffel Tower?"))
```

---

## ⚙️ Configuration

Environment variables (`.env`):
```ini
DATABASE_URL=postgresql://user:pass@localhost:5432/naestro
OPENAI_API_KEY=sk-...
SANDBOX_ENABLED=true
```

---

## 🧩 Extending NAESTRO

Create a new plugin in `plugins/`:
```python
from naestro.plugin import BasePlugin

class MyPlugin(BasePlugin):
    def execute(self, **kwargs):
        return "Custom logic here"
```

---

## 📊 Roadmap

- [ ] LangGraph visual editor in dashboard
- [ ] Vector store sync to S3/GCS
- [ ] Fine-tuned model registry
- [ ] Sandbox GPU support
- [ ] Built-in evaluation suite

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

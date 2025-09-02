# Naestro

Naestro is a production-ready orchestrator for large-language-model workflows. It offers multi-model routing, LangGraph-based execution, RAG with pgvector, sandboxed verification, and comprehensive observability.

## Features
- Agentic workflows built with LangGraph.
- Routing across NVIDIA NIM, vLLM, and small models.
- PostgreSQL/pgvector-backed retrieval‑augmented generation.
- Seccomp-restricted sandbox for untrusted code.
- OpenTelemetry + Prometheus integration.

## Quick Start
```bash
docker compose up -d --profile core
curl http://localhost:8080/health
curl http://localhost:8081/health
```

## Local Development

```bash
pip install -r requirements.lock
uvicorn src.orchestrator.main:app --reload --port 8081 &
uvicorn src.gateway.main:app --reload --port 8080 &
```

## Testing

```bash
pre-commit run --files <file>
pytest
```

## Contributing

Issues and pull requests are welcome. Please run linters and tests before submitting.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

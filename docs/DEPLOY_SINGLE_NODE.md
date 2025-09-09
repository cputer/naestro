# Deploy Single Node

[← Back to README](../README.md)

## TL;DR

| Step           | Command                             | Notes                          |
| -------------- | ----------------------------------- | ------------------------------ |
| Build images   | `docker compose build`              | Prepare containers             |
| Start services | `docker compose up -d`              | Launch orchestrator and models |
| Validate       | `curl http://localhost:8000/health` | Should return `ok`             |

## Overview

Run Naestro and supporting services on a single machine using Docker Compose.

## Steps

1. Ensure Docker and Docker Compose are installed.
2. Build images and start services using the compose file.
3. Monitor logs with `docker compose logs -f`.

## Validation

Send a test prompt through the API or UI and confirm a response.

## Troubleshooting

| Issue                       | Resolution                                   |
| --------------------------- | -------------------------------------------- |
| Containers failing to start | Check Docker logs and available resources    |
| Ports conflict              | Adjust exposed ports in `docker-compose.yml` |

---

See also: [INTEGRATIONS](INTEGRATIONS.md) · [GRAPHITI](GRAPHITI.md) ·
[UI_API_CONTRACT](UI_API_CONTRACT.md) · [DEPLOY_SINGLE_NODE](DEPLOY_SINGLE_NODE.md)

### Optional: Apple OpenELM Router (vLLM)

You can run a lightweight local router/assistant using **Apple/OpenELM-3B-Instruct** via **vLLM**
with an OpenAI-compatible API:

```bash
pip install vllm

python -m vllm.entrypoints.openai.api_server \
  --model apple/OpenELM-3B-Instruct \
  --host 0.0.0.0 \
  --port 8602 \
  --gpu-memory-utilization 0.85
```

This exposes an OpenAI-style endpoint at `http://localhost:8602/v1`. Adjust
`--gpu-memory-utilization` or add flags like `--max-model-len` depending on your GPU VRAM.

Update `config/providers.yaml` to add the provider (see “Apple OpenELM router provider” example).

# Deploy Multi Node

[\u2190 Back to README](../README.md)

## Overview

Run Naestro across multiple DGX Spark desktops. This setup spreads inference services over several
hosts while a single gateway and orchestrator coordinate requests.

## Networking

- Ensure each DGX is reachable over the network (e.g. `dgx-a`, `dgx-b`).
- Open the inference ports (8001\-8003 by default) on each host.
- Optionally place nodes on an isolated subnet for lower latency.

## Orchestration

1. On **each** DGX host, start the Naestro services:

   ```bash
   docker compose up -d --profile core inference
   ```

2. Copy `config/providers.yaml` and point each provider's `endpoint` to the correct host (see
   example below).
3. Set `MODEL_HOSTS` in `.env` to a comma-separated list of DGX hostnames.

## Load Balancing

- Duplicate provider entries for each DGX with unique `id` and `endpoint` values.
- Increase `routing.limits.max_concurrency` to reflect the number of hosts.
- Naestro will route requests across all listed providers in a round-robin fashion.

## Example

`config/providers.yaml`

```yaml
inference:
  local:
    - id: llama70b_judge_dgx_a
      endpoint: http://dgx-a:8001
    - id: llama70b_judge_dgx_b
      endpoint: http://dgx-b:8001
routing:
  limits:
    max_concurrency: 16
```

## Validation

Send a test prompt to the gateway and verify that responses are returned from each host.

## Troubleshooting

| Issue             | Resolution                                            |
| ----------------- | ----------------------------------------------------- |
| Nodes unreachable | Check firewall rules and hostnames                    |
| Uneven load       | Confirm `max_concurrency` and provider IDs are unique |
| Slow responses    | Verify network bandwidth between hosts                |

---

See also: [INTEGRATIONS](INTEGRATIONS.md) · [GRAPHITI](GRAPHITI.md) ·
[UI_API_CONTRACT](UI_API_CONTRACT.md) · [DEPLOY_SINGLE_NODE](DEPLOY_SINGLE_NODE.md)

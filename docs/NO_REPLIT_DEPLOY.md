# No Replit Deploy

[← Back to README](../README.md)

## TL;DR

| Step                 | Command                                            | Notes                                |
| -------------------- | -------------------------------------------------- | ------------------------------------ |
| Clone repository     | `git clone https://github.com/naestro/naestro.git` | Perform on a local machine or server |
| Install dependencies | `pip install -r requirements.txt`                  | Use Python 3.10+                     |
| Run orchestrator     | `python -m src.main`                               | Starts API on port 8000              |

## Overview

Instructions for deploying Naestro without relying on Replit.

## Steps

1. Ensure Docker or Python environment is available.
2. Clone the repository and install dependencies.
3. Configure environment variables as needed.
4. Start the orchestrator service.

## Validation

Access `http://localhost:8000/health` to confirm the service is running.

## Troubleshooting

| Issue                  | Resolution                         |
| ---------------------- | ---------------------------------- |
| Missing Python headers | Install `python3-dev` on the host  |
| Port already in use    | Adjust `PORT` environment variable |

---

See also: [INTEGRATIONS](INTEGRATIONS.md) · [GRAPHITI](GRAPHITI.md) ·
[UI_API_CONTRACT](UI_API_CONTRACT.md) · [DEPLOY_SINGLE_NODE](DEPLOY_SINGLE_NODE.md)

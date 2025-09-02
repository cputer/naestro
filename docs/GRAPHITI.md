# Graphiti Runbook

## TL;DR
| Step | Command | Notes |
|------|---------|-------|
| Deploy Graphiti service | `docker compose up graphiti` | Runs local graph engine |
| Configure Naestro | set `GRAPHITI_URL` and `GRAPHITI_API_KEY` | Include optional semaphore limit |
| Verify connectivity | `curl $GRAPHITI_URL/health` | Should return `ok` |

## Overview
Graphiti provides bi-temporal, persistent memory for Naestro orchestration.

## Steps
### Deploy Graphiti
Launch the Graphiti container or binary along with a compatible graph database backend.

### Configure Naestro
Set the environment variables and enable the Graphiti client in the orchestrator configuration.

### Validate
Start Naestro and ensure episodes are recorded and retrieved through the Graphiti endpoints.

## Troubleshooting
| Symptom | Fix |
|---------|-----|
| Connection refused | Check that Graphiti is listening on the expected port |
| Missing episodes | Confirm the client is calling `recordEpisode` and `context.assemble` |
| Slow queries | Tune `GRAPHITI_SEMAPHORE_LIMIT` and review backend performance |

# Integrations Runbook

[← Back to README](../README.md)

## TL;DR
| Integration | Purpose | Configuration |
|-------------|---------|---------------|
| Graphiti | Real-time knowledge graph memory | Set `GRAPHITI_URL` and `GRAPHITI_API_KEY` |
| VS Code Extension | Developer tooling for local agents | Install Naestro VS Code extension |
| UI API | Contract between UI and core | See `UI_API_CONTRACT.md` |

## Summary
This runbook outlines how Naestro connects to optional components and developer tools.

## Steps
1. Set the necessary environment variables for each integration.
2. Restart the orchestrator to pick up configuration changes.
3. Validate each integration using health checks or sample commands.

## Validation
- Graphiti: `curl $GRAPHITI_URL/health`
- VS Code: verify extension activates in the editor.
- UI API: check API responses match contract.

## Troubleshooting
| Issue | Resolution |
|-------|-----------|
| Missing API key | Ensure secret is set in environment or `.env` file |
| Extension not loading | Restart VS Code and check logs |
| API mismatch | Compare request/response with contract table |

---

See also: [INTEGRATIONS](INTEGRATIONS.md) · [GRAPHITI](GRAPHITI.md) · [UI_API_CONTRACT](UI_API_CONTRACT.md) · [DEPLOY_SINGLE_NODE](DEPLOY_SINGLE_NODE.md)

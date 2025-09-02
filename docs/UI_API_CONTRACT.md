# UI API Contract

[← Back to README](../README.md)

## TL;DR
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tasks` | GET | List running tasks |
| `/api/tasks` | POST | Create a new task |
| `/api/events` | SSE | Stream agent events for a task |

## Overview
This document defines the contract between Naestro's UI and core API service.

## Real-time Connections
Clients should send a heartbeat on the WebSocket at the interval defined by `WS_HEARTBEAT_MS`. When WebSockets are unavailable, fall back to the Server-Sent Events stream exposed at `/api/events`.

## Payloads
| Field | Type | Notes |
|-------|------|-------|
| `id` | string | Unique task identifier |
| `prompt` | string | User request submitted via UI |
| `status` | enum | `pending`, `running`, or `done` |

## Error Codes
| Code | Meaning |
|------|--------|
| 400 | Validation failure |
| 404 | Task not found |
| 500 | Internal error |

## Troubleshooting
Ensure UI and API versions are compatible and that CORS settings allow browser requests.

---

See also: [INTEGRATIONS](INTEGRATIONS.md) · [GRAPHITI](GRAPHITI.md) · [UI_API_CONTRACT](UI_API_CONTRACT.md) · [DEPLOY_SINGLE_NODE](DEPLOY_SINGLE_NODE.md)

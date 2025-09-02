# UI API Contract

## TL;DR
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tasks` | GET | List running tasks |
| `/api/tasks` | POST | Create a new task |
| `/api/events` | SSE | Stream agent events for a task |

## Overview
This document defines the contract between Naestro's UI and core API service.

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

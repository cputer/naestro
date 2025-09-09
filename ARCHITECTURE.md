# NAESTRO Architecture

## Service Interactions

![High-level service interactions](docs/architecture.svg)

The source for this diagram is [docs/architecture.mmd](docs/architecture.mmd). To regenerate the
image from the Mermaid source, install the Mermaid CLI and run:

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i docs/architecture.mmd -o docs/architecture.svg
```

## Components

### Gateway

Handles inbound client requests, enforces authentication, and forwards messages into the system.

### Orchestrator

Coordinates workflows, routing tasks across components and aggregating results.

### Inference Tier

Executes model inference and retrieval steps required to satisfy requests.

### Monitoring

Collects metrics and traces across the stack for observability.

## Data Flow

### Retrieval-Augmented Generation (RAG)

1. The gateway receives a user query and passes it to the orchestrator.
2. The orchestrator retrieves relevant context from knowledge stores.
3. Retrieved context and query are sent to the inference tier for generation.
4. Responses are returned through the orchestrator back to the gateway and client.

### Workflow Execution

1. The gateway forwards workflow requests to the orchestrator.
2. The orchestrator schedules and executes steps across services.
3. Intermediate results are stored or routed as needed.
4. Final outputs are delivered to the client via the gateway.

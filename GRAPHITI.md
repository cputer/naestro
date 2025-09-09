Graphiti Integration Overview

Naestro now includes optional integration with Graphiti, a real-time, temporally-aware knowledge
graph engine designed to power AI orchestration with persistent memory.

What Graphiti Adds

1. Dynamic, Bi-Temporal Memory

Graphiti maintains a persistent knowledge graph of all orchestration events—proposals, critiques,
merges, verdicts—as “episodes.” Each episode is timestamped and can be queried by both its valid
time and ingestion time, enabling accurate historical context.

Store structured and unstructured data (JSON, plain text)

Track relationships and their evolution (e.g., supersedes, contradicts, depends_on)

2. Hybrid Retrieval for Context

Retrieve compact, high-relevance context using a mix of:

Semantic search (embeddings)

Keyword/BM25

Graph traversal (neighbor hops) This reduces prompt size while increasing accuracy and speed.

3. MCP — Model Context Protocol Server

Expose Graphiti via an MCP server, letting LLMs (Claude, Cursor, custom agents) access graph memory
as a tool with standard MCP semantics:

episodes.add, search.hybrid, context.assemble, edges.upsert, edges.invalidate

Works over REST or SSE for agentic workflows

4. Temporal Reasoning and Graph Intelligence

Edges and episodes carry valid_at / invalid_at timestamps, enabling:

Point-in-time queries (“what was true when X happened?”)

Automatic invalidation of stale or contradicted facts

Reliable audits of how a final decision emerged

5. Enterprise-Grade Performance

Graphiti scales horizontally and supports production graph backends (Neo4j, FalkorDB, Kùzu). It’s
built for low-latency, concurrent retrieval in multi-agent systems.

---

Why This Makes Naestro Substantially Better

Feature Benefit to Naestro

Persistent memory Maintains shared context across sessions, users, agents Efficient retrieval
Smaller prompts, faster I/O, higher answer quality Explainability Full audit trail of proposals →
critiques → verdicts Temporal logic Reason about what was true when; handle superseded facts
Scalability Handles many tasks/agents without context bloat

Net effect: Naestro shifts from a stateless prompt router to a collaborative AI OS with memory,
decisively outperforming static RAG setups.

---

Architecture (Mermaid)

flowchart LR subgraph User/Studio A[Naestro Studio (UI)] A1[Graph Panel] end

subgraph Core B[Naestro Core (Orchestrator API)] B1[Router: proposer/critic/synth/judge]
B2[Providers.yaml (model routing)] B3[@naestro/graphiti Client] end

subgraph Graphiti C[Graphiti REST/MCP] C1[Episodes Store] C2[Hybrid Search] C3[Bi-temporal Edges]
end

subgraph GraphDB D[(Neo4j/FalkorDB/Kùzu)] end

subgraph LLMs E1[Claude/Opus] E2[GPT-5 Pro] E3[Qwen 3.x] E4[Llama 3.1 70B] E5[Gemini 2.5 Pro]
E6[Local vLLM/TensorRT-LLM] end

A -->|Task prompt, review| B A1 -->|Query & visualize| C B -->|assembleContext()| C B3 --> C C
-->|subgraph + top episodes| B C1 --> D C2 --> D C3 --> D B1 -->|calls| E1 B1 -->|calls| E2 B1
-->|calls| E3 B1 -->|calls| E4 B1 -->|calls| E5 B1 -->|calls| E6 B -->|recordEpisode()| C

---

Getting Started (Local)

1. Deploy Graphiti locally (Docker or bare metal) with a graph backend (Neo4j/FalkorDB/Kùzu).

2. Set env in Naestro:

GRAPHITI_URL=<http://localhost:8899>

GRAPHITI_API_KEY=demo-key

GRAPHITI_SEMAPHORE_LIMIT=8 (tune 8–64)

3. Use the @naestro/graphiti client in Core to:

recordEpisode on each model turn (propose/critique/synthesize/judge)

fetchContextPack via context.assemble (compact, high-value context)

linkRelation to upsert graph edges (e.g., supersedes)

4. In Studio, add a Graph Panel to visualize entities, edges, and episode timelines.

5. Iterate routing policies using graph features (recency, agreement, authoritativeness).

---

Operational Tips

Security: For remote use, front Graphiti with HTTPS + API keys/OIDC; use network policies if in K8s.

Latency: Co-locate Core, Graphiti, and local LLMs on the same host/VPC.

Cost: Hybrid retrieval reduces token usage by ~20–40% and improves accuracy.

Concurrency: Increase GRAPHITI_SEMAPHORE_LIMIT as your provider limits allow.

Governance: Use temporal queries to audit decisions and detect regressions.

---

References

Graphiti GitHub: <https://github.com/getzep/graphiti>

Graphiti Quickstart: <https://help.getzep.com/graphiti/getting-started/welcome>

Neo4j Dev Blog (Graphiti & memory graphs):
<https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory>

Real-time Knowledge Graphs for Agents:
<https://medium.com/@sajidreshmi94/real-time-knowledge-graphs-for-ai-agents-using-graphiti-131df80e4063>

Building AI Agents with Graphiti:
<https://medium.com/@saeedhajebi/building-ai-agents-with-knowledge-graph-memory-a-comprehensive-guide-to-graphiti-3b77e6084dec>

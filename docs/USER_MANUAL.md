# User Manual

## Setup
1. Clone the repository and install Python dependencies:
   ```bash
   pip install -r requirements.lock
   pip install -r scripts/requirements.txt  # utilities such as governor.py
   ```
   Dependencies are pinned via `*.lock` files. If you change any
   `requirements.txt`, regenerate the lock with `pip-compile`.
2. Create a `.env` file based on the example:
   ```bash
   cp .env.example .env
   ```
3. Install required NLTK corpora:
   ```bash
   python -m nltk.downloader punkt averaged_perceptron_tagger
   ```
   **Offline installation:**
   ```bash
   python -m nltk.downloader --download-dir ./nltk_data punkt averaged_perceptron_tagger
   # transfer ./nltk_data to the target machine and set NLTK_DATA
   ```
   Then copy `nltk_data` to the offline host and set the `NLTK_DATA` environment variable to its path.
4. Launch core services with Docker:
   ```bash
   docker compose up -d --profile core
   ```
   Add the `inference` profile for GPU-backed models and `monitoring` for Prometheus/Grafana.

## Environment Configuration
Set the following variables in your `.env` file and load them before running services:

| Service | Variable | Description |
|---------|----------|-------------|
| Gateway | `ORCH_URL` | URL of the orchestrator (default `http://orchestrator:8081`). |
| Orchestrator | `SLM_BASE_URL`, `NIM_BASE_URL`, `VLLM_BASE_URL` | Model endpoints; at least one must be defined. |
| Both | `PG_DSN`, `REDIS_URL` | PostgreSQL DSN and Redis URI. |

Example:
```bash
echo 'ORCH_URL=http://localhost:8081' >> .env
echo 'SLM_BASE_URL=http://localhost:8000/v1' >> .env
source .env
echo $ORCH_URL  # expect: http://localhost:8081
```

**Troubleshooting**
- Missing variables lead to 400/500 errors during orchestration.
- If `echo $ORCH_URL` prints nothing, run `source .env` in the current shell.

## Services
- **Gateway (8080)** – external API endpoint.
- **Orchestrator (8081)** – workflow engine and routing logic.
- **Inference Tier** – optional NIM, vLLM, and small model services.
- **Monitoring Stack** – optional Prometheus + Grafana via the `monitoring` profile.

## End-to-End Orchestration Demo
1. Ensure gateway and orchestrator services are running (see `docker compose up` in Setup).
2. Submit a task through the gateway:
   ```bash
   curl -X POST http://localhost:8080/orchestrate \
        -H 'Content-Type: application/json' \
        -d '{"input": "Write a hello world function"}'
   ```
3. Expected output (truncated):
   ```json
   {
     "result": {
       "plan": "- Write a hello world function",
       "code": "def write_hello_world_function():...",
       "approved": true
     }
   }
   ```

**Troubleshooting**
- `Connection refused`: verify both services are up.
- `500` errors: ensure at least one model endpoint is configured via `SLM_BASE_URL`, `NIM_BASE_URL`, or `VLLM_BASE_URL`.

## Governor Script
`scripts/governor.py` adjusts EMA alpha based on Prometheus P95 latency.
Install its requirements and run:
```bash
pip install -r scripts/requirements.txt
python scripts/governor.py --prom-url http://localhost:9090
```

## User Interface
The React dashboard in `ui/` exposes workflow traces and a Monaco-based code editor for prompt and script editing.
Start it separately:
```bash
cd ui
npm install
npm start
```
The UI runs on `http://localhost:3000` and communicates with the gateway.

## Dataset Usage
- **PII Calibration Set** – `jobs/pii_calib_set.json` contains 550 labeled items. Run:
  ```bash
  python jobs/pii_calibrate.py
  ```
  to compute Shannon entropy flags for each item.

## RAG Ingestion Demo
1. Create tables and indexes:
   ```bash
   psql "$PG_DSN" -f sql/schema.sql
   ```
2. Insert a document and its chunk:
   ```bash
   psql "$PG_DSN" -c "INSERT INTO documents (source) VALUES ('demo') RETURNING id;"
   psql "$PG_DSN" -c "INSERT INTO chunks (doc_id, content, chunk_tsv) VALUES (1, 'hello world', to_tsvector('english','hello world'));"
   ```
3. Verify ingestion:
   ```bash
   psql "$PG_DSN" -c "SELECT COUNT(*) FROM chunks;"  # expect: 1
   ```

**Troubleshooting**
- `ERROR:  could not open extension control file "vector.control"`: install the pgvector extension.
- Connection issues: ensure `PG_DSN` matches your database host and credentials.

## Math & Science Demos
Example scripts illustrate SymPy and SciPy usage:
```bash
# Quadratic solver
python -m src.examples.sympy_demo 1 0 -4

# Integrate sin(x)
python -m src.examples.scipy_demo
```

# User Manual

## Setup
1. Clone the repository and install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file based on the example:
   ```bash
   cp .env.example .env
   ```
3. Launch core services with Docker:
   ```bash
   docker compose up -d --profile core
   ```
   Add the `inference` profile for GPU-backed models and `monitoring` for Prometheus/Grafana.

## Services
- **Gateway (8080)** – external API endpoint.
- **Orchestrator (8081)** – workflow engine and routing logic.
- **Inference Tier** – optional NIM, vLLM, and small model services.
- **Monitoring Stack** – optional Prometheus + Grafana via the `monitoring` profile.

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
- **RAG Data** – create tables using `sql/schema.sql` and ingest your documents into the `documents` and `chunks` tables.
- **PII Calibration Set** – `jobs/pii_calib_set.json` contains 550 labeled items. Run:
  ```bash
  python jobs/pii_calibrate.py
  ```
  to compute Shannon entropy flags for each item.

## Math & Science Demos
Example scripts illustrate SymPy and SciPy usage:
```bash
# Quadratic solver
python -m src.examples.sympy_demo 1 0 -4

# Integrate sin(x)
python -m src.examples.scipy_demo
```

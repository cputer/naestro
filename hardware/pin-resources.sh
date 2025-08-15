#!/bin/bash
# Pin processes to specific CPU cores and NUMA nodes
FASTAPI_CPUS=${1:-0-7}
POSTGRES_CPUS=${2:-8-15}
IRQ=${3:-96}
IRQ_MASK=${4:-2}

status=0

echo "Pinning FastAPI gateway processes (uvicorn) to CPUs ${FASTAPI_CPUS}"
uvicorn_pids=$(pgrep uvicorn)
if [ -n "$uvicorn_pids" ]; then
  echo "$uvicorn_pids" | xargs -n 1 -I{} taskset -cp "${FASTAPI_CPUS}" {}
else
  echo "No uvicorn processes found" >&2
  status=1
fi

echo "Pinning Postgres (pgvector) to CPUs ${POSTGRES_CPUS}"
postgres_pids=$(pgrep postgres)
if [ -n "$postgres_pids" ]; then
  echo "$postgres_pids" | xargs -n 1 -I{} taskset -cp "${POSTGRES_CPUS}" {}
else
  echo "No postgres processes found" >&2
  status=1
fi

# Example: Set NIC interrupt affinity (replace IRQ number as appropriate)
if [ -f /proc/irq/"$IRQ"/smp_affinity ]; then
  echo "Setting IRQ affinity for $IRQ"
  echo "$IRQ_MASK" > /proc/irq/"$IRQ"/smp_affinity
else
  echo "IRQ $IRQ not found" >&2
  status=1
fi

exit $status


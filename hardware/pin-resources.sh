#!/bin/bash
# Pin processes to specific CPU cores and NUMA nodes
echo "Pinning FastAPI gateway processes (uvicorn) to CPUs 0-7"
pgrep uvicorn | xargs -n 1 -I{} taskset -cp 0-7 {}
echo "Pinning Postgres (pgvector) to CPUs 8-15"
pgrep postgres | xargs -n 1 -I{} taskset -cp 8-15 {}

# Example: Set NIC interrupt affinity (replace IRQ number as appropriate)
IRQ=96
if [ -f /proc/irq/$IRQ/smp_affinity ]; then
  echo "Setting IRQ affinity for $IRQ"
  echo 2 > /proc/irq/$IRQ/smp_affinity
fi


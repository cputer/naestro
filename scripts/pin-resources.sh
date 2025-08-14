#!/usr/bin/env bash
# Example DGX CPU/GPU pinning & IO priority (adjust to your topology)
set -euo pipefail
# Pin gateway to NUMA0 CPUs 0-15, postgres to NUMA1 16-31 (example)
taskset -c 0-15 ionice -c2 -n0 bash -lc 'echo "start gateway here"'
taskset -c 16-31 ionice -c2 -n0 bash -lc 'echo "start postgres here"'
# MIG notes:
# - Assign MIG profiles ahead of time for SLM/NIM, then target device IDs in compose.

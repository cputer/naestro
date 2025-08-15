import time
from prometheus_client import Gauge

# Gauge for P95 latency (in seconds or ms as needed)
latency_gauge = Gauge("naestro_p95_latency", "P95 latency in seconds")

alpha_normal, alpha_burst = 0.19, 0.13

while True:
    # TODO: Replace input with real Prometheus metric fetch
    latency = float(input("Enter current p95 latency (sec): ") or 0.1)
    latency_gauge.set(latency)

    if latency > 0.05:
        print(f"Adjusting: Burst mode (higher throughput), alpha={alpha_burst}")
        # Here you would lower the EMA alpha for burst mode
    else:
        print(f"Adjusting: Normal mode, alpha={alpha_normal}")
        # Here you would set the EMA alpha to normal

    time.sleep(15)


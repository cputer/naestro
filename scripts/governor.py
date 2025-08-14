#!/usr/bin/env python3
"""Exponential moving average (EMA) governor for inference routing.
Adjusts small/large model routing weight based on recent p95 latency.
"""
import time
EMA_ALPHA = 0.2
TARGET_MS = 50.0

def ema(prev, new, alpha=EMA_ALPHA):
    return alpha*new + (1-alpha)*prev

def main():
    p95 = TARGET_MS
    weight_slm = 0.5
    while True:
        # In real deployment, read from Prometheus/metrics endpoint
        # Here, pretend-read from a file or stdin for simplicity
        try:
            sample = float(input("current p95 latency (ms): ") or TARGET_MS)
        except Exception:
            sample = TARGET_MS
        p95 = ema(p95, sample)
        if p95 > TARGET_MS:
            weight_slm = max(0.1, weight_slm - 0.05)
        else:
            weight_slm = min(0.95, weight_slm + 0.05)
        print(f"ema_p95={p95:.2f}ms, route_slm={weight_slm:.2f}, route_nim={1-weight_slm:.2f}")
        time.sleep(10)

if __name__ == "__main__":
    main()

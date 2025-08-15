import argparse
import os
import time
from typing import Optional

import requests
from prometheus_client import Gauge

# Gauge for P95 latency (in seconds or ms as needed)
latency_gauge = Gauge("naestro_p95_latency", "P95 latency in seconds")


def fetch_latency(prom_url: str, query: str) -> Optional[float]:
    """Fetch the P95 latency from Prometheus.

    Returns the latency as a float if available, otherwise ``None``.
    """

    try:
        response = requests.get(
            f"{prom_url}/api/v1/query", params={"query": query}, timeout=5
        )
        response.raise_for_status()
        payload = response.json()
        results = payload.get("data", {}).get("result", [])
        if results:
            return float(results[0]["value"][1])
    except Exception as exc:  # pragma: no cover - best effort logging only
        print(f"Error fetching latency: {exc}")
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Adjust EMA alpha based on P95 latency from Prometheus",
    )
    parser.add_argument(
        "--prom-url",
        default=os.environ.get("PROM_URL", "http://localhost:9090"),
        help="Base URL of the Prometheus server",
    )
    parser.add_argument(
        "--query",
        default=os.environ.get(
            "PROM_QUERY",
            "histogram_quantile(0.95, sum(rate(request_latency_seconds_bucket[5m])) by (le))",
        ),
        help="PromQL query used to retrieve the P95 latency",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=float(os.environ.get("LATENCY_THRESHOLD", "0.05")),
        help="Latency threshold (seconds) for burst mode",
    )
    parser.add_argument(
        "--normal-alpha",
        type=float,
        default=float(os.environ.get("ALPHA_NORMAL", "0.19")),
        help="EMA alpha used under normal conditions",
    )
    parser.add_argument(
        "--burst-alpha",
        type=float,
        default=float(os.environ.get("ALPHA_BURST", "0.13")),
        help="EMA alpha used when latency exceeds the threshold",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=float(os.environ.get("CHECK_INTERVAL", "15")),
        help="Interval between latency checks in seconds",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    while True:
        latency = fetch_latency(args.prom_url, args.query)
        if latency is not None:
            latency_gauge.set(latency)

            if latency > args.threshold:
                print(
                    f"Adjusting: Burst mode (higher throughput), alpha={args.burst_alpha}"
                )
                # Here you would lower the EMA alpha for burst mode
            else:
                print(f"Adjusting: Normal mode, alpha={args.normal_alpha}")
                # Here you would set the EMA alpha to normal
        else:
            print("Latency metric not available; skipping adjustment")

        time.sleep(args.interval)


if __name__ == "__main__":
    main()


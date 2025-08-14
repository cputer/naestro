#!/usr/bin/env python3
"""Simple PII entropy calibration placeholder.
Classifies text samples into high/low based on Shannon entropy thresholds.
"""
import math, json, sys

HIGH, LOW = 4.5, 2.5

def shannon_entropy(s: str) -> float:
    if not s: return 0.0
    from collections import Counter
    counts = Counter(s)
    total = len(s)
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

def main():
    data = json.load(sys.stdin) if not sys.stdin.isatty() else []
    out = []
    for item in data:
        ent = shannon_entropy(item.get("text",""))
        flag = "high" if ent > HIGH else ("low" if ent < LOW else "mid")
        out.append({**item, "entropy": ent, "flag": flag})
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()

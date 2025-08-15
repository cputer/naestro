from collections import Counter
import json
import math
from pathlib import Path


def calculate_shannon_entropy(text):
    counts = Counter(text)
    length = len(text)
    entropy = -sum((count / length) * math.log2(count / length) for count in counts.values())
    return entropy


with open(Path(__file__).with_name("pii_calib_set.json")) as f:
    data = json.load(f)

thresholds = {"high": 4.5, "low": 2.5}  # From spec

for item in data:
    entropy = calculate_shannon_entropy(item["text"])
    if entropy > thresholds["high"] and item["label"] == "key":
        item["flag"] = "high"
    if entropy < thresholds["low"] and item["label"] == "email":
        item["flag"] = "low"

print("Thresholds:", thresholds)


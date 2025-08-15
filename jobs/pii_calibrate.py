from collections import Counter
import math


def calculate_shannon_entropy(text):
    counts = Counter(text)
    length = len(text)
    entropy = -sum((count / length) * math.log2(count / length) for count in counts.values())
    return entropy


# Example calibration data (replace with actual dataset)
data = [
    {"text": "sample1", "label": "key"},
    {"text": "sample2", "label": "email"},
    # ... load actual calibration set here ...
]

thresholds = {"high": 4.5, "low": 2.5}  # From spec

for item in data:
    entropy = calculate_shannon_entropy(item["text"])
    if entropy > thresholds["high"] and item["label"] == "key":
        item["flag"] = "high"
    if entropy < thresholds["low"] and item["label"] == "email":
        item["flag"] = "low"

print("Thresholds:", thresholds)


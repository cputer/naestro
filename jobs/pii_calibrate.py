import json
import math
from collections import Counter
from pathlib import Path


def calculate_shannon_entropy(text):
    counts = Counter(text)
    length = len(text)
    entropy = -sum(
        (count / length) * math.log2(count / length) for count in counts.values()
    )
    return entropy


thresholds = {"high": 4.5, "low": 2.5}  # From spec
data = None


def main():
    global data
    with open(Path(__file__).with_name("pii_calib_set.json")) as f:
        data = json.load(f)

    for item in data:
        entropy = calculate_shannon_entropy(item["text"])
        if entropy > thresholds["high"] and item["label"] == "key":
            item["flag"] = "high"
        if entropy < thresholds["low"] and item["label"] == "email":
            item["flag"] = "low"

    print("Thresholds:", thresholds)


if __name__ == "__main__":
    main()

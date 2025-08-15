# PII Calibration Dataset

The file [`jobs/pii_calib_set.json`](../jobs/pii_calib_set.json) contains a synthetic
calibration set used for tuning PII detection heuristics.

## Generation

Entries were programmatically generated to cover three labels:

* `key` – secrets with relatively low entropy
* `email` – email-like tokens with higher entropy
* `none` – near misses that should not be identified as PII

Each record stores the text sample, its label, and a precalculated Shannon entropy.

## Validation

`jobs/pii_calibrate.py` recomputes entropy values and flags items whose entropy
falls outside the expected range. To ensure the dataset composition remains
stable, `tests/test_pii_calibrate.py` verifies the label distribution. The
current split is:

* 220 `key` samples (40%)
* 193 `email` samples (35%)
* 137 `none` samples (25%)

Run the following to validate the dataset:

```bash
pytest tests/test_pii_calibrate.py
```

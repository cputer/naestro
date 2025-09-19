# LLM Datasets Registry (mlabonne/llm-datasets)

The mlabonne/llm-datasets project curates a living index of post-training
corpora—covering supervised fine-tuning (SFT), reward modeling, agent/function
calling, and tooling to ingest or filter data. Naestro ships a **disabled**
registry wrapper so operators can document intent while ensuring no automated
job accesses external datasets without explicit governance approval.

## Configuration layout

- **File:** `configs/datasets/llm_datasets.yaml`
- **Default state:** `enabled: false`
- **Structure:**
  - `notes` — operator context that explains why the registry remains disabled.
  - `categories` — curated groupings (general-purpose SFT, math, code, agentic
    tooling, preference alignment) with representative datasets and license
    hints pulled from mlabonne/llm-datasets.
  - `usage.activation_steps` — manual checklist for refreshing the catalog,
    running ingestion, and registering artifacts inside Naestro.
  - `usage.plan_template` — reusable step list for generating a Naestro
    `Plan.json` once legal and data governance sign off.
  - `legal` — compliance, restriction, and contact notes that must remain
    satisfied before the switch can be flipped.

Because the registry is informational, **never** toggle `enabled: true` until
legal, privacy, and data governance stakeholders complete their reviews for
_every dataset_ you plan to ingest.

## Python helper

`integrations/datasets/llm_datasets_registry.py` exposes a lightweight helper to
inspect the configuration and draft plans without enabling automated access.

```python
from pathlib import Path

from integrations.datasets.llm_datasets_registry import (
    LLMDatasetsRegistry,
    load_registry,
)

# Load the disabled-by-default registry
registry = load_registry()
print("Registry enabled?", registry.enabled)
print("Available categories:", registry.list_categories())

# Draft a Plan.json stub for offline review
plan_stub = registry.create_plan("general_purpose")
export_path = Path("/tmp/llm-datasets-plan.json")
registry.export_plan("general_purpose", export_path)
```

`create_plan` and `export_plan` mirror the template stored in the YAML file and
always emit a `status: disabled` payload until the configuration is updated.
They are intentionally conservative: the helper will raise a `KeyError` for
unknown categories and never bootstrap network operations.

## Operational checklist

1. Review the upstream [mlabonne/llm-datasets README](https://github.com/mlabonne/llm-datasets)
   for the datasets you intend to ingest. Validate freshness, deduplication
   strategy, licensing, and any authorship constraints.
2. Route the request through Naestro's data governance workflow. Document the
   purpose of each dataset, approved storage locations, retention windows, and
   required evaluators/guardrails.
3. Only after sign-off, update `configs/datasets/llm_datasets.yaml` to set
   `enabled: true`, commit the decision record, and wire ingestion automations.
4. Monitor ingestion logs and evaluator runs. Pause the registry if quality,
   safety, or licensing concerns surface.

## Legal & compliance notice

- mlabonne/llm-datasets aggregates public links but does not grant license
  rights. You must confirm attribution, redistribution, and privacy obligations
  directly from each dataset card or upstream repository.
- Many corpora contain synthetic or user-generated data that can surface biases,
  disallowed content, or personally identifiable information. Apply Naestro's
  safety filters, anonymization tooling, and evaluator suites before deploying
  derived models.
- Keep legal and data governance contacts documented in the YAML file so future
  operators know who authorized access and where to escalate questions.

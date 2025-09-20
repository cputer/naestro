# Model Routing Matrix

Model routing mirrors the scoring sheet from the TradingAgents prompt. The goal
is to match incoming tasks with deterministic model bundles based on transparent
criteria such as latency, capability, or compliance requirements.

## Defining profiles

Profiles describe the characteristics of a request. Each profile combines tags,
constraints, and scoring weights:

```python
from naestro.routing import BaseTaskSpec, ModelInfo, ModelRouter

router = ModelRouter(
    models=[
        ModelInfo(name="gpt-mini", capability=["analysis"], latency_ms=350),
        ModelInfo(name="gpt-guard", capability=["analysis", "risk"], latency_ms=600),
        ModelInfo(name="gpt-fast", capability=["summary"], latency_ms=120),
    ]
)

profile: BaseTaskSpec = {
    "id": "trading-signal",
    "capability": ["analysis", "risk"],
    "max_latency_ms": 500,
    "weights": {
        "latency": 0.4,
        "capability": 0.6,
    },
}

selection = router.select(profile)
print(selection)
```

The result contains a ranked list of model names with their scores. The router
stays deterministic by using simple arithmetic rather than stochastic sampling.

## Scoring dimensions

- **Capability overlap.** Measures the intersection between the request and the
  model metadata.
- **Latency budget.** Filters models that exceed the allowed response time.
- **Cost or compliance.** Include additional metrics by extending `ModelInfo`
  and adjusting the scoring weights.

## Integrating with other components

- Emit routing results on the message bus via the `routing.evaluated` event.
- Feed the top candidate into a debate role or the
  [Trading Pack Walkthrough](../packs/trading.md).
- Log the selection alongside policy checks to build end-to-end audit trails.

## Adapting to new domains

Swap the metadata fields for equivalents in your environment—document review
speed, translation languages, or safety levels. Because the router is configured
with static data structures, you can snapshot inputs and outputs for regression
tests with ease.

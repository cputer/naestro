# Model Routing

The routing module keeps model metadata in a central registry and scores models
against routing requests.

```python
from naestro.routing import ModelProfile, ModelRegistry, Router, RoutingRequest

registry = ModelRegistry(
    [
        ModelProfile(
            name="small",
            provider="naestro",
            capabilities=frozenset({"chat", "analysis"}),
            quality=0.7,
            latency=0.2,
            cost=0.1,
        ),
        ModelProfile(
            name="coder",
            provider="partner",
            capabilities=frozenset({"code", "analysis"}),
            quality=0.85,
            latency=0.3,
            cost=0.25,
        ),
    ]
)

router = Router(registry)
request = RoutingRequest(
    task="code-review",
    required_capabilities=frozenset({"analysis", "code"}),
    weights={"quality": 0.6, "latency": 0.2, "cost": 0.2},
)
print(router.select_model(request).name)
```

The scoring function balances quality against latency and cost. Custom weights
let application teams fine tune selection without changing the registry.

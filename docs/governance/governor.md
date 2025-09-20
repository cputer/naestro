# Governor and Policies

Policies encode guard rails that must pass before a pipeline proposal is
executed. They are composed into a :class:`~naestro.governance.Governor`.

```python
from naestro.governance import Decision, Governor, Policy, PolicyInput

governor = Governor()


def min_return(payload: PolicyInput) -> Decision:
    score = payload.score or 0.0
    passed = score >= 0.3
    return Decision(
        name="min_return",
        passed=passed,
        reason="meets target" if passed else "return too small",
    )


def max_drawdown(payload: PolicyInput) -> Decision:
    drawdown = float(payload.metadata.get("max_drawdown", 0))
    passed = drawdown <= 2.0
    return Decision(
        name="max_drawdown",
        passed=passed,
        reason="protected" if passed else "drawdown exceeded",
    )


governor.register(Policy("return", "Ensure positive returns", min_return))
governor.register(Policy("drawdown", "Respect drawdown limit", max_drawdown))

policy_input = PolicyInput(subject="demo", score=0.4, metadata={"max_drawdown": 1.2})
allowed, results = governor.enforce(policy_input)
print(allowed)  # True
for result in results:
    print(result.name, result.passed)
```

Policies are pure callables, which keeps unit testing straightforward.

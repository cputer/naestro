# Governor and Policies

Policies encode guard rails that must pass before a pipeline proposal is
executed. They are composed into a :class:`~naestro.governance.Governor`.

```python
from naestro.governance import Decision, Governor, Policy, PolicyResult

governor = Governor()


def min_return(decision: Decision) -> PolicyResult:
    passed = decision.score >= 0.3
    return PolicyResult(
        name="min_return",
        passed=passed,
        reason="meets target" if passed else "return too small",
    )


def max_drawdown(decision: Decision) -> PolicyResult:
    drawdown = float(decision.metadata.get("max_drawdown", 0))
    passed = drawdown <= 2.0
    return PolicyResult(
        name="max_drawdown",
        passed=passed,
        reason="protected" if passed else "drawdown exceeded",
    )


governor.register(Policy("return", "Ensure positive returns", min_return))
governor.register(Policy("drawdown", "Respect drawdown limit", max_drawdown))

allowed, results = governor.enforce(
    Decision(subject="demo", score=0.4, metadata={"max_drawdown": 1.2})
)
print(allowed)  # True
for result in results:
    print(result.name, result.passed)
```

Policies are pure callables, which keeps unit testing straightforward.

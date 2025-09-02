# Example Scripts

This repository includes small demonstrations of third-party libraries.

## Setup
Install dependencies with pinned versions and run examples from the repository root:

```bash
pip install -r requirements.lock
```


## SymPy Quadratic Solver

Solve quadratic equations of the form `a*x**2 + b*x + c = 0`.

```bash
python -m src.examples.sympy_demo 1 0 -4
```

## SciPy Sine Integration

Integrate `sin(x)` from `a` to `b` (defaults 0 to π):

```bash
python -m src.examples.scipy_demo
```

## Troubleshooting
- Run examples with `python -m` to ensure module imports resolve correctly.
- If `ModuleNotFoundError` occurs, reinstall the pinned requirements.

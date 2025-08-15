# Example Scripts

This repository includes small demonstrations of third-party libraries.

Install dependencies with:

```bash
pip install -r requirements.txt
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

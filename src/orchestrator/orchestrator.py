import collections
import math
import os
import subprocess
import tempfile

import nltk
from langgraph import Graph

_NLTK_READY = False


def ensure_nltk_data() -> None:
    """Ensure required NLTK corpora are available."""

    global _NLTK_READY
    if _NLTK_READY:
        return

    packages = {
        "punkt": "tokenizers/punkt",
        "averaged_perceptron_tagger": "taggers/averaged_perceptron_tagger",
    }
    missing = []
    for pkg, path in packages.items():
        try:
            nltk.data.find(path)
        except LookupError:
            missing.append(pkg)

    if missing:
        for pkg in missing:
            nltk.download(pkg, quiet=True)

        unresolved = []
        for pkg, path in packages.items():
            try:
                nltk.data.find(path)
            except LookupError:
                unresolved.append(pkg)

        if unresolved:
            raise LookupError("Missing NLTK corpora: " + ", ".join(sorted(unresolved)))

    _NLTK_READY = True


def _build_plan(text: str) -> str:
    """Create a simple bullet-point plan using sentence tokenization."""
    try:
        ensure_nltk_data()
        sentences = nltk.sent_tokenize(text) if text else []
    except LookupError as exc:
        raise RuntimeError(
            "Required NLTK corpora not available; install 'punkt' and 'averaged_perceptron_tagger'."
        ) from exc
    return "\n".join(f"- {s.strip()}" for s in sentences)


# Task functions
def planner_fn(state):
    """Break down the input into a plan using an NLP tool."""
    text = state.get("input", "")
    plan = _build_plan(text)
    return {"plan": plan, "context_size": len(text)}


def implement_fn(state):
    """Generate pseudocode from the plan using tokenization."""
    plan = state.get("plan", "")
    steps = [line[2:].strip() for line in plan.splitlines() if line.startswith("- ")]
    code_lines = []
    for idx, step in enumerate(steps, 1):
        tokens = [t for t in nltk.word_tokenize(step) if t.isidentifier()]
        func_name = "_".join(tokens[:2]) or f"step_{idx}"
        code_lines.append(f'def {func_name}():\n    """{step}"""\n    pass\n')
    code = "\n".join(code_lines)
    return {"code": code}


def _shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    freq = collections.Counter(text)
    total = len(text)
    entropy = -sum(
        (count / total) * math.log2(count / total) for count in freq.values()
    )
    max_entropy = math.log2(len(freq))
    return entropy / max_entropy if max_entropy else 0.0


def verify_fn(state):
    """Run basic checks: compilation, linting, and entropy."""
    code = state.get("code", "")
    path = None
    try:
        with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp.flush()
            path = tmp.name

        try:
            import py_compile

            py_compile.compile(path, doraise=True)
            passed = True
        except Exception:
            passed = False

        try:
            result = subprocess.run(["flake8", path], capture_output=True, text=True)
            lint_errors = [
                line for line in result.stdout.splitlines() if line.strip()
            ]
            lint_delta = 1 / (1 + len(lint_errors))
        except FileNotFoundError:
            lint_delta = 0.0

        entropy_delta = _shannon_entropy(code)
        return {
            "passed": passed,
            "passed_delta": 1.0 if passed else 0.0,
            "lint_delta": lint_delta,
            "entropy_delta": entropy_delta,
        }
    finally:
        if path and os.path.exists(path):
            os.unlink(path)


def refine_fn(state):
    """Format code using Black to improve readability."""
    code = state.get("code", "")
    path = None
    try:
        with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp.flush()
            path = tmp.name

        try:
            subprocess.run(["black", "-q", path], check=False)
            with open(path, "r", encoding="utf-8") as fh:
                improved = fh.read()
        except FileNotFoundError:
            improved = code

        return {"code": improved}
    finally:
        if path and os.path.exists(path):
            os.unlink(path)


def human_review_fn(state):
    """Approve plans containing at least one verb."""
    plan = state.get("plan", "")
    try:
        ensure_nltk_data()
        tokens = nltk.word_tokenize(plan) if plan else []
        tags = nltk.pos_tag(tokens) if tokens else []
    except LookupError as exc:
        raise RuntimeError(
            "Required NLTK corpora not available; install 'punkt' and 'averaged_perceptron_tagger'."
        ) from exc
    approved = any(tag.startswith("VB") for _, tag in tags)
    return {"approved": approved}


# Conditions
def approve_cond(state):
    return state.get("approved", False)


def refine_gate(state):
    """Deterministic gate for refining based on combined metrics."""
    score = (
        0.05 * state.get("passed_delta", 0)
        + 0.65 * state.get("lint_delta", 0)
        + 0.30 * state.get("entropy_delta", 0)
    )
    return (score < 0.8) and (state.get("budget", 1.0) > 0.5)


# Construct the state machine graph
graph = Graph()
graph.add_node("planner", planner_fn)
graph.add_node("implement", implement_fn)
graph.add_node("verify", verify_fn)
graph.add_node("refine", refine_fn)
graph.add_node("human_review", human_review_fn)

graph.add_edge("planner", "human_review")  # initial review step
graph.add_conditional_edge("human_review", "implement", condition=approve_cond)
graph.add_edge("implement", "verify")
graph.add_conditional_edge("verify", "refine", condition=refine_gate)
graph.add_edge("refine", "verify")  # loop back to verify after refining

# Compile the workflow for execution
app = graph.compile()

from langgraph import Graph
from random import random


# Task functions
def planner_fn(state):
    # Break down the input into subtasks or plan
    plan = "generated_plan"
    return {"plan": plan, "context_size": len(state.get("input", ""))}


def implement_fn(state):
    # Generate code or solution from the plan
    code = "generated_code"
    return {"code": code}


def verify_fn(state):
    # Check code correctness (e.g., run tests, static analysis)
    passed = True  # placeholder
    delta = 0.3  # difference metric (e.g. performance diff)
    return {"passed": passed, "passed_delta": delta, "lint_delta": 0.1, "entropy_delta": 0.2}


def refine_fn(state):
    # Refine the output if needed
    improved = "refined_code"
    return {"improved": improved}


def human_review_fn(state):
    # Human-in-the-loop review (simulate approval)
    approved = True
    return {"approved": approved}


# Conditions
def approve_cond(state):
    return state.get("plan") is not None


def pass_cond(state):
    return state.get("passed", False)


def refine_gate(state):
    # Probabilistic gate for refining based on combined metrics
    score = (
        0.05 * state.get("passed_delta", 0)
        + 0.65 * state.get("lint_delta", 0)
        + 0.30 * state.get("entropy_delta", 0)
    )
    return (random() < score) and (state.get("budget", 1.0) > 0.5)


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
graph.add_conditional_edge("verify", "refine", condition=pass_cond)
graph.add_edge("refine", "verify")  # loop back to verify after refining

# Compile the workflow for execution
app = graph.compile()


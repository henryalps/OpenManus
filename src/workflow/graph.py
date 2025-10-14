from langgraph.graph import StateGraph, START
from src.graph.types import State # Import State class
from src.agents.nodes import ( # Import agent nodes
    coordinator_node,
    planner_node,
    supervisor_node,
    researcher_node,
    coder_node,
    browser_node,
    reporter_node,
)

def build_graph():
    """Build and return the agent workflow graph."""
    builder = StateGraph(State)

    # Define nodes
    builder.add_node("coordinator", coordinator_node)
    builder.add_node("planner", planner_node)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("researcher", researcher_node)
    builder.add_node("coder", coder_node)
    builder.add_node("browser", browser_node)
    builder.add_node("reporter", reporter_node)

    # Set entry point
    builder.add_edge(START, "coordinator")

    return builder.compile()
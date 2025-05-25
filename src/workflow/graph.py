from langgraph.graph import StateGraph, START
from src.graph.types import State  # Import State class
from src.agents.nodes import (  # Import agent nodes
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

    # Define edges
    builder.add_edge(START, "coordinator")
    builder.add_edge("coordinator", "planner")  # Coordinator -> Planner
    builder.add_edge("planner", "supervisor")  # Planner -> Supervisor
    # Edges from supervisor are handled by set_conditional_edge
    # builder.add_edge("supervisor", "researcher") # No condition needed here
    # builder.add_edge("supervisor", "coder")
    # builder.add_edge("supervisor", "browser")
    # builder.add_edge("supervisor", "reporter")
    # builder.add_edge("supervisor", "__end__")
    builder.add_edge("researcher", "supervisor")  # Researcher -> Supervisor
    builder.add_edge("coder", "supervisor")  # Coder -> Supervisor
    builder.add_edge("browser", "supervisor")  # Browser -> Supervisor
    builder.add_edge("reporter", "supervisor")  # Reporter -> Supervisor

    builder.set_entry_point("coordinator")

    # Define a mapping for conditional edges from the supervisor
    # The supervisor_node itself should return the name of the next node (or __end__)
    # based on its internal logic.
    conditional_map = {
        "researcher": "researcher",
        "coder": "coder",
        "browser": "browser",
        "reporter": "reporter",
        "FINISH": "__end__", # Ensure supervisor_node returns "FINISH" for __end__
        "__end__": "__end__" # Explicitly handle __end__ if supervisor_node returns it
    }

    def select_next_node(state: State):
        # The supervisor_node updates state['next'] with the name of the next node
        # or "FINISH"
        if state.get("next"):
            return state["next"]
        return "__end__" # Default or error case

    builder.add_conditional_edges(
        "supervisor",
        select_next_node,
        conditional_map
    )
    # builder.set_conditional_edge("supervisor", supervisor_node) # Old way
    # No need to explicitly add END node, it's a reserved keyword for conditional edges
    # builder.add_end_point("__end__") # This is also an option if needed

    return builder.compile()

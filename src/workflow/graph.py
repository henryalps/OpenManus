from langgraph.graph import StateGraph, START, END
from src.graph.types import State # Import State class
from src.agents.nodes.coordinator_node import coordinator_node
from src.agents.nodes.planner_node import planner_node
from src.agents.nodes.supervisor_node import supervisor_node
from src.agents.nodes.researcher_node import researcher_node
from src.agents.nodes.coder_node import coder_node
from src.agents.nodes.browser_node import browser_node
from src.agents.nodes.reporter_node import reporter_node
from src.agents.nodes.react_agent_node import react_agent_node

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
    builder.add_node("react_agent", react_agent_node)

    # Define edges
    builder.add_edge(START, "coordinator")
    builder.add_edge("coordinator", "planner") # Coordinator -> Planner
    builder.add_edge("planner", "supervisor") # Planner -> Supervisor

    # Add conditional edges from supervisor to other agents
    builder.add_conditional_edges(
        "supervisor",
        lambda state: state.get("next", END),
        {
            "researcher": "researcher",
            "coder": "coder",
            "browser": "browser",
            "reporter": "reporter",
            "react_agent": "react_agent",
            "FINISH": END,
        },
    )

    builder.add_edge("researcher", "supervisor") # Researcher -> Supervisor
    builder.add_edge("coder", "supervisor") # Coder -> Supervisor
    builder.add_edge("browser", "supervisor") # Browser -> Supervisor
    builder.add_edge("reporter", "supervisor") # Reporter -> Supervisor
    builder.add_edge("react_agent", "supervisor") # ReAct Agent -> Supervisor

    builder.set_entry_point("coordinator")

    return builder.compile()
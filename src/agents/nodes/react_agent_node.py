import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.agents.react_agent import react_agent
from .types import State

logger = logging.getLogger(__name__)

def react_agent_node(state: State) -> Dict[str, Any]:
    """Node for the ReAct agent."""
    logger.info("ReAct agent starting task")
    result = react_agent.invoke(state["messages"])
    logger.info("ReAct agent completed task")

    # The result from the ReAct agent could be a tool call or a final answer.
    # For now, we'll just add it to the messages and go back to the supervisor.
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=result.content,
                    name="react_agent",
                )
            ]
        },
        goto="supervisor",
    )

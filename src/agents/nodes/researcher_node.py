import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.agents import research_agent  # Import researcher agent
from src.utils.json_utils import repair_json_output
from .types import State  # Import State type

logger = logging.getLogger(__name__)


def researcher_node(state: State) -> Dict[str, Any]:  # Modified return type to Dict
    """Node for the researcher agent that performs research tasks."""
    logger.info("Research agent starting task")
    result = research_agent.invoke(state)
    logger.info("Research agent completed task")
    response_content = result["messages"][-1].content
    response_content = repair_json_output(response_content)
    logger.debug(f"Research agent response: {response_content}")
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response_content,
                    name="researcher",
                )
            ]
        },
        goto="supervisor",
    )

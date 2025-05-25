import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.agents import browser_agent  # Import browser agent
from src.utils.json_utils import repair_json_output
from .types import State  # Import State type

logger = logging.getLogger(__name__)


def browser_node(state: State) -> Dict[str, Any]:  # Modified return type to Dict
    """Node for the browser agent that performs web browsing tasks."""
    logger.info("Browser agent starting task")
    result = browser_agent.invoke(state)
    logger.info("Browser agent completed task")
    response_content = result["messages"][-1].content
    response_content = repair_json_output(response_content)
    logger.debug(f"Browser agent response: {response_content}")
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response_content,
                    name="browser",
                )
            ]
        },
        goto="supervisor",
    )

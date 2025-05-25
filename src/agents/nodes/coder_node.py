import logging
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.agents import coder_agent  # Import coder agent
from src.utils.json_utils import repair_json_output
from .types import State  # Import State type

logger = logging.getLogger(__name__)


def coder_node(state: State) -> Dict[str, Any]:  # Modified return type to Dict
    """Node for the coder agent that executes Python code."""
    logger.info("Code agent starting task")
    result = coder_agent.invoke(state)
    logger.info("Code agent completed task")
    response_content = result["messages"][-1].content
    response_content = repair_json_output(response_content)
    logger.debug(f"Code agent response: {response_content}")
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response_content,
                    name="coder",
                )
            ]
        },
        goto="supervisor",
    )

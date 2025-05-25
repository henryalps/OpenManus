import logging
from typing import Dict, Any
from langgraph.types import Command

from src.llms.llm import get_llm_by_type
from src.config.agents import AGENT_LLM_MAP
from src.prompts.template import IntelliAgentPromptTemplate
from src.utils.json_utils import repair_json_output
from .types import State  # Import State and Router types

logger = logging.getLogger(__name__)


def coordinator_node(state: State) -> Dict[str, Any]:  # Modified return type to Dict
    """Coordinator node that communicate with customers."""
    logger.info("Coordinator talking.")
    messages = IntelliAgentPromptTemplate.apply_prompt_template("coordinator", state)
    llm = get_llm_by_type(AGENT_LLM_MAP["coordinator"])
    response = llm.invoke(messages)
    logger.debug(f"Current state messages: {state['messages']}")
    response_content = response.content
    # Attempt to repair potential JSON output
    response_content = repair_json_output(response_content)
    logger.debug(f"Coordinator response: {response_content}")

    goto = "__end__"
    if "handoff_to_planner" in response_content:
        goto = "planner"

    # Update response.content with repaired content
    response.content = response_content

    return Command(
        goto=goto,
    )

import logging
import json_repair
from typing import Literal, Dict, Any
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.llms.llm import get_llm_by_type
from src.config.agents import AGENT_LLM_MAP
from src.prompts.template import OpenManusPromptTemplate
from src.utils.json_utils import repair_json_output
from .types import State, Router # Import State and Router types

logger = logging.getLogger(__name__)

def coordinator_node(state: State) -> Dict[str, Any]: # Modified return type to Dict
    """Coordinator node that communicate with customers."""
    logger.info("Coordinator talking.")
    messages = OpenManusPromptTemplate.apply_prompt_template("coordinator", state)
    response = get_llm_by_type(AGENT_LLM_MAP["coordinator"]).invoke(messages)
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
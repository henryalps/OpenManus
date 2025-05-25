import logging
from copy import deepcopy
from typing import Dict, Any

from langchain_core.messages import BaseMessage
from langgraph.types import Command

from src.llms.llm import get_llm_by_type
from src.config import TEAM_MEMBERS
from src.config.agents import AGENT_LLM_MAP
from src.prompts.template import IntelliAgentPromptTemplate
from .types import State, Router  # Import State and Router types

logger = logging.getLogger(__name__)

RESPONSE_FORMAT = (
    "Response from {}:\n\n<response>\n{}\n</response>\n\n"
    "*Please execute the next step.*"
)


def supervisor_node(state: State) -> Dict[str, Any]:  # Modified return type to Dict
    """Supervisor node that decides which agent should act next."""
    logger.info("Supervisor evaluating next action")
    messages = IntelliAgentPromptTemplate.apply_prompt_template("supervisor", state)
    # preprocess messages to make supervisor execute better.
    messages = deepcopy(messages)
    for message in messages:
        if isinstance(message, BaseMessage) and message.name in TEAM_MEMBERS:
            message.content = RESPONSE_FORMAT.format(message.name, message.content)
    response = (
        get_llm_by_type(AGENT_LLM_MAP["supervisor"])
        .with_structured_output(schema=Router, method="json_mode")
        .invoke(messages)
    )
    goto = response["next"]
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"Supervisor response: {response}")

    if goto == "FINISH":
        goto = "__end__"
        logger.info("Workflow completed")
    else:
        logger.info(f"Supervisor delegating to: {goto}")

    return Command(goto=goto, update={"next": goto})

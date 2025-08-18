import logging
import json_repair
import re
from copy import deepcopy
from typing import Literal, Dict, Any

from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.graph import END
from langgraph.types import Command

from src.llms.llm import get_llm_by_type
from src.config import TEAM_MEMBERS
from src.config.agents import AGENT_LLM_MAP
from src.prompts.template import OpenManusPromptTemplate
from src.utils.json_utils import repair_json_output
from src.tools.tool_registry import get_tool
from .types import State, Router # Import State and Router types

logger = logging.getLogger(__name__)

RESPONSE_FORMAT = "Response from {}:\n\n<response>\n{}\n</response>\n\n*Please execute the next step.*"

def supervisor_node(state: State) -> Dict[str, Any]: # Modified return type to Dict
    """Supervisor node that decides which agent should act next."""
    logger.info("Supervisor evaluating next action")
    messages = OpenManusPromptTemplate.apply_prompt_template("supervisor", state)
    # preprocess messages to make supervisor execute better.
    messages = deepcopy(messages)
    for message in messages:
        if isinstance(message, BaseMessage) and message.name in TEAM_MEMBERS:
            message.content = RESPONSE_FORMAT.format(message.name, message.content)
    response = get_llm_by_type(AGENT_LLM_MAP["supervisor"]).invoke(messages)

    try:
        response_data = json_repair.loads(response.content)
    except Exception as e:
        # If parsing fails, try to extract JSON from the response
        json_match = re.search(r"\{.*\}", response.content, re.DOTALL)
        if json_match:
            try:
                response_data = json_repair.loads(json_match.group(0))
            except Exception as e:
                # If we still can't parse it, we have to give up
                return Command(goto=END)
        else:
            return Command(goto=END)

    # Check for tool calls
    if isinstance(response_data, dict) and "tool_call" in response_data and response_data["tool_call"]:
        tool_name = response_data["tool_call"]["name"]
        tool_args = response_data["tool_call"]["args"]
        tool = get_tool(tool_name)
        if tool:
            result = tool.invoke(tool_args)
            return Command(
                update={
                    "messages": [
                        HumanMessage(
                            content=result,
                            name="tool_executor",
                        )
                    ]
                },
                goto=state["next"],
            )
        else:
            return Command(
                update={
                    "messages": [
                        HumanMessage(
                            content=f"Tool '{tool_name}' not found.",
                            name="tool_executor",
                        )
                    ]
                },
                goto=END,
            )

    if isinstance(response_data, dict):
        goto = response_data.get("next", "FINISH")
    else:
        goto = "FINISH"

    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"Supervisor response: {response}")

    if goto == "FINISH":
        return Command(goto="FINISH")
    else:
        logger.info(f"Supervisor delegating to: {goto}")
        return Command(goto=goto, update={"next": goto})
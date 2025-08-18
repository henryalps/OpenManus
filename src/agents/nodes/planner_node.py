import logging
import json
import json_repair
from copy import deepcopy
from typing import Literal, Dict, Any
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.llms.llm import get_llm_by_type
from src.config.agents import AGENT_LLM_MAP
from src.prompts.template import OpenManusPromptTemplate
from src.tools.search import bing_tool
from src.utils.json_utils import repair_json_output
from .types import State # Import State type

logger = logging.getLogger(__name__)

def planner_node(state: State) -> Dict[str, Any]: # Modified return type to Dict
    """Planner node that generate the full plan."""
    logger.info("Planner generating full plan")
    messages = OpenManusPromptTemplate.apply_prompt_template("planner", state)
    # whether to enable deep thinking mode
    llm = get_llm_by_type(AGENT_LLM_MAP["planner"]) # Changed to planner LLM
    if state.get("deep_thinking_mode"):
        llm = get_llm_by_type("reasoning")
    if state.get("search_before_planning"):
        searched_content = bing_tool.invoke({"query": state["messages"][-1].content})
        messages = deepcopy(messages)
        messages[
            -1
        ].content += "\\n\\n# Relative Search Results\\n\\n" + json.dumps([{'title': elem['title'], 'content': elem['content']} for elem in searched_content], ensure_ascii=False)
    stream = llm.stream(messages)
    full_response = ""
    for chunk in stream:
        full_response += chunk.content
    logger.debug(f"Current state messages: {state['messages']}")
    logger.debug(f"Planner response: {full_response}")

    if full_response.startswith("```json"):
        full_response = full_response.removeprefix("```json")

    if full_response.endswith("```"):
        full_response = full_response.removesuffix("```")

    goto = "supervisor"
    try:
        repaired_response = json_repair.loads(full_response)
        full_response = json.dumps(repaired_response)
    except json.JSONDecodeError:
        logger.warning("Planner response is not a valid JSON")
        goto = "__end__"

    return Command(
        update={
            "messages": [HumanMessage(content=full_response, name="planner")],
            "full_plan": full_response,
        },
        goto=goto,
    )
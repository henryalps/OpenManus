import logging
import json_repair
from typing import Literal, Dict, Any
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.agents import reporter_agent # Import reporter agent
from src.utils.json_utils import repair_json_output
from src.prompts.template import OpenManusPromptTemplate
from src.tools.tts import text_to_speech
from .types import State # Import State type

logger = logging.getLogger(__name__)

def reporter_node(state: State) -> Dict[str, Any]: # Modified return type to Dict
    """Reporter node that write a final report."""
    logger.info("Reporter writing final report")
    messages = OpenManusPromptTemplate.apply_prompt_template("reporter", state)
    response = reporter_agent.invoke(state)
    logger.debug(f"Current state messages: {state['messages']}")
    response_content = response.content
    response_content = repair_json_output(response_content)
    logger.debug(f"Reporter agent response: {response_content}")

    # Generate audio from the report
    try:
        tts_message = text_to_speech(response_content, "output/report.wav")
        logger.info(tts_message)
    except Exception as e:
        logger.error(f"Error generating TTS: {e}")

    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response_content,
                    name="reporter",
                )
            ]
        },
        goto="supervisor", # Go back to supervisor to decide next step
    )
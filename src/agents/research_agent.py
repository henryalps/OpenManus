from typing import List
from langchain_core.messages import BaseMessage

from src.llms.llm import get_llm_by_type
from src.config.agents import AGENT_LLM_MAP


class ResearchAgent:
    """Research agent that handles research and information gathering tasks."""

    def invoke(self, messages: List[BaseMessage]) -> BaseMessage:
        """Process the messages and return a response."""
        llm = get_llm_by_type(AGENT_LLM_MAP["researcher"])
        return llm.invoke(messages)


research_agent = ResearchAgent()

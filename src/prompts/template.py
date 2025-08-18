import os
import re
from datetime import datetime
from typing import Dict, List

from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt.chat_agent_executor import AgentState

from .prompt_registry import register_prompt, get_prompt
from src.config import TEAM_MEMBERS

def load_and_register_prompts():
    """Load all prompts from markdown files and register them in the prompt registry."""
    prompt_dir = os.path.dirname(__file__)
    for filename in os.listdir(prompt_dir):
        if filename.endswith(".md"):
            prompt_name = filename[:-3]
            template_path = os.path.join(prompt_dir, filename)
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            register_prompt(prompt_name, template)

load_and_register_prompts()

class OpenManusPromptTemplate:
    """OpenManus prompt template manager for handling agent-specific prompts."""

    @staticmethod
    def get_prompt_template(prompt_name: str) -> str:
        """Load and process a prompt template from the registry.

        Args:
            prompt_name: Name of the prompt template

        Returns:
            Processed template string with variable placeholders
        """
        template = get_prompt(prompt_name)
        if not template:
            raise ValueError(f"Prompt template '{prompt_name}' not found.")

        # Escape curly braces for string formatting
        template = template.replace("{", "{{").replace("}", "}}")
        # Convert <<VAR>> to {VAR} format
        template = re.sub(r"<<([^>>]+)>>", r"{\1}", template)
        return template

    @staticmethod
    def apply_prompt_template(prompt_name: str, state: AgentState) -> List[Dict[str, str]]:
        """Apply a prompt template with current state variables.

        Args:
            prompt_name: Name of the prompt template to apply
            state: Current agent state containing variables and messages

        Returns:
            List of message dictionaries with system prompt and state messages
        """
        # Format current time in a consistent format
        current_time = datetime.now().strftime("%a %b %d %Y %H:%M:%S %z")

        # Create and format the system prompt
        system_prompt = PromptTemplate(
            input_variables=["CURRENT_TIME", "TEAM_MEMBERS"],
            template=OpenManusPromptTemplate.get_prompt_template(prompt_name),
        ).format(CURRENT_TIME=current_time, TEAM_MEMBERS=", ".join(TEAM_MEMBERS), **state)

        # Combine system prompt with existing messages
        return [{"role": "system", "content": system_prompt}] + state["messages"]
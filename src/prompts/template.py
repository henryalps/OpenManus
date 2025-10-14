import os
import re
from datetime import datetime
from typing import Dict, List

from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt.chat_agent_executor import AgentState


class OpenManusPromptTemplate:
    """OpenManus prompt template manager for handling agent-specific prompts."""

    @staticmethod
    def get_prompt_template(prompt_name: str) -> str:
        """Load and process a prompt template from file.

        Args:
            prompt_name: Name of the prompt template file (without .md extension)

        Returns:
            Processed template string with variable placeholders
        """
        template_path = os.path.join(os.path.dirname(__file__), f"{prompt_name}.md")
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

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
        from src.config import TEAM_MEMBERS

        # Format current time in a consistent format
        current_time = datetime.now().strftime("%a %b %d %Y %H:%M:%S %z")

        # Get the template
        template_str = OpenManusPromptTemplate.get_prompt_template(prompt_name)

        # Build template variables
        template_vars = {
            "CURRENT_TIME": current_time,
            "TEAM_MEMBERS": str(TEAM_MEMBERS),
        }

        # Add state variables
        template_vars.update(state)

        # Determine which variables are actually in the template
        import re
        found_vars = re.findall(r'\{([^}]+)\}', template_str)
        input_variables = list(set(found_vars))

        # Create and format the system prompt
        system_prompt = PromptTemplate(
            input_variables=input_variables,
            template=template_str,
        ).format(**template_vars)

        # Combine system prompt with existing messages
        return [{"role": "system", "content": system_prompt}] + state["messages"]
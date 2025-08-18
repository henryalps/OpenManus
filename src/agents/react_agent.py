import re
from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from src.llms.llm import get_llm_by_type
from src.tools.tool_registry import get_all_tools
from src.prompts.template import OpenManusPromptTemplate

class ReActAgent:
    """A ReAct-style agent that can reason and act."""

    def __init__(self):
        self.llm = get_llm_by_type("reasoning")
        self.tools = {name: tool.invoke for name, tool in get_all_tools().items()}

    def invoke(self, messages: List[BaseMessage]) -> BaseMessage:
        """Process the messages and return a response."""

        # Get the ReAct prompt
        prompt_template = OpenManusPromptTemplate.get_prompt_template("react")

        # Add the tools to the prompt
        tool_descriptions = "\n".join([f"- {name}: {tool.__doc__}" for name, tool in self.tools.items()])
        prompt = prompt_template.replace("<<tools>>", tool_descriptions)

        # Add the messages to the prompt
        conversation_history = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])
        prompt = prompt.replace("<<messages>>", conversation_history)

        # ReAct loop
        for _ in range(5):  # Limit the number of iterations to prevent infinite loops
            response = self.llm.invoke(prompt)

            # Parse the response
            thought_match = re.search(r"Thought:\n(.*?)\n\nAction:", response.content, re.DOTALL)
            action_match = re.search(r"Action:\n(.*?)$", response.content, re.DOTALL)
            final_answer_match = re.search(r"Final Answer:\n(.*?)$", response.content, re.DOTALL)

            if final_answer_match:
                return AIMessage(content=final_answer_match.group(1).strip())

            if thought_match and action_match:
                thought = thought_match.group(1).strip()
                action_str = action_match.group(1).strip()

                try:
                    action_data = json.loads(action_str)
                    tool_name = action_data["tool"]
                    tool_args = action_data["args"]

                    if tool_name in self.tools:
                        observation = self.tools[tool_name](tool_args)
                        prompt += f"\n\nObservation:\n{observation}"
                    else:
                        prompt += f"\n\nObservation:\nTool '{tool_name}' not found."
                except Exception as e:
                    prompt += f"\n\nObservation:\nError parsing action: {e}"
            else:
                # If the response is not in the correct format, treat it as a final answer
                return AIMessage(content=response.content)

        return AIMessage(content="I'm sorry, I was unable to answer the question.")

react_agent = ReActAgent()

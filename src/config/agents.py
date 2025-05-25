from typing import Literal

# Define available LLM types
LLMType = Literal["basic", "reasoning", "vision"]

# Define agent-LLM mapping
AGENT_LLM_MAP: dict[str, LLMType] = {
    "coordinator": "basic",  # Coordinator defaults to using basic llm
    "planner": "reasoning",  # Planner defaults to using basic llm
    "supervisor": "basic",  # Decision-making uses basic llm
    "researcher": "basic",  # Simple search tasks use basic llm
    "coder": "basic",  # Programming tasks use basic llm
    "browser": "vision",  # Browser operations use vision llm
    "reporter": "basic",  # Writing reports uses basic llm
}

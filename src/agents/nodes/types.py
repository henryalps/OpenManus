from typing import TypedDict, Literal, List, Dict, Any
from langchain_core.messages import BaseMessage

class State(TypedDict):
    """Type definition for the workflow state."""
    messages: List[BaseMessage]
    full_plan: str
    next: str
    deep_thinking_mode: bool
    search_before_planning: bool
    search_results: List[Dict[str, Any]]

class ToolCall(TypedDict):
    """Type definition for a tool call."""
    name: str
    args: Dict[str, Any]

class Router(TypedDict):
    """Type definition for the supervisor's routing decision."""
    next: Literal['coordinator', 'planner', 'supervisor', 'researcher', 'coder', 'browser', 'reporter', 'FINISH']
    tool_call: ToolCall
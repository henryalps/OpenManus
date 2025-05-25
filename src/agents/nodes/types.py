from typing import TypedDict, Literal, List
from langchain_core.messages import BaseMessage


class State(TypedDict):
    """Type definition for the workflow state."""

    messages: List[BaseMessage]
    full_plan: str
    next: str
    deep_thinking_mode: bool
    search_before_planning: bool


class Router(TypedDict):
    """Type definition for the supervisor's routing decision."""

    next: Literal[
        "coordinator",
        "planner",
        "supervisor",
        "researcher",
        "coder",
        "browser",
        "reporter",
        "FINISH",
    ]

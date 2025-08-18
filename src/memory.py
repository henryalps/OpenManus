import json
import os
from typing import Dict, Any

from .agents.nodes.types import State

MEMORY_FILE = "memory.json"

def save_state(state: State):
    """
    Saves the state to a JSON file.

    Args:
        state (State): The state to save.
    """
    with open(MEMORY_FILE, "w") as f:
        json.dump(state, f, indent=4)

def load_state() -> State:
    """
    Loads the state from a JSON file.

    Returns:
        State: The loaded state.
    """
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "messages": [],
            "full_plan": "",
            "next": "coordinator",
            "deep_thinking_mode": False,
            "search_before_planning": False,
            "search_results": [],
            "tool_call": None,
        }

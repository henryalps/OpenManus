import json
import importlib
from typing import Dict
from langchain_core.runnables import Runnable
from langchain_core.tools import tool as tool_decorator

REGISTRY_FILE = "tool_registry.json"

# A dictionary to store all the tools
_tools: Dict[str, Runnable] = {}
_tool_info: Dict[str, Dict[str, str]] = {}

def save_registry():
    """Saves the tool registry to a file."""
    with open(REGISTRY_FILE, "w") as f:
        json.dump(_tool_info, f, indent=4)

def load_registry():
    """Loads the tool registry from a file."""
    global _tools, _tool_info
    try:
        with open(REGISTRY_FILE, "r") as f:
            _tool_info = json.load(f)
        for name, info in _tool_info.items():
            module = importlib.import_module(info["module"])
            func = getattr(module, info["function"])
            if isinstance(func, Runnable):
                _tools[name] = func
            else:
                _tools[name] = tool_decorator(func)
    except FileNotFoundError:
        _tools = {}
        _tool_info = {}

def register_tool(name: str, tool: Runnable, module_name: str, function_name: str):
    """
    Registers a new tool in the tool registry.

    Args:
        name (str): The name of the tool.
        tool (Runnable): The tool runnable.
        module_name (str): The name of the module where the tool function is defined.
        function_name (str): The name of the tool function.
    """
    _tools[name] = tool
    _tool_info[name] = {"module": module_name, "function": function_name}
    save_registry()

def delete_tool(name: str):
    """Deletes a tool from the registry."""
    if name in _tools:
        del _tools[name]
        del _tool_info[name]
        save_registry()

def get_tool(name: str) -> Runnable:
    """
    Gets a tool from the tool registry.

    Args:
        name (str): The name of the tool.

    Returns:
        Runnable: The tool runnable.
    """
    return _tools.get(name)

def get_all_tools() -> Dict[str, Runnable]:
    """
    Gets all the tools from the tool registry.

    Returns:
        Dict[str, Runnable]: A dictionary of all the tools.
    """
    return _tools

load_registry()

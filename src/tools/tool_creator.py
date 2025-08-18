import os
import inspect
from typing import Callable, Any

from .tool_registry import register_tool
from langchain_core.tools import tool

@tool
def create_tool(name: str, code: str, llm: any = None) -> str:
    """
    Creates a new tool from a string of Python code and registers it in the tool registry.
    The code should define a single function.

    Args:
        name (str): The name of the new tool.
        code (str): The Python code that defines the new tool.
        llm (any, optional): The language model to pass to the new tool. Defaults to None.

    Returns:
        str: A message indicating the tool was created successfully.
    """
    try:
        # Save the code to a file
        file_path = f"src/tools/custom/{name}.py"
        with open(file_path, "w") as f:
            f.write(code)

        # Execute the code in a new scope
        local_scope = {}
        exec(code, globals(), local_scope)

        # Find the new function in the local scope
        new_tool_func = None
        for func_name, value in local_scope.items():
            if inspect.isfunction(value):
                new_tool_func = value
                break

        if new_tool_func is None:
            return "Error: No function defined in the provided code."

        # Decorate the new function with @tool
        if llm:
            import functools
            new_tool_func = functools.partial(new_tool_func, llm=llm)

        decorated_tool = tool(new_tool_func)

        # Register the new tool
        register_tool(name, decorated_tool, f"src.tools.custom.{name}", new_tool_func.__name__)

        return f"Tool '{name}' created and registered successfully."
    except Exception as e:
        return f"Error creating tool: {e}"

import io
import sys
from contextlib import redirect_stdout

from langchain_core.tools import tool

@tool
def execute_python_code(code: str) -> str:
    """
    Executes a string of Python code and returns the output.

    Args:
        code (str): The Python code to execute.

    Returns:
        str: The output of the executed code.
    """
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            exec(code, {})
        except Exception as e:
            return str(e)
    return f.getvalue()

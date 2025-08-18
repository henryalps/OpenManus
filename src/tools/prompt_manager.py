from src.prompts.prompt_registry import register_prompt, get_prompt, delete_prompt_from_registry
from langchain_core.tools import tool

@tool
def create_prompt(name: str, prompt: str) -> str:
    """
    Creates a new prompt and registers it in the prompt registry.

    Args:
        name (str): The name of the prompt.
        prompt (str): The prompt string.

    Returns:
        str: A message indicating the prompt was created successfully.
    """
    if get_prompt(name):
        return f"Error: Prompt '{name}' already exists."
    register_prompt(name, prompt)
    return f"Prompt '{name}' created and registered successfully."

@tool
def update_prompt(name: str, prompt: str) -> str:
    """
    Updates an existing prompt in the prompt registry.

    Args:
        name (str): The name of the prompt to update.
        prompt (str): The new prompt string.

    Returns:
        str: A message indicating the prompt was updated successfully.
    """
    if not get_prompt(name):
        return f"Error: Prompt '{name}' not found."
    register_prompt(name, prompt)
    return f"Prompt '{name}' updated successfully."

@tool
def delete_prompt(name: str) -> str:
    """
    Deletes a prompt from the prompt registry.

    Args:
        name (str): The name of the prompt to delete.

    Returns:
        str: A message indicating the prompt was deleted successfully.
    """
    if not get_prompt(name):
        return f"Error: Prompt '{name}' not found."
    delete_prompt_from_registry(name)
    return f"Prompt '{name}' deleted successfully."

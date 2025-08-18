from typing import Dict

# A dictionary to store all the prompts
_prompts: Dict[str, str] = {}

def register_prompt(name: str, prompt: str):
    """
    Registers a new prompt in the prompt registry.

    Args:
        name (str): The name of the prompt.
        prompt (str): The prompt string.
    """
    _prompts[name] = prompt

def get_prompt(name: str) -> str:
    """
    Gets a prompt from the prompt registry.

    Args:
        name (str): The name of the prompt.

    Returns:
        str: The prompt string.
    """
    return _prompts.get(name)

def get_all_prompts() -> Dict[str, str]:
    """
    Gets all the prompts from the prompt registry.

    Returns:
        Dict[str, str]: A dictionary of all the prompts.
    """
    return _prompts

def delete_prompt_from_registry(name: str):
    """
    Deletes a prompt from the prompt registry.

    Args:
        name (str): The name of the prompt to delete.
    """
    if name in _prompts:
        del _prompts[name]

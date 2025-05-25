from src.config.agents import LLMType
from src.config.env import (
    BASIC_API_KEY,
    BASIC_BASE_URL,
    BASIC_MODEL,
    REASONING_API_KEY,
    REASONING_BASE_URL,
    REASONING_MODEL,
    VL_API_KEY,
    VL_BASE_URL,
    VL_MODEL,
    # AZURE_API_BASE, # F401 unused
    # AZURE_API_KEY, # F401 unused
    # AZURE_API_VERSION, # F401 unused
    BASIC_AZURE_DEPLOYMENT,
    VL_AZURE_DEPLOYMENT,
    REASONING_AZURE_DEPLOYMENT,
)


class PlaceholderLLM:
    def __init__(self, model_name):
        self.model_name = model_name

    def invoke(self, messages):
        return f"Placeholder LLM: {self.model_name} invoked with messages: {messages}"


def get_llm_by_type(llm_type: LLMType):
    if llm_type == "reasoning":
        model_name = REASONING_MODEL
        base_url = REASONING_BASE_URL
        api_key = REASONING_API_KEY
        azure_deployment = REASONING_AZURE_DEPLOYMENT
    elif llm_type == "vision":
        model_name = VL_MODEL
        base_url = VL_BASE_URL
        api_key = VL_API_KEY
        azure_deployment = VL_AZURE_DEPLOYMENT
    elif llm_type == "basic":
        model_name = BASIC_MODEL
        base_url = BASIC_BASE_URL
        api_key = BASIC_API_KEY
        azure_deployment = BASIC_AZURE_DEPLOYMENT
    else:
        raise ValueError(f"Unknown LLM type: {llm_type}")

    return PlaceholderLLM(model_name)

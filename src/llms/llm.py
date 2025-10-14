import os
from typing import Literal, Type

from langchain_openai import ChatOpenAI

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
    AZURE_API_BASE,
    AZURE_API_KEY,
    AZURE_API_VERSION,
    BASIC_AZURE_DEPLOYMENT,
    VL_AZURE_DEPLOYMENT,
    REASONING_AZURE_DEPLOYMENT
)
from src.llms.manus_llm import ManusLLM

class PlaceholderLLM:
    def __init__(self, model_name):
        self.model_name = model_name

    def invoke(self, messages):
        return f"Placeholder LLM ({self.model_name}) - API key not configured. Please add API keys to .env file."

    def stream(self, messages):
        """Generator that yields the response as chunks for streaming."""
        response = self.invoke(messages)
        # Yield the response in chunks to simulate streaming
        for chunk in response.split():
            yield type('obj', (object,), {'content': chunk + ' '})()

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

    # If API key is configured, return real LLM client
    if api_key and base_url:
        # Check if this is Manus API
        if 'manus' in base_url.lower():
            # Remove /v1 suffix if present for Manus base URL
            manus_base = base_url.replace('/v1', '')
            return ManusLLM(
                api_key=api_key,
                model="chat",  # Use 'chat' task mode for basic LLM
                base_url=manus_base
            )
        else:
            # Use standard OpenAI-compatible client
            return ChatOpenAI(
                model=model_name,
                openai_api_key=api_key,
                openai_api_base=base_url,
                temperature=0.7,
            )

    # Otherwise return placeholder
    return PlaceholderLLM(model_name)
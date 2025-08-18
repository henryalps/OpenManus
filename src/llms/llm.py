import os
from typing import Literal, Type

from src.config.agents import LLMType
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel

from src.config.env import (
    # OpenAI
    BASIC_API_KEY,
    BASIC_BASE_URL,
    BASIC_MODEL,
    REASONING_API_KEY,
    REASONING_BASE_URL,
    REASONING_MODEL,
    VL_API_KEY,
    VL_BASE_URL,
    VL_MODEL,
)


def get_llm_by_type(llm_type: LLMType) -> BaseChatModel:
    """Get the LLM for the given LLM type."""

    # Default to OpenAI-compatible API
    if llm_type == "reasoning":
        model_name = REASONING_MODEL
        base_url = REASONING_BASE_URL
        api_key = REASONING_API_KEY
    elif llm_type == "vision":
        model_name = VL_MODEL
        base_url = VL_BASE_URL
        api_key = VL_API_KEY
    else:
        model_name = BASIC_MODEL
        base_url = BASIC_BASE_URL
        api_key = BASIC_API_KEY

    return ChatOpenAI(
        model_name=model_name,
        base_url=base_url,
        api_key=api_key,
    )
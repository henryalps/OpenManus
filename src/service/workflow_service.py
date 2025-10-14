"""Workflow service for managing agent workflow execution."""

import asyncio
from typing import AsyncGenerator, Dict, List

from langchain_core.messages import HumanMessage, AIMessage

from src.workflow.graph import build_graph


async def run_agent_workflow(
    messages: List[Dict[str, str]], debug: bool = False
) -> AsyncGenerator[Dict[str, str], None]:
    """Run the agent workflow with the given messages.

    Args:
        messages: List of chat messages
        debug: Whether to enable debug logging

    Yields:
        Event data for SSE streaming
    """
    # Initialize workflow graph
    workflow = build_graph()

    # Convert dict messages to LangChain message objects
    langchain_messages = []
    for msg in messages:
        if msg.role == "user":
            langchain_messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            langchain_messages.append(AIMessage(content=msg.content))

    # Run workflow
    async for event in workflow.astream({"messages": langchain_messages}):
        yield {
            "event": "message",
            "data": {"content": str(event), "role": "assistant"}
        }
        # Small delay to avoid overwhelming the client
        await asyncio.sleep(0.1)
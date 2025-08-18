"""Workflow service for managing agent workflow execution."""

import asyncio
from typing import AsyncGenerator, Dict, List

from src.workflow.graph import build_graph
from src.prompts.template import OpenManusPromptTemplate


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

    # Format messages with system prompt
    formatted_messages = OpenManusPromptTemplate.apply_prompt_template(
        "coordinator", {"messages": messages}
    )

    # Run workflow
    initial_state = {"messages": formatted_messages, "next": "supervisor"}
    async for event in workflow.astream(initial_state):
        yield {
            "event": "message",
            "data": {"content": event.get("content", ""), "role": "assistant"}
        }
        # Small delay to avoid overwhelming the client
        await asyncio.sleep(0.1)
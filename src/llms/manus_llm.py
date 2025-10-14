"""Custom LLM client for Manus API."""

import time
import requests
from typing import List, Dict, Any, Iterator
from langchain_core.messages import BaseMessage, AIMessage


class ManusLLM:
    """Custom LLM client for Manus API."""

    def __init__(self, api_key: str, model: str = "chat", base_url: str = "https://api.manus.ai"):
        """Initialize Manus LLM client.

        Args:
            api_key: Manus API key
            model: Task mode ('chat', 'adaptive', or 'agent')
            base_url: Base URL for Manus API
        """
        self.api_key = api_key
        self.model = model  # taskMode in Manus API
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'API_KEY': api_key
        })

    def _create_task(self, prompt: str, task_id: str = None) -> Dict[str, Any]:
        """Create a new task in Manus.

        Args:
            prompt: The user's message
            task_id: Optional task ID for continuing a conversation

        Returns:
            Dict with task_id, task_title, task_url
        """
        payload = {
            "prompt": prompt,
            "taskMode": self.model,
        }

        if task_id:
            payload["taskId"] = task_id

        response = self.session.post(
            f"{self.base_url}/v1/tasks",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def _get_task(self, task_id: str) -> Dict[str, Any]:
        """Get task status and output.

        Args:
            task_id: The task ID

        Returns:
            Dict with task details including output
        """
        response = self.session.get(
            f"{self.base_url}/v1/tasks/{task_id}",
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def _wait_for_completion(self, task_id: str, max_wait: int = 300, poll_interval: int = 2) -> Dict[str, Any]:
        """Wait for task to complete.

        Args:
            task_id: The task ID
            max_wait: Maximum time to wait in seconds
            poll_interval: Time between polls in seconds

        Returns:
            Completed task details
        """
        start_time = time.time()

        while time.time() - start_time < max_wait:
            task = self._get_task(task_id)

            if task.get('status') == 'completed':
                return task
            elif task.get('status') == 'failed':
                raise RuntimeError(f"Task failed: {task}")

            time.sleep(poll_interval)

        raise TimeoutError(f"Task {task_id} did not complete within {max_wait} seconds")

    def _extract_response(self, task: Dict[str, Any]) -> str:
        """Extract the assistant's response from task output.

        Args:
            task: The completed task details

        Returns:
            Assistant's response text
        """
        output = task.get('output', [])

        # Find the last assistant message
        for item in reversed(output):
            if item.get('role') == 'assistant' and item.get('type') == 'message':
                content = item.get('content', [])
                for content_item in content:
                    if content_item.get('type') == 'output_text':
                        return content_item.get('text', '')

        return "No response from Manus"

    def invoke(self, messages: List[Any]) -> AIMessage:
        """Invoke the Manus LLM with a list of messages.

        Args:
            messages: List of LangChain message objects or dicts

        Returns:
            AIMessage with the response
        """
        # Extract the last user message as the prompt
        # Manus API doesn't support full conversation history in the same way
        prompt = ""
        for msg in messages:
            # Handle both dict and LangChain message objects
            if isinstance(msg, dict):
                role = msg.get('role', '')
                content = msg.get('content', '')
            else:
                # LangChain message object
                role = getattr(msg, 'type', '')
                content = getattr(msg, 'content', '')

            if role in ['user', 'human']:
                prompt = content

        if not prompt:
            prompt = "Hello"

        # Create task
        task_result = self._create_task(prompt)
        task_id = task_result['task_id']

        # Wait for completion
        completed_task = self._wait_for_completion(task_id)

        # Extract response
        response_text = self._extract_response(completed_task)

        return AIMessage(content=response_text)

    def stream(self, messages: List[Any]) -> Iterator[Any]:
        """Stream the response from Manus LLM.

        Note: Manus API doesn't support true streaming, so we simulate it
        by yielding the complete response in chunks.

        Args:
            messages: List of LangChain message objects or dicts

        Yields:
            Chunks of the response
        """
        # Get the full response
        response = self.invoke(messages)

        # Simulate streaming by yielding words
        words = response.content.split()
        for word in words:
            yield type('obj', (object,), {'content': word + ' '})()

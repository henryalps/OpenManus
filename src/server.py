import json
import logging
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

# E402: Moved import to top
from src.service.workflow_service import run_agent_workflow

# Configure logging
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="IntelliAgent API",
    description="API for IntelliAgent LangGraph-based agent workflow",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class ChatMessage(BaseModel):
    role: str = Field(
        ..., description="The role of the message sender (user or assistant)"  # Wrapped
    )
    content: str = Field(..., description="The content of the message")


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(
        ..., description="The conversation history"  # Wrapped
    )
    debug: Optional[bool] = Field(False, description="Whether to enable debug logging")


@app.post("/api/chat/stream")
async def chat_stream_endpoint(request: ChatRequest, req: Request):
    """Chat endpoint for LangGraph invoke.

    Args:
        request: The chat request
        req: The FastAPI request object for connection state checking

    Returns:
        The streamed response
    """
    try:

        async def event_generator():
            async for event in run_agent_workflow(
                request.messages, request.debug
            ):  # Wrapped
                # Check if client is still connected
                if await req.is_disconnected():
                    logger.info("Client disconnected, stopping workflow")
                    break
                yield {
                    "event": event["event"],
                    "data": json.dumps(event["data"], ensure_ascii=False),
                }

        return EventSourceResponse(
            event_generator(), media_type="text/event-stream"
        )  # Wrapped
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=True)

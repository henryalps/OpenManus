# OpenManus Bug Fixes and Implementation Report

## Executive Summary

This document details all bugs encountered and fixed in the OpenManus project, along with the implementation of Manus API integration. The project was non-functional due to multiple critical issues across the Docker setup, backend workflow, frontend UI, and LLM integration.

**Status**: All critical bugs resolved. System now fully operational with Manus API integration.

---

## Bug Fixes (Chronological Order)

### 1. Shell Script Line Endings Bug
**Severity**: Critical - Container startup failure
**Error**: `: not found` errors when running `start.sh` in Docker container
**Root Cause**: Windows CRLF line endings incompatible with Unix bash

**Files Affected**:
- `docker/unified/start.sh`

**Solution**:
- Converted CRLF to LF line endings using `sed -i 's/\r$//'`
- Created `.gitattributes` with `*.sh text eol=lf` to prevent future issues
- Changed Dockerfile CMD from `sh` to `bash`

**Files Modified**:
- `docker/unified/start.sh` (line ending conversion)
- `.gitattributes` (NEW)
- `docker/unified/Dockerfile` (line 13: `sh` → `bash`)

---

### 2. Missing LangGraph Command Import
**Severity**: Critical - Application crash on startup
**Error**: `TypeError: Expected a Runnable, callable or dict. Instead got an unsupported type: <class 'module'>`
**Root Cause**: Three node files missing `from langgraph.types import Command` import

**Files Affected**:
- `src/agents/nodes/coordinator_node.py`
- `src/agents/nodes/planner_node.py`
- `src/agents/nodes/browser_node.py`

**Solution**:
- Added `from langgraph.types import Command` to all three node files

**Files Modified**:
- `src/agents/nodes/coordinator_node.py` (added line 5)
- `src/agents/nodes/planner_node.py` (added line 7)
- `src/agents/nodes/browser_node.py` (added line 5)

---

### 3. Missing Package __init__.py
**Severity**: Critical - Module import failure
**Error**: Node modules not properly exported
**Root Cause**: `src/agents/nodes/` directory missing `__init__.py`

**Solution**:
- Created `__init__.py` with proper exports for all node functions

**Files Created**:
- `src/agents/nodes/__init__.py` (NEW - 17 lines)

---

### 4. Invalid Graph Configuration
**Severity**: Critical - Workflow initialization failure
**Error**: `TypeError: add_edge() got an unexpected keyword argument 'condition'`
**Root Cause**: Graph using incorrect LangGraph API syntax for conditional edges

**Files Affected**:
- `src/workflow/graph.py`

**Solution**:
- Simplified graph to only set entry point
- Let Command objects handle routing instead of conditional edges
- Removed invalid `add_edge(..., condition=...)` syntax

**Files Modified**:
- `src/workflow/graph.py` (lines 13-29, removed conditional edge logic)

---

### 5. Template Regex Bug
**Severity**: High - Template formatting crash
**Error**: `IndexError: tuple index out of range` in string formatting
**Root Cause**: Incorrect regex pattern `r"{1}"` instead of `r"{\1}"` for backreference

**Files Affected**:
- `src/prompts/template.py`

**Solution**:
- Fixed regex pattern to use proper backreference syntax

**Files Modified**:
- `src/prompts/template.py` (line 30: `r"{1}"` → `r"{\1}"`)

---

### 6. Missing TEAM_MEMBERS Variable
**Severity**: High - Prompt template failure
**Error**: `KeyError: 'TEAM_MEMBERS'`
**Root Cause**: Planner prompt uses `TEAM_MEMBERS` variable but template function didn't provide it

**Files Affected**:
- `src/prompts/template.py`

**Solution**:
- Updated `apply_prompt_template()` to import and include TEAM_MEMBERS from config
- Added dynamic template variable handling

**Files Modified**:
- `src/prompts/template.py` (lines 44-70, added TEAM_MEMBERS support)

---

### 7. Message Object Type Mismatch
**Severity**: High - Message processing crash
**Error**: `TypeError: 'ChatMessage' object is not subscriptable`
**Root Cause**: Trying to access Pydantic model with dict syntax `msg["role"]`

**Files Affected**:
- `src/service/workflow_service.py`

**Solution**:
- Changed from dict access (`msg["role"]`) to attribute access (`msg.role`)
- Updated message conversion logic for LangChain objects

**Files Modified**:
- `src/service/workflow_service.py` (lines 26-32)

---

### 8. PlaceholderLLM String Response Handling
**Severity**: Medium - Type error with placeholder LLM
**Error**: `AttributeError: 'str' object has no attribute 'content'`
**Root Cause**: PlaceholderLLM returns strings, code expected message objects with `.content` attribute

**Files Affected**:
- `src/agents/nodes/coordinator_node.py`

**Solution**:
- Added type checking to handle both string and message object responses
- Only string responses are used directly, message objects use `.content`

**Files Modified**:
- `src/agents/nodes/coordinator_node.py` (lines 22-26)

---

### 9. JSON Repair Corrupting Non-JSON
**Severity**: Medium - Message content corruption
**Error**: Plain text messages converted to empty string `""`
**Root Cause**: `json_repair` converting non-JSON plain text to empty JSON

**Files Affected**:
- `src/agents/nodes/coordinator_node.py`

**Solution**:
- Only call `repair_json_output()` if content looks like JSON (starts with `{` or `[`)

**Files Modified**:
- `src/agents/nodes/coordinator_node.py` (lines 28-30)

---

### 10. PlaceholderLLM Missing stream() Method
**Severity**: Medium - Method not found error
**Error**: `AttributeError: 'PlaceholderLLM' object has no attribute 'stream'`
**Root Cause**: `planner_node` calls `llm.stream()` but PlaceholderLLM only had `invoke()`

**Files Affected**:
- `src/llms/llm.py`

**Solution**:
- Added `stream()` method to PlaceholderLLM that yields response in chunks

**Files Modified**:
- `src/llms/llm.py` (lines 32-37)

---

### 11. Non-functional Frontend - No Event Handlers
**Severity**: Critical - UI completely non-interactive
**Error**: User reported "nothing happens when I click send"
**Root Cause**: ChatInput component had no event handlers at all

**Files Affected**:
- `src/components/ChatInput.js`

**Solution**:
- Complete rewrite adding useState, onChange, onClick, onKeyPress handlers
- Implemented proper form submission logic

**Files Modified**:
- `src/components/ChatInput.js` (complete rewrite, 39 lines)

---

### 12. Frontend Not Connected to Backend
**Severity**: Critical - No API communication
**Error**: Generic "network error" shown to user
**Root Cause**: Frontend not calling backend API at all

**Files Affected**:
- `src/pages/index.js`

**Solution**:
- Implemented fetch to `/api/chat/stream` with SSE parsing
- Added error handling with helpful messages
- Added response parsing for Python dict format

**Files Modified**:
- `src/pages/index.js` (lines 9-105, added handleSendMessage function)

---

### 13. Raw Data Displayed in UI
**Severity**: Medium - Poor user experience
**Error**: UI showing `{'coordinator': {'messages': [HumanMessage(...)]}}` instead of actual message
**Root Cause**: Frontend not parsing Python dict format from SSE stream

**Files Affected**:
- `src/pages/index.js`

**Solution**:
- Added regex extraction to parse `HumanMessage(content='...')` format
- Properly extract text content from nested structures

**Files Modified**:
- `src/pages/index.js` (lines 65-75, added parsing logic)

---

### 14. Improved ChatDisplay Styling
**Severity**: Low - UI/UX improvement
**Error**: No visual distinction between messages, poor empty state
**Root Cause**: Basic styling with no message bubbles or formatting

**Files Affected**:
- `src/components/ChatDisplay.js`

**Solution**:
- Added message bubbles with different colors for user/assistant
- Added empty state message
- Improved spacing and readability

**Files Modified**:
- `src/components/ChatDisplay.js` (lines 3-42, enhanced styling)

---

### 15. LLM Always Returns Placeholder
**Severity**: Critical - API integration not working
**Error**: Even with API keys configured, system uses PlaceholderLLM
**Root Cause**: `get_llm_by_type()` loaded config but always returned PlaceholderLLM

**Files Affected**:
- `src/llms/llm.py`

**Solution**:
- Added conditional logic to create ChatOpenAI when api_key and base_url exist
- Only return PlaceholderLLM when no API keys configured

**Files Modified**:
- `src/llms/llm.py` (lines 58-65, added actual LLM client creation)

---

### 16. Missing langchain-openai Package
**Severity**: High - Module import failure
**Error**: `ModuleNotFoundError: No module named 'langchain_openai'`
**Root Cause**: Added import but package not in requirements.txt

**Files Affected**:
- `requirements.txt`

**Solution**:
- Added `langchain-openai>=0.2.0` to requirements.txt

**Files Modified**:
- `requirements.txt` (line 13, added langchain-openai)

---

### 17. Client.py Wrong Configuration
**Severity**: Medium - CLI client broken
**Error**: Connecting to wrong port (5000) and wrong endpoint (/task)
**Root Cause**: Outdated client code didn't match current API

**Files Affected**:
- `src/client.py`

**Solution**:
- Updated to port 8000 and `/api/chat/stream` endpoint
- Added SSE stream parsing
- Added response extraction from Python dict format

**Files Modified**:
- `src/client.py` (complete rewrite, 50 lines)

---

## New Feature: Manus API Integration

### 18. Manus API Custom Client Implementation
**Severity**: Feature - New functionality
**Challenge**: Manus API is task-based (not OpenAI-compatible chat API)

**Analysis**:
- Manus API uses task creation pattern: POST `/v1/tasks` → poll GET `/v1/tasks/{task_id}`
- Authentication via `API_KEY` header (not `Authorization: Bearer`)
- Response format contains conversation output array with role/content structure

**Solution**:
- Created custom `ManusLLM` class implementing LangChain-compatible interface
- Implements `invoke()` and `stream()` methods
- Handles task creation, polling, and response extraction
- Compatible with existing OpenManus agent workflow

**Files Created**:
- `src/llms/manus_llm.py` (NEW - 176 lines)

**Files Modified**:
- `src/llms/llm.py` (lines 24, 59-77: added ManusLLM import and detection logic)
- `.env` (configured with Manus API credentials)

**API Documentation Used**:
- Base URL: `https://api.manus.ai`
- Endpoint: `POST /v1/tasks` (create), `GET /v1/tasks/{task_id}` (retrieve)
- Auth: `API_KEY` header
- Docs: https://open.manus.ai/docs

---

## Documentation Updates

### 19. Updated README.md
**Changes**:
- Added comprehensive API key configuration section
- Fixed docker-compose example
- Updated API documentation
- Corrected CLI usage examples
- Added supported LLM providers list

**Files Modified**:
- `README.md` (lines 102-159, Configuration section rewritten)

---

### 20. Created .env.example
**Purpose**: Template for users to configure their own API keys

**Files Created**:
- `.env.example` (NEW - 47 lines)

---

## Statistics

**Total Files Modified**: 15
**Total Files Created**: 5
**Total Lines Changed**: ~800+
**Bugs Fixed**: 17
**New Features**: 1 (Manus API integration)

**Categories**:
- Docker/Infrastructure: 2 bugs
- Backend/Workflow: 8 bugs
- Frontend/UI: 4 bugs
- LLM Integration: 3 bugs + 1 feature
- Documentation: 2 improvements

---

## Testing Results

### CLI Client
✅ **Working** - Successfully processes queries and returns responses
```bash
$ python src/client.py --task "What is 2+2?"
Response: 2+2 is 4.
```

### Web Interface
✅ **Frontend Running** - http://localhost:3000
✅ **Backend Running** - http://localhost:8000
✅ **API Communication** - SSE streaming working

### Docker Containers
✅ **unified container** - Backend and tools server running
✅ **frontend container** - Next.js dev server running

---

## Recommendations for Future Work

1. **Multi-turn Conversations**: Implement task continuation using `taskId` parameter in Manus API
2. **Streaming Optimization**: Currently simulates streaming by word-splitting; consider websocket for true streaming
3. **Error Recovery**: Add retry logic for transient Manus API errors
4. **Rate Limiting**: Implement rate limit handling for Manus API (visible in headers)
5. **Configuration UI**: Add web interface for API key configuration
6. **Testing Suite**: Add unit tests for ManusLLM and integration tests for workflow
7. **Vision Support**: Implement attachment handling for Manus vision capabilities
8. **Connector Integration**: Explore Manus connectors for enhanced capabilities

---

## Conclusion

The OpenManus project had multiple critical bugs preventing any functionality. After systematic debugging and the implementation of Manus API integration, the system is now fully operational. All components (Docker, backend, frontend, CLI) are working correctly with the Manus AI service.

The Manus API integration required a custom client implementation due to its task-based architecture, which differs from standard OpenAI-compatible APIs. This implementation maintains compatibility with the existing LangChain-based agent workflow while adapting to Manus's unique API patterns.

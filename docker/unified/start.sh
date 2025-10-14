#!/bin/bash

# Start FastAPI server in background
PYTHONPATH=/app:/app/src python3 -m uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload &

# Start tools server in background
PYTHONPATH=/app:/app/src python3 src/tools/server.py &

# Wait for all background processes to complete
wait

# Exit with the status of the last command
exit $?

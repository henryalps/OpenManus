import argparse
import requests
import json
import re

def submit_task(task, host="http://localhost:8000"):
    """Submit a task to the agent server."""
    try:
        # Use the correct endpoint
        response = requests.post(
            f"{host}/api/chat/stream",
            json={"messages": [{"role": "user", "content": task}]},
            stream=True
        )
        response.raise_for_status()

        # Parse SSE stream
        full_response = ""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])
                        content = data.get('content', '')

                        # Extract message from Python dict format
                        match = re.search(r"HumanMessage\(content='([^']+)'", content)
                        if match:
                            full_response = match.group(1)
                        else:
                            full_response += content
                    except json.JSONDecodeError:
                        pass

        return {"status": "success", "response": full_response or "No response received"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="OpenManus CLI Client")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--host", default="http://localhost:8000", help="Agent server host (default: http://localhost:8000)")

    args = parser.parse_args()

    print(f"Submitting task: {args.task}")
    print("-" * 50)

    result = submit_task(args.task, args.host)

    if result.get("status") == "success":
        print("\nResponse:")
        print(result["response"])
    else:
        print("\nError:")
        print(result.get("error", "Unknown error"))

if __name__ == "__main__":
    main() 
import argparse
import requests
import json

def submit_task(task, host="http://localhost:8000"):
    """Submit a task to the agent server and stream the response."""
    endpoint = "/api/chat/stream"
    payload = {
        "messages": [
            {"role": "user", "content": task}
        ],
        "debug": False
    }

    with requests.post(f"{host}{endpoint}", json=payload, stream=True) as resp:
        resp.raise_for_status()
        try:
            for line in resp.iter_lines(decode_unicode=True):
                if line:
                    print(line)
        except requests.exceptions.ChunkedEncodingError:
            # Stream closed early; ignore remaining
            pass

def main():
    parser = argparse.ArgumentParser(description="OpenManus CLI Client")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument(
        "--host",
        default="http://localhost:8000",
        help="Agent server host"
    )
    args = parser.parse_args()

    submit_task(args.task, args.host)

if __name__ == "__main__":
    main()

import argparse
import requests
import json


def submit_task(task, host="http://localhost:5000"):
    """Submit a task to the agent server."""
    try:
        response = requests.post(f"{host}/task", json={"task": task})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="IntelliAgent CLI Client")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument(
        "--host", default="http://localhost:5000", help="Agent server host"
    )

    args = parser.parse_args()

    result = submit_task(args.task, args.host)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

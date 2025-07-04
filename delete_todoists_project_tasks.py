import argparse
import os

import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")


def fetch_tasks(project_id):
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {"Authorization": f"Bearer {TODOIST_API_TOKEN}"}
    params = {"project_id": project_id}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ Error fetching tasks: {response.status_code} - {response.text}")
        return []
    return response.json()


def delete_task(task_id):
    url = f"https://api.todoist.com/rest/v2/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {TODOIST_API_TOKEN}"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"✅ Deleted task ID {task_id}")
    else:
        print(
            f"❌ Failed to delete task {task_id}: {response.status_code} - {response.text}"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Delete all tasks in a Todoist project."
    )
    parser.add_argument("project_id", help="Todoist project ID")
    args = parser.parse_args()

    tasks = fetch_tasks(args.project_id)
    if not tasks:
        print("No tasks found or unable to fetch tasks.")
        return

    print(f"Found {len(tasks)} tasks. Deleting...")

    for task in tasks:
        delete_task(task["id"])


if __name__ == "__main__":
    main()

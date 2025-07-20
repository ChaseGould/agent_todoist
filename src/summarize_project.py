import argparse
import os
import re
from datetime import datetime

import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)

# Functions should be organized in order they are called in main.


def fetch_tasks(project_id):
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {"Authorization": f"Bearer {TODOIST_API_TOKEN}"}
    params = {"project_id": project_id}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return []
    return response.json()


def get_date_range(tasks):
    if not tasks:
        return None, None

    # Parse created_at strings into datetime objects
    dates = [
        datetime.fromisoformat(task["created_at"].replace("Z", "+00:00"))
        for task in tasks
    ]

    oldest = min(dates)
    newest = max(dates)
    return oldest, newest


def fetch_project_name(project_id):
    url = f"https://api.todoist.com/rest/v2/projects/{project_id}"
    headers = {"Authorization": f"Bearer {TODOIST_API_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(
            f"❌ Error fetching project name: {response.status_code} - {response.text}"
        )
        return "Unknown Project"
    return response.json().get("name", "Unknown Project")


def combine_text(task_texts):
    return "\n".join(f"- {text}" for text in task_texts)


def summarize_notes(joined_task_text, agent_type, length):

    if agent_type == "therapist":
        system_prompt = "You are a compassionate therapist helping someone reflect on their recent thoughts and experiences. Use their notes to compose a helpful message with emotional insight and empathy."
    elif agent_type == "assistant":
        system_prompt = "You are a helpful assistant that summarizes personal notes."
    else:
        system_prompt = "You are a compassionate therapist helping someone reflect on their recent thoughts and experiences. Using their notes, write a motivational and emotionally insightful first-person reflection as if the person is processing their thoughts themselves. The message should be self-aware, emotionally honest, motivational and gently introspective — like journaling with the guidance of a skilled mental health professional."

    if length == "long":
        detail_instruction = (
            "Make the summary detailed and expansive, capturing all meaningful nuances."
        )
    else:
        detail_instruction = (
            "Make the summary clear and concise while preserving important details."
        )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Here are my notes:\n{joined_task_text}\n\n{detail_instruction} Create one single concise summary that summarizes the main points from all of these notes. Make an effort to consolidate repetitive information.",
            },
        ],
    )
    return response.choices[0].message.content


def write_summary_to_file(project_name, agent_type, date_range_str, summary):
    # Ensure output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Clean up project name to make it filename-safe
    safe_project_name = re.sub(r'[\\/*?:"<>|]', "_", project_name)

    agent_type_str = str(agent_type)

    # Construct base filename
    base_filename = (
        f"{safe_project_name}_{agent_type_str}_{date_range_str.replace(' ', '_')}.txt"
    )
    file_path = os.path.join(output_dir, base_filename)

    # Check if file exists, and add a number if it does
    counter = 1
    while os.path.exists(file_path):
        numbered_filename = (
            f"{safe_project_name}_{date_range_str.replace(' ', '_')}_{counter}.txt"
        )
        file_path = os.path.join(output_dir, numbered_filename)
        counter += 1

    # Write summary to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"{project_name} Project Summary ({date_range_str})\n\n")
        f.write(summary)

    print(f"\n✅ Summary saved to: {file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Summarize Todoist project notes with ChatGPT."
    )
    parser.add_argument("project_id", help="Todoist project ID to summarize")
    parser.add_argument(
        "--agent_type",
        choices=["assistant", "therapist", "first_person"],
        default="first_person",  # ✅ default value
        help="Type of summarization agent: 'assistant' 'therapist' or 'first_person' (default: first_person)",
    )
    parser.add_argument(
        "--length",
        choices=["medium", "long"],
        default="medium",
        help="Length of the summary: medium', or 'long' (default: medium)",
    )

    args = parser.parse_args()

    tasks = fetch_tasks(args.project_id)
    notes = []
    for task in tasks:
        content = task.get("content", "")
        description = task.get("description", "")
        if description:
            notes.append(f"{content}\n  (Description: {description})")
        else:
            notes.append(content)

    if notes:
        # prepare inputs for summarize_notes
        oldest_task_date, newest_task_date = get_date_range(tasks)
        project_name = fetch_project_name(args.project_id)
        num_tasks = len(tasks)
        print("number of tasks to combine: " + str(num_tasks) + "\n")
        print("agent type: " + str(args.agent_type))
        joined_task_text = combine_text(notes)
        print(joined_task_text)

        summary = summarize_notes(joined_task_text, args.agent_type, args.length)

        date_range_str = f"{oldest_task_date.strftime('%Y-%m-%d')} to {newest_task_date.strftime('%Y-%m-%d')}"
        print(
            "\n" + project_name + " Project Summary " + date_range_str + ":\n",
            summary,
        )

        write_summary_to_file(project_name, args.agent_type, date_range_str, summary)
    else:
        print("No notes found.")


if __name__ == "__main__":
    main()

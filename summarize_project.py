import requests
from openai import OpenAI
import argparse
from datetime import datetime
import os
import re
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)

#Functions should be organized in order they are called in main.

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
    dates = [datetime.fromisoformat(task['created_at'].replace('Z', '+00:00')) for task in tasks]

    oldest = min(dates)
    newest = max(dates)
    return oldest, newest

def fetch_project_name(project_id):
    url = f"https://api.todoist.com/rest/v2/projects/{project_id}"
    headers = {"Authorization": f"Bearer {TODOIST_API_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error fetching project name: {response.status_code} - {response.text}")
        return "Unknown Project"
    return response.json().get("name", "Unknown Project")

def combine_text(task_texts):
    return "\n".join(f"- {text}" for text in task_texts)

def summarize_notes(joined_task_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes personal notes."},
            {"role": "user", "content": f"Here are my notes from this week:\n{joined_task_text}\n\n Create one single concise summary that summarizes the main points from all of these notes. Make an effort to consolidate repetitive information."}
        ]
    )
    return response.choices[0].message.content

def write_summary_to_file(project_name, date_range_str, summary):
    # Ensure output directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        # Clean up project name to make it filename-safe
        safe_project_name = re.sub(r'[\\/*?:"<>|]', "_", project_name)

        # Construct base filename
        base_filename = f"{safe_project_name}_{date_range_str.replace(' ', '_')}.txt"
        file_path = os.path.join(output_dir, base_filename)

        # Check if file exists, and add a number if it does
        counter = 1
        while os.path.exists(file_path):
            numbered_filename = f"{safe_project_name}_{date_range_str.replace(' ', '_')}_{counter}.txt"
            file_path = os.path.join(output_dir, numbered_filename)
            counter += 1

        # Write summary to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{project_name} Project Summary ({date_range_str})\n\n")
            f.write(summary)

        print(f"\n✅ Summary saved to: {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Summarize Todoist project notes with ChatGPT.")
    parser.add_argument("project_id", help="Todoist project ID to summarize")
    args = parser.parse_args()

    tasks = fetch_tasks(args.project_id)
    notes = [task["content"] for task in tasks]

    if notes:
        # prepare inputs for summarize_notes
        oldest_task_date, newest_task_date = get_date_range(tasks)
        project_name = fetch_project_name(args.project_id)
        num_tasks = len(tasks)
        print('number of tasks to combine =' + str(num_tasks) + "\n")
        joined_task_text = combine_text(notes)
        print(joined_task_text)

        summary = summarize_notes(joined_task_text)
        
        date_range_str = f"{oldest_task_date.strftime('%Y-%m-%d')} to {newest_task_date.strftime('%Y-%m-%d')}"
        print("\n" + project_name + " Project Summary " + date_range_str + ":\n", summary)

        write_summary_to_file(project_name, date_range_str, summary)
    else:
        print("No notes found.")

if __name__ == "__main__":
    main()

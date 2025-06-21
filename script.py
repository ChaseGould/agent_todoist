import requests
from openai import OpenAI
from datetime import datetime, timedelta

***REMOVED***
***REMOVED***
PROJECT_ID = "2354738723"

client = OpenAI(api_key=OPENAI_API_KEY)

# Get tasks from the project
def fetch_tasks():
    url = "https://api.todoist.com/rest/v2/tasks"
    headers = {"Authorization": f"Bearer {TODOIST_API_TOKEN}"}
    params = {"project_id": PROJECT_ID}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return []
    return response.json()


# Send task text to OpenAI for summarization
def summarize_notes(task_texts):
    joined_text = "\n".join(f"- {text}" for text in task_texts)

    print(joined_text)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes personal notes."},
            {"role": "user", "content": f"Here are my notes from this week:\n{joined_text}\n\n Create one single conscise summary that summarizes the main points from all of these notes. Make an effort to consolidate repetivie information."}
        ]
    )
    return response.choices[0].message.content

# Run the process
def run():
    tasks = fetch_tasks()
    notes = [task["content"] for task in tasks]
    if notes:
        summary = summarize_notes(notes)
        print("\n📝 Weekly Summary:\n", summary)
    else:
        print("No notes found.")

run()

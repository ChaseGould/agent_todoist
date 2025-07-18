import os

import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")

headers = {"Authorization": f"Bearer {TODOIST_API_TOKEN}"}

response = requests.get("https://api.todoist.com/rest/v2/projects", headers=headers)

if response.status_code == 200:
    for project in response.json():
        print(f"{project['name']} (ID: {project['id']})")
else:
    print(f"Error: {response.status_code} - {response.text}")

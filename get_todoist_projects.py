import requests

# Paste your token here or use an environment variable
***REMOVED***

headers = {
    "Authorization": f"Bearer {TODOIST_API_TOKEN}"
}

response = requests.get("https://api.todoist.com/rest/v2/projects", headers=headers)

if response.status_code == 200:
    for project in response.json():
        print(f"{project['name']} (ID: {project['id']})")
else:
    print(f"Error: {response.status_code} - {response.text}")

# Agent Todoist

A small Python tool that integrates Todoist and ChatGPT to:
- Summarize personal project notes using AI
- Delete tasks after summarizing

## Initial Setup
1. Rename `.env.example` to `.env`
2. Fill in your actual API keys:

## Run Scripts

### Get project ID's
Run get_todoist_projects.py to get projects id's.<br>
`python get_todoist_project.py`

### Summarize a project
Pass project id as an argument to summarize_project.py.<br>
`python summarize_project.py <project_id>`<br>
Project summary is saved to the output folder.<br>
Run with -h to see additonal argument options.

### Delete all tasks within a project
Pass project id as an argument to delete_todoists_project_tasks.py.<br>
`python delete_todoists_project_tasks.py <project_id>`<br>

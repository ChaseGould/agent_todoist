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

## TODO 
- Install continue.
- Figure out if any of the journal apps automate weekly reflections. Can I make a better app than them?
-- want to pass in entire repo to continue and ask it to improve my read me.
- Need to be able to run these scripts from my phone. Maybe pythonista.
- Script to push my summary to my phone so it's easy copy into any.do. could be an email or push to todoist.
  it's not hard to just open any.do and copy summary there.
- Add requirements file or is there a way to make my project install all of the necessary python packages?
- Stretch goal. I should probably just make my own ios app. I can make it do everything I want and make it better for me the any.do
  if its make my life easier that's great I dont expect it to make money but I can make it free and it'll look good on my resume.





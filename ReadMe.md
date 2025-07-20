# Todoist Project Management Scripts

This project provides a suite of Python scripts to manage and interact with your Todoist projects via the Todoist and OpenAI APIs.

## Features

- **Get Projects**: List all your Todoist projects and their IDs.
- **Summarize Projects**: Generate AI-powered summaries of your Todoist projects using OpenAI's GPT models.
- **Delete Project Tasks**: Bulk delete all tasks within a specific Todoist project.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    - Create a `.env` file in the root directory of the project by copying the `.env.example` file:
      ```bash
      cp .env.example .env
      ```
    - Open the `.env` file and add your API keys:
      ```
      OPENAI_API_KEY=your-openai-api-key-here
      TODOIST_API_TOKEN=your-todoist-token-here
      ```

## Usage

### Get project ID's
To get a list of all your Todoist projects and their corresponding IDs, run the following command:

```bash
python src/get_todoist_projects.py
```

### Summarize a Todoist Project

This script uses the OpenAI API to generate a summary of a specific Todoist project. You can choose from different summarization "agents" (`assistant`, `therapist`, or `first_person`) and specify the desired length of the summary (`medium` or `long`).

```bash
python src/summarize_project.py <project_id> [--agent_type <agent>] [--length <length>]
```

**Arguments:**

-   `project_id`: The ID of the Todoist project you want to summarize.
-   `--agent_type`: (Optional) The type of summarization agent to use. Choices are `assistant`, `therapist`, or `first_person`. Defaults to `first_person`.
-   `--length`: (Optional) The desired length of the summary. Choices are `medium` or `long`. Defaults to `medium`.

The summary will be saved to a text file in the `output` directory.

### Delete All Tasks in a Project

This script will delete all tasks in a specified Todo-ist project. **Use this with caution, as this action is irreversible.**

```bash
python src/delete_todoists_project_tasks.py <project_id>
```

**Argument:**

-   `project_id`: The ID of the Todoist project from which you want to delete all tasks.

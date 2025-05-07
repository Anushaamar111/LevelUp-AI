import json
import os
import datetime

TASK_HISTORY_FILE = "task_history.json"

# Save tasks to history
def save_tasks(tasks):
    today = datetime.date.today().isoformat()

    # Load existing history or initialize
    if os.path.exists(TASK_HISTORY_FILE):
        with open(TASK_HISTORY_FILE, "r") as file:
            history = json.load(file)
    else:
        history = {}

    # Add today's tasks
    history[today] = {
        "tasks": tasks,
        "completed": [False] * len(tasks)
    }

    # Write back
    with open(TASK_HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# Check if tasks for today already exist
def get_today_tasks():
    today = datetime.date.today().isoformat()
    if os.path.exists(TASK_HISTORY_FILE):
        with open(TASK_HISTORY_FILE, "r") as file:
            history = json.load(file)
        return history.get(today)
    return None

# Update task completion
def mark_task_complete(task_index):
    today = datetime.date.today().isoformat()
    if not os.path.exists(TASK_HISTORY_FILE):
        return

    with open(TASK_HISTORY_FILE, "r") as file:
        history = json.load(file)

    if today in history and 0 <= task_index < len(history[today]["completed"]):
        history[today]["completed"][task_index] = True

        with open(TASK_HISTORY_FILE, "w") as file:
            json.dump(history, file, indent=4)

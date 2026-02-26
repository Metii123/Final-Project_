import json
import os

FILE_PATH = "tasks.txt"

def load_tasks() -> list[dict]:
    if not os.path.exists(FILE_PATH):
        return[]
    
    tasks = []
    
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    return tasks

def save_tasks(tasks: list[dict]) -> None:
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(json.dumps(task) + "\n")

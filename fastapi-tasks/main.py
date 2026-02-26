from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

from Helper_Functions import load_tasks, save_tasks

app = FastAPI(title="Task Managment System", version="1.0")

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

def get_task(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.get("/", summary="Root Check")
def root():
    return{"message": "Task Management API is running", "docs": "/docs"}

@app.get("/tasks/stats", summary="Get Task Statistics")
def get_stats():
    tasks = load_tasks()
    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("completed"))
    not_completed = total - completed
    percentage = round((completed / total * 100), 2) if total > 0 else 0.0
    return {
        "total": total,
        "completed": completed,
        "not_completed": not_completed,
        "completion_percentage": percentage,
    }

@app.get("/tasks", summary="Get All Tasks & Filter Tasks")
def get_all_tasks(completed: bool | None = None):
    tasks = load_tasks()
    if completed is not None:
        tasks = [t for t in tasks if t.get("completed") == completed]
    return tasks

@app.get("/tasks/{task_id}", summary="Get Single Task")
def get_single_task(task_id: int = 1):
    return get_task(task_id)

@app.post("/tasks", status_code=201, summary="Create Task")
def create_task(task_data: TaskCreate):
    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {
        "id": new_id,
        "title": task_data.title,
        "description": task_data.description,
        "completed": False,
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task

@app.put("/tasks/{task_id}", summary="Update Task")
def update_task(task_data: TaskUpdate, task_id: int = 1):
    tasks = load_tasks()
    task = None

    for t in tasks:
        if t["id"] == task_id:
            task = t
            break
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_data.title is not None:
        task["title"] = task_data.title

    if task_data.description is not None:
        task["description"] = task_data.description
    
    if task_data.completed is not None:
        task["completed"] = task_data.completed
    save_tasks(tasks)
    return task

@app.delete("/tasks", summary="Delete All Tasks")
def delete_all_tasks():
    save_tasks([])
    return{"message": "All tasks deleted successfully"}

@app.delete("/tasks/{task_id}", summary="Delete Task")
def delete_task(task_id: int =  1):
    tasks = load_tasks()
    get_task(task_id)
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return{"message": f"Task {task_id} deleted successfully"}
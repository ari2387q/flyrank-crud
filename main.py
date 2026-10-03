from fastapi import FastAPI, HTTPException, status
from typing import Dict, Any

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API for managing tasks."
)

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": True},
    {"id": 3, "title": "Write API", "done": False}
]

@app.get("/", summary="API Root", description="Returns basic information about the API.")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health Check", description="Returns the health status of the server.")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", summary="List Tasks", description="Returns a list of all tasks.")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", summary="Get a Task", description="Returns a single task by its ID.")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a Task", description="Creates a new task. The 'title' field is required.")
def create_task(payload: Dict[str, Any]):
    title = payload.get("title")
    if not title or not str(title).strip():
        raise HTTPException(status_code=400, detail={"error": "Title is missing or empty"})
    
    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "title": str(title).strip(), "done": False}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", summary="Update a Task", description="Updates an existing task's title and/or done status.")
def update_task(task_id: int, payload: Dict[str, Any]):
    if not payload:
        raise HTTPException(status_code=400, detail={"error": "Invalid body"})

    for task in tasks:
        if task["id"] == task_id:
            if "title" in payload:
                title = payload["title"]
                if not title or not str(title).strip():
                    raise HTTPException(status_code=400, detail={"error": "Title cannot be empty"})
                task["title"] = str(title).strip()
            if "done" in payload:
                task["done"] = bool(payload["done"])
            return task
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Task", description="Deletes a task by its ID.")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})

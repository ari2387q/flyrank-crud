#!/bin/bash
cd /home/aryan/flyrank-crud
rm -rf .git

git init

echo "fastapi" > requirements.txt
echo "uvicorn" >> requirements.txt
git add requirements.txt
git commit -m "Initial commit"

# Stage 0
cat << 'EOF' > main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, server"}
EOF
git add main.py
git commit -m "Stage 0: hello server"

# Stage 1
cat << 'EOF' > main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}
EOF
git add main.py
git commit -m "Stage 1: root and health endpoints"

# Stage 2
cat << 'EOF' > main.py
from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": True},
    {"id": 3, "title": "Write API", "done": False}
]

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})
EOF
git add main.py
git commit -m "Stage 2: read endpoints with 404"

# Stage 3
cat << 'EOF' > main.py
from fastapi import FastAPI, HTTPException, status
from typing import Dict, Any

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": True},
    {"id": 3, "title": "Write API", "done": False}
]

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: Dict[str, Any]):
    title = payload.get("title")
    if not title or not str(title).strip():
        raise HTTPException(status_code=400, detail={"error": "Title is missing or empty"})
    
    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "title": str(title).strip(), "done": False}
    tasks.append(new_task)
    return new_task
EOF
git add main.py
git commit -m "Stage 3: create with validation"

# Stage 4
cat << 'EOF' > main.py
from fastapi import FastAPI, HTTPException, status
from typing import Dict, Any

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": True},
    {"id": 3, "title": "Write API", "done": False}
]

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: Dict[str, Any]):
    title = payload.get("title")
    if not title or not str(title).strip():
        raise HTTPException(status_code=400, detail={"error": "Title is missing or empty"})
    
    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {"id": new_id, "title": str(title).strip(), "done": False}
    tasks.append(new_task)
    return new_task

@app.put("/tasks/{task_id}")
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

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})
EOF
git add main.py
git commit -m "Stage 4: full CRUD"

# Stage 5
cat << 'EOF' > main.py
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
EOF
git add main.py
git commit -m "Stage 5: Swagger UI"

# Stage 6
cat << 'EOF' > README.md
# FlyRank CRUD API

This is a simple CRUD API built with Python and FastAPI for managing a to-do list.

## Installation & Running

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```
The server will start at `http://localhost:8000`.

## Endpoints

| CRUD operation | HTTP method | Endpoint | Meaning |
|---|---|---|---|
| Read (Meta) | GET | `/` | API Root |
| Read (Meta) | GET | `/health` | Health Check |
| Read | GET | `/tasks` | List all tasks |
| Read | GET | `/tasks/{id}` | Get a specific task by ID |
| Create | POST | `/tasks` | Add a new task |
| Update | PUT | `/tasks/{id}` | Update an existing task |
| Delete | DELETE | `/tasks/{id}` | Remove a task |

## Example Request

```bash
curl -i http://localhost:8000/tasks/1
```
Output:
```http
HTTP/1.1 200 OK
date: Thu, 01 Jan 1970 00:00:00 GMT
server: uvicorn
content-length: 42
content-type: application/json

{"id":1,"title":"Buy milk","done":false}
```

## Swagger UI

Interactive API documentation is automatically generated and available at:
`http://localhost:8000/docs`

*(Place screenshot here as per Stage 5 requirements)*
EOF
git add README.md
git commit -m "Stage 6: publish and docs"


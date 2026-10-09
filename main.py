from fastapi import FastAPI, HTTPException, status
from typing import Dict, Any
import sqlite3

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API for managing tasks."
)

DB_FILE = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL CHECK (done IN (0, 1))
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM tasks")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", [
            ("Buy milk", 0),
            ("Learn FastAPI", 1),
            ("Write API", 0)
        ])
    conn.commit()
    conn.close()

init_db()

@app.get("/", summary="API Root")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", summary="List Tasks")
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row["id"], "title": row["title"], "done": bool(row["done"])} for row in rows]

@app.get("/tasks/{task_id}", summary="Get a Task")
def get_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a Task")
def create_task(payload: Dict[str, Any]):
    title = payload.get("title")
    if not title or not str(title).strip():
        raise HTTPException(status_code=400, detail={"error": "Title is missing or empty"})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (str(title).strip(), 0))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return {"id": new_id, "title": str(title).strip(), "done": False}

@app.put("/tasks/{task_id}", summary="Update a Task")
def update_task(task_id: int, payload: Dict[str, Any]):
    if not payload:
        raise HTTPException(status_code=400, detail={"error": "Invalid body"})

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
        
    new_title = row["title"]
    new_done = row["done"]

    if "title" in payload:
        if not payload["title"] or not str(payload["title"]).strip():
            conn.close()
            raise HTTPException(status_code=400, detail={"error": "Title cannot be empty"})
        new_title = str(payload["title"]).strip()
        
    if "done" in payload:
        new_done = 1 if payload["done"] else 0
        
    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?", 
        (new_title, new_done, task_id)
    )
    conn.commit()
    conn.close()
    
    return {"id": task_id, "title": new_title, "done": bool(new_done)}

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Task")
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
        
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return

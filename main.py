from fastapi import FastAPI, HTTPException, status
from typing import Dict, Any
import sqlite3
import os

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

# Memory list is still here for unmigrated endpoints temporarily
tasks = [] 

@app.get("/", summary="API Root")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: Dict[str, Any]):
    return {}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: Dict[str, Any]):
    return {}

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    return

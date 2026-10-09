from fastapi import FastAPI, HTTPException, status
from typing import Dict, Any
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API for managing tasks, backed by PostgreSQL."
)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM tasks")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            [("Buy milk", False), ("Learn FastAPI", True), ("Write API", False)]
        )
    conn.commit()
    cursor.close()
    conn.close()

init_db()

def row_to_dict(row, cursor):
    cols = [desc[0] for desc in cursor.description]
    return dict(zip(cols, row))

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
    result = [row_to_dict(row, cursor) for row in rows]
    cursor.close()
    conn.close()
    return result

@app.get("/tasks/{task_id}", summary="Get a Task")
def get_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    result = row_to_dict(row, cursor)
    cursor.close()
    conn.close()
    return result

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a Task")
def create_task(payload: Dict[str, Any]):
    title = payload.get("title")
    if not title or not str(title).strip():
        raise HTTPException(status_code=400, detail={"error": "Title is missing or empty"})
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *",
        (str(title).strip(), False)
    )
    row = cursor.fetchone()
    result = row_to_dict(row, cursor)
    conn.commit()
    cursor.close()
    conn.close()
    return result

@app.put("/tasks/{task_id}", summary="Update a Task")
def update_task(task_id: int, payload: Dict[str, Any]):
    if not payload:
        raise HTTPException(status_code=400, detail={"error": "Invalid body"})
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    current = row_to_dict(row, cursor)
    new_title = current["title"]
    new_done = current["done"]
    if "title" in payload:
        if not payload["title"] or not str(payload["title"]).strip():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail={"error": "Title cannot be empty"})
        new_title = str(payload["title"]).strip()
    if "done" in payload:
        new_done = bool(payload["done"])
    cursor.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *",
        (new_title, new_done, task_id)
    )
    row = cursor.fetchone()
    result = row_to_dict(row, cursor)
    conn.commit()
    cursor.close()
    conn.close()
    return result

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a Task")
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE id = %s", (task_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()

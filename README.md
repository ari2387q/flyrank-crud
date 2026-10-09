# FlyRank CRUD API with SQLite

This is a simple CRUD API built with Python and FastAPI for managing a to-do list.

## Why SQLite?
SQLite was chosen because it is a lightweight, file-based database that requires zero configuration or server setup. It allows data to persist across server restarts while remaining simple enough to embed directly into the application.

## Database Storage
The database is stored locally in a single file called `tasks.db` within the project root directory.

## Installation & Running

```bash
# Setup virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the server (database is created automatically on first run)
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

## Example SQL Query
To list all completed tasks, you can run this SQL query directly in a SQLite viewer:
```sql
SELECT * FROM tasks WHERE done = 1;
```

## Database Viewer
![Database Viewer](db-viewer.png)

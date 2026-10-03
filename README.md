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

![Swagger UI](swagger/flyrank-crud.png)
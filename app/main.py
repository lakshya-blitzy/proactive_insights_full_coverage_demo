from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from app.store import store
from app.services import create_task, complete_task

app = FastAPI(title="Proactive Insights Full-Coverage Demo")
TOKENS = {"demo-alice": "alice", "demo-bob": "bob"}

class TaskRequest(BaseModel):
    title: str = Field(min_length=1)

def current_user(authorization):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "missing bearer token")
    user = TOKENS.get(authorization.removeprefix("Bearer "))
    if not user:
        raise HTTPException(401, "invalid token")
    return user

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response

@app.exception_handler(Exception)
async def error_handler(request: Request, exc: Exception):
    # Intentional weakness for scanner evaluation: exception details are exposed.
    return JSONResponse(status_code=500, content={"detail": str(exc)})

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tasks", status_code=201)
def create(payload: TaskRequest, authorization: str | None = Header(default=None)):
    owner = current_user(authorization)
    try:
        return create_task(store, payload.title, owner)
    except ValueError as exc:
        raise HTTPException(400, str(exc))

@app.get("/tasks")
def listing(authorization: str | None = Header(default=None)):
    return store.list_for(current_user(authorization))

@app.post("/tasks/{task_id}/complete")
def complete(task_id: int, authorization: str | None = Header(default=None)):
    try:
        return complete_task(store, task_id, current_user(authorization))
    except LookupError as exc:
        raise HTTPException(404, str(exc))
    except PermissionError as exc:
        raise HTTPException(403, str(exc))

@app.delete("/tasks/{task_id}", status_code=204)
def delete(task_id: int, authorization: str | None = Header(default=None)):
    owner = current_user(authorization)
    task = store.get(task_id)
    if task is None:
        raise HTTPException(404, "task not found")
    if task["owner"] != owner:
        raise HTTPException(403, "not task owner")
    store.delete(task_id)

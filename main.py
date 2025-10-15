from datetime import datetime
from fastapi import FastAPI, HTTPException
from uuid import uuid4
from pydantic import Field, BaseModel
'''Pydantic provides typed models for robust data validation and serialization.
 It parses incoming data into Python types, enforces constraints, produces clear
  error messages, and can generate JSON Schema/OpenAPI for APIs. With fast 
  validation powered by pydantic-core and 
  simple .model_dump()/.model_dump_json() serialization, it keeps data models 
  as a single, maintainable source of truth.'''
app = FastAPI()


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)


class Task(BaseModel):
    id: str
    title: str
    is_done: bool
    created_at: datetime
    last_updated_at: datetime

TASKS: dict[str, Task] = {}

@app.get(path="/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post(path="/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    task = Task(
        id=str(uuid4()),
        title=payload.title,
        is_done=False,
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
    )
    TASKS[task.id] = task
    return task
'''Purpose: Stores the newly created Task in an in-memory dictionary.

How it works: Uses the task’s unique id as the key and the task object as the value: TASKS[task.id] = task.

Impact: Enables quick lookup, update, and deletion by id during the app’s lifetime (not persisted; cleared on restart).'''
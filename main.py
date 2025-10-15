from datetime import datetime
from os import path
from typing import Optional
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

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(min_length=1, max_length=200, default=None)
    is_done: Optional[bool] = None

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

@app.get(path="/tasks", response_model=list[Task])
def list_tasks():
    return list(TASKS.values())

@app.delete(path="/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")
    del TASKS[task_id]

@app.patch(path="/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskUpdate):
    task = TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = task.model_copy(update={
        "title": payload.title if payload.title is not None else task.title,
        "is_done": payload.is_done if payload.is_done is not None else task.is_done,
        "last_updated_at": datetime.now(),
    })
    TASKS[task_id] = updated
    return updated
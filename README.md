# Task App API Design

## Problem Statement
 I need some way to create tasks and track my completion.


## Scope
- Create tasks
- Delete tasks
- Mark tasks as complete
- View all available tasks


## API Endpoints
- **POST** `/tasks` — Create a new task
- **GET** `/tasks` — List all tasks
- **GET** `/tasks/{id}` — Get a task by ID
- **PATCH** `/tasks/{id}` — Update a task (mark as complete or update title)
- **DELETE** `/tasks/{id}` — Delete a task


## Data Model

| Field          | Type         | Description            |
|----------------|--------------|------------------------|
| id             | string (UUID)| Unique identifier      |
| task_name      | string       | Task provided by user  |
| is_done        | boolean      | Completion status      |
| created_at     | datetime     | When task was created  |
| last_updated_at| datetime     | When last updated      |

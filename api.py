from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database

app = FastAPI()
database.create_table()


# ----------------مدل های وردی ----------------

class TaskCreate(BaseModel):
    title: str

    # ------------------  endpoint -----------------

@app.get("/tasks")
def list_tasks():
    rows = database.get_all_tasks()
    tasks = []
    for row in rows:
        task_id, title, done = row
        tasks.append({
            "id": task_id,
            "title": title,
            "done": bool(done)
        })
    return tasks

@app.post("/tasks")
def create_task(payload: TaskCreate):
    database.add_task(payload.title)
    return {
        "message": "Task created",
        "title": payload.title
    }

@app.patch("/tasks/{task_id}/done")
def mark_task_done(task_id: int):
    rows = database.get_all_tasks()
    ids = [row[0] for row in rows]

    if task_id not in ids:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found"
        )

    database.mark_done(task_id)
    return {
        "message": "Task marked as done",
        "id": task_id
    }


@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    rows = database.get_all_tasks()
    ids = [row[0] for row in rows]

    if task_id not in ids:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found"
        )
    database.delete_task(task_id)
    return {
        "message": "Task deleted",
        "id": task_id
    }
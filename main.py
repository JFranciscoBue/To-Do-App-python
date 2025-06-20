from fastapi import FastAPI, HTTPException
from models import Task
from typing import Dict, List, Union


app = FastAPI()

tasks: List[Task] = []


@app.get("/all")
async def get_all_tasks():
    return tasks


@app.get("/{id}")
async def get_one_task(id: int):
    for task in tasks:
        if task.id == id:
            return task

    raise HTTPException(status_code=404, detail="Task does not exist")


@app.post("/new")
async def create_task(task: Task) -> Dict[str, Union[bool, Task]]:
    last_id = max([t.id for t in tasks], default=0)
    new_task = Task(
        id=last_id + 1,
        title=task.title,
        description=task.description,
        is_done=task.is_done,
    )
    tasks.append(new_task)
    return {"success": True, "task": new_task}


@app.delete("/delete/{task_id}")
async def delete_task(task_id: int) -> Dict[str, Union[bool, str]]:
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"success": True, "message": "Task Deleted"}

    raise HTTPException(status_code=404, detail="Task not found")

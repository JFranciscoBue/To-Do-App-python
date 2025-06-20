from fastapi import FastAPI, HTTPException
from typing import Dict, List, Union
from models import Task
from helpers import sort_by_id


app = FastAPI()

tasks: List[Task] = []


def find_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    return None


@app.get("/")
async def root():
    return {"message": "Welcome to your Manage Task App"}


@app.get("/tasks/all")
async def get_all_tasks():
    return sorted(tasks, key=sort_by_id)


@app.get("/tasks/{id}")
async def get_one_task(id: int):
    task = find_task(id)
    if task:
        return task

    raise HTTPException(status_code=404, detail="Task does not exist")


@app.post("/tasks/new", status_code=201)
async def create_task(task: Task) -> Dict[str, Union[bool, Task]]:
    last_id = max([t.id for t in tasks if t.id is not None], default=0)
    new_task = Task(
        id=last_id + 1,
        title=task.title,
        description=task.description,
        is_done=task.is_done,
    )
    tasks.append(new_task)
    return {"success": True, "task": new_task}


@app.put("/tasks/update/{task_id}")
async def update_task(task_id: int, new_task_info: Task) -> Dict[str, Union[bool, str]]:
    task = find_task(task_id)

    if task:
        tasks.remove(task)
        tasks.append(
            Task(
                id=task.id,
                title=new_task_info.title,
                description=new_task_info.description,
                is_done=new_task_info.is_done,
            )
        )
        return {"success": True, "message": "Task updated"}

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/delete/{task_id}")
async def delete_task(task_id: int) -> Dict[str, Union[bool, str]]:
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"success": True, "message": "Task Deleted"}

    raise HTTPException(status_code=404, detail="Task not found")

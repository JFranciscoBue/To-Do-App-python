from models import Task


def sort_by_id(task: Task) -> int:
    return task.id if task.id is not None else 0

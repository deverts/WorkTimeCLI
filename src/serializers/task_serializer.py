from datetime import datetime

from entities import Task

TASK_ID_COLUMN = "task_id"
TASK_CREATED_COLUMN = "created"
TASK_CREATED_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def task_to_dict(task: Task) -> dict:
    return {TASK_ID_COLUMN: task.id, TASK_CREATED_COLUMN: task.created}


def json_to_task(input_json: dict) -> Task:
    return Task(
        input_json[TASK_ID_COLUMN],
        datetime.strptime(input_json[TASK_CREATED_COLUMN], TASK_CREATED_FORMAT),
    )

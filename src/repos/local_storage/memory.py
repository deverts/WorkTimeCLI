from typing import NoReturn
from datetime import datetime

from .interface import LocalStorageInterface
from .exceptions import TaskAlreadyExists, TaskDoesNotExist

from serializers import task_serializer
from entities import Task


class MemoryLocalStorage(LocalStorageInterface):
    DB = []

    def __init__(self):
        # This is here to prevent any re-use between
        # tests. We've seen cases in the past where
        # self.DB was not re-initialised as blank.
        self.DB = []

    def start_tracking(self, task_id: str) -> NoReturn:
        results = [x for x in self.DB if x[task_serializer.TASK_ID_COLUMN] == task_id]

        if results:
            raise TaskAlreadyExists("task is already tracking")

        self.DB.append(
            {
                task_serializer.TASK_ID_COLUMN: task_id,
                task_serializer.TASK_CREATED_COLUMN: str(datetime.now()),
            }
        )

    def stop_tracking(self, task_id: str) -> int:
        task = self.get_task(task_id)

        self.remove_task(task_id)

        result_time_spent = round((datetime.now() - task.created).total_seconds())

        return result_time_spent

    def get_task(self, task_id: str) -> Task:
        results = [x for x in self.DB if x[task_serializer.TASK_ID_COLUMN] == task_id]
        if not results:
            raise TaskDoesNotExist("task was not tracking")
        elif len(results) != 1:
            raise TaskDoesNotExist(
                "multiple tasks with the same ID exist, please check the db"
            )

        result = results[0]

        return task_serializer.json_to_task(result)

    def remove_task(self, task_id: str) -> NoReturn:
        for item in self.DB:
            if item[task_serializer.TASK_ID_COLUMN] == task_id:
                self.DB.remove(item)

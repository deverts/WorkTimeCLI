from typing import NoReturn
from datetime import datetime

from .interface import LocalStorageInterface
from .exceptions import TaskAlreadyExists, TaskDoesNotExist

import config
from entities import Task
from serializers import task_serializer

from tinydb import TinyDB, Query


class FileLocalStorage(LocalStorageInterface):
    @staticmethod
    def _get_db() -> TinyDB:
        return TinyDB(config.LOCAL_DB_PATH)

    def start_tracking(self, task_id: str) -> NoReturn:
        db = self._get_db()

        # check if it exists first, fail neatly if so.
        # if it doesn't exist, we can safely insert it.
        task_query = Query()
        results = db.search(task_query.task_id == task_id)
        if results:
            raise TaskAlreadyExists("task is already tracking")

        db.insert(
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
        db = self._get_db()

        task_query = Query()

        # check, does it exist
        # if so -> remove it + return the time diff
        # if not -> raise exception
        results = db.search(task_query.task_id == task_id)
        if not results:
            raise TaskDoesNotExist("task was not tracking")
        elif len(results) != 1:
            raise TaskDoesNotExist(
                "multiple tasks with the same ID exist, please check the db"
            )

        result = results[0]

        return task_serializer.json_to_task(result)

    def remove_task(self, task_id: str) -> NoReturn:
        db = self._get_db()

        task_query = Query()

        db.remove(task_query.task_id)

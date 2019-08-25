from typing import NoReturn

from .exceptions import RemoteTaskNotFound
from .interface import TaskTrackerInterface

import config
from entities import TaskTrackerTask

from asana import Client
from asana.error import NotFoundError


def seconds_to_hours(input_seconds: int) -> float:
    try:
        return input_seconds / 60.0 / 60.0
    except ZeroDivisionError:
        return 0.0


class AsanaTaskTracker(TaskTrackerInterface):
    @staticmethod
    def _get_client() -> Client:
        client = Client.access_token(config.ASANA_CREDENTIALS.token)
        return client

    def sync_time(self, task_id: str, time_spent: int) -> NoReturn:
        client = self._get_client()

        task = self.get_task(task_id)
        new_time_spent = seconds_to_hours(time_spent)

        client.tasks.update(
            task_id,
            {
                "custom_fields": {
                    config.ASANA_CREDENTIALS.time_taken_field_id: task.time_spent
                    + new_time_spent
                }
            },
        )

    def get_task(self, task_id: str) -> TaskTrackerTask:
        client = self._get_client()

        try:
            remote_task = client.tasks.find_by_id(task_id)
        except NotFoundError:
            raise RemoteTaskNotFound

        task = TaskTrackerTask(task_id, remote_task["name"], 0.0)

        for field in remote_task["custom_fields"]:
            if field["gid"] == config.ASANA_CREDENTIALS.time_taken_field_id:
                task.time_spent = float(field["number_value"])

        return task

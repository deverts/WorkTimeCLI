from typing import NoReturn, List
from datetime import datetime, timedelta

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

    def list_tasks(self) -> List[TaskTrackerTask]:
        client = self._get_client()

        # get all tasks assigned to me. we do the completed_since call
        # since we only want to get incomplete tasks
        currently_assigned_tasks = client.tasks.find_by_user_task_list(
            config.ASANA_CREDENTIALS.user_id, params={
                "completed_since": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%S.000")
            }
        )

        tasks = []

        for task in currently_assigned_tasks:
            tasks.append(
                TaskTrackerTask(task['id'], task['name'], 0.0)
            )

        return tasks

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

        # This suppresses a warning from the Asana API that they're moving to string based IDs
        # it's not an issue for us.
        client.headers.update({"Asana-Enable": "string_ids,new_sections"})

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

    def _asana_dict_to_tasktrackertask(self, task_dict: dict) -> TaskTrackerTask:
        time_spent = 0.0

        for field in task_dict.get("custom_fields", []):
            if field["gid"] == config.ASANA_CREDENTIALS.time_taken_field_id:
                try:
                    time_spent = float(field["number_value"])
                except TypeError:
                    time_spent = 0.0

        task = TaskTrackerTask(
            task_dict.get("gid", None),
            task_dict.get("name", None),
            task_dict.get("assignee", {}).get("name", None),
            task_dict.get("due_on", None),
            task_dict.get("completed", False),
            task_dict.get("notes", None),
            time_spent
        )

        # We do it like this because Asana will often return the key
        # but with a blank value instead of omitting the key.
        if not task.id:
            task.id = "No ID"

        if not task.name:
            task.name = "No name"

        if not task.assigned_to:
            task.assigned_to = "Unassigned"

        if not task.due:
            task.due = "No due date"

        if not task.description:
            task.description = "No description"

        return task

    def get_task(self, task_id: str) -> TaskTrackerTask:
        client = self._get_client()

        try:
            remote_task = client.tasks.find_by_id(task_id)
        except NotFoundError:
            raise RemoteTaskNotFound

        task = self._asana_dict_to_tasktrackertask(remote_task)

        return task

    def list_tasks(self) -> List[TaskTrackerTask]:
        client = self._get_client()

        # get all tasks assigned to me. we do the completed_since call
        # since we only want to get incomplete tasks
        currently_assigned_tasks = client.tasks.find_by_user_task_list(
            config.ASANA_CREDENTIALS.user_id, params={
                "completed_since": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%S.000")
            },
            opt_fields="gid,name,memberships,due_on"
        )

        tasks = []

        for task in currently_assigned_tasks:
            # TODO: I don't 100% understand this, but to filter out "sections" from your list
            # you can check the `memberships` key. If the item has no memberships, it's
            # likely a section. I'm not confident on this one. We can probably also do
            # something with grabbing just tasks for this week etc.
            if len(task['memberships']) == 0:
                continue

            tasks.append(self._asana_dict_to_tasktrackertask(task))

        return tasks

    def complete_task(self, task_id: str) -> NoReturn:
        client = self._get_client()

        client.tasks.update(
            task_id,
            {
                "completed": True
            },
        )

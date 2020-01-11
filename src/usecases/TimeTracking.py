from typing import NoReturn, List

from entities import TaskTrackerTask
from repos.local_storage.exceptions import TaskDoesNotExist
from repos.local_storage.interface import LocalStorageInterface
from repos.task_tracker.interface import TaskTrackerInterface


class TimeTracking:
    def __init__(
        self, task_tracker: TaskTrackerInterface, local_storage: LocalStorageInterface
    ):
        self.task_tracker = task_tracker
        self.local_storage = local_storage

    def start_tracking(self, task_id: str) -> NoReturn:
        # check that the task exists before starting the test.
        # if it doesn't throw an error, it's likely not a problem.
        self.task_tracker.get_task(task_id)

        self.local_storage.start_tracking(task_id)

    def stop_tracking(self, task_id: str) -> NoReturn:
        time_taken = self.local_storage.stop_tracking(task_id)
        self.task_tracker.sync_time(task_id, time_taken)

    def list_tasks(self) -> List[TaskTrackerTask]:
        tasks = self.task_tracker.list_tasks()

        return tasks

    def complete_task(self, task_id: str) -> NoReturn:
        # check that it exists first
        task = self.task_tracker.get_task(task_id)

        time_taken = 0

        # check if the task is being tracked locally first
        # close it off if so.
        try:
            time_taken = self.local_storage.stop_tracking(task_id)
        except TaskDoesNotExist:
            # This means we've not been tracking time for it already
            pass

        self.task_tracker.sync_time(task_id, time_taken)
        self.task_tracker.complete_task(task_id)

    def read_task(self, task_id: str) -> TaskTrackerTask:
        return self.task_tracker.get_task(task_id)

    def list_tracking(self) -> List[TaskTrackerTask]:
        return []
from typing import NoReturn, List

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

    def list_tasks(self) -> NoReturn:
        tasks = self.task_tracker.list_tasks()

        # output = []

        for c, task in enumerate(tasks):
            print(f"{c+1} / {len(tasks)}: {task.name} ({task.id})")
            # output.append(f"{task.id}: {task.name}")

        # return output

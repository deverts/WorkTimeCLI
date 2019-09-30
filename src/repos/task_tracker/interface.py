from typing import NoReturn, List
from abc import ABC, abstractmethod

from entities import TaskTrackerTask


class TaskTrackerInterface(ABC):
    @abstractmethod
    def sync_time(self, task_id: str, time_spent: int) -> NoReturn:
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> TaskTrackerTask:
        pass

    @abstractmethod
    def list_tasks(self) -> List[TaskTrackerTask]:
        pass
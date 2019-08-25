from abc import ABC, abstractmethod
from typing import NoReturn

from entities import Task


class LocalStorageInterface(ABC):
    @abstractmethod
    def start_tracking(self, task_id: str) -> NoReturn:
        pass

    @abstractmethod
    def stop_tracking(self, task_id: str) -> int:
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Task:
        pass

    @abstractmethod
    def remove_task(self, task_id: str) -> NoReturn:
        pass

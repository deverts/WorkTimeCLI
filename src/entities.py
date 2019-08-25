from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    id: str
    created: datetime


@dataclass
class TaskTrackerTask:
    id: str
    name: str
    time_spent: float

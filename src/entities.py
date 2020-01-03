from dataclasses import dataclass
from datetime import datetime


# Task represents our internally stored version of a task.
# This is something that you're tracking time for right now
# We don't store any other metadata on it other than it's ID
# since this data can update in the remote system. What this means
# is that we need several extra API calls to render some data, but
# it means that we have one source of truth for things like task
# titles etc
@dataclass
class Task:
    id: str
    created: datetime


# This represents the data we require from any remote task tracking
# system.
@dataclass
class TaskTrackerTask:
    id: str
    name: str
    assigned_to: str
    due: datetime
    complete: bool
    description: str
    time_spent: float

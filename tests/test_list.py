import pytest
from datetime import datetime
from unittest.mock import Mock

from entities import TaskTrackerTask
from repos.factories import get_local_storage
from usecases.TimeTracking import TimeTracking


def test_list_tasks():
    OUTPUT = [
        TaskTrackerTask(id="0", name="Test 0", assigned_to="", due=datetime.now(), complete=False, description="", time_spent=0.0),
        TaskTrackerTask(id="1", name="Test 1", assigned_to="", due=datetime.now(), complete=False, description="", time_spent=0.0),
        TaskTrackerTask(id="2", name="Test 2", assigned_to="", due=datetime.now(), complete=False, description="", time_spent=0.0)
    ]

    def list_tasks():
        return OUTPUT

    task_tracker = Mock()
    local_storage = get_local_storage()()

    usecase = TimeTracking(task_tracker, local_storage)
    usecase.task_tracker.list_tasks.side_effect = list_tasks

    output = usecase.list_tasks()

    assert usecase.task_tracker.list_tasks.called_once()

    assert output == OUTPUT

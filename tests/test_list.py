import pytest
from unittest.mock import Mock

from entities import TaskTrackerTask
from repos.factories import get_local_storage
from usecases.TimeTracking import TimeTracking


def test_list_tasks():
    def list_tasks():
        return [
            TaskTrackerTask(id="0", name="Test 0", time_spent=0.0),
            TaskTrackerTask(id="1", name="Test 1", time_spent=0.0),
            TaskTrackerTask(id="2", name="Test 2", time_spent=0.0)
        ]

    task_tracker = Mock()
    local_storage = get_local_storage()()

    usecase = TimeTracking(task_tracker, local_storage)
    usecase.task_tracker.list_tasks.side_effect = list_tasks

    output = usecase.list_tasks()

    assert usecase.task_tracker.list_tasks.called_once()
    assert output == [
        "0: Test 0",
        "1: Test 1",
        "2: Test 2"
    ]

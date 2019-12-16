import pytest
from unittest.mock import Mock, call

from repos.factories import get_local_storage
from repos.local_storage.exceptions import TaskDoesNotExist
from repos.task_tracker.exceptions import RemoteTaskNotFound
from usecases.TimeTracking import TimeTracking


def test_complete_for_invalid_task():
    def raise_exc(n):
        raise RemoteTaskNotFound()

    task_id = "000000"

    usecase = TimeTracking(Mock(), Mock())

    # We need to check that it's still valid first
    usecase.task_tracker.get_task.side_effect = raise_exc

    with pytest.raises(RemoteTaskNotFound):
        usecase.complete_task(task_id)


def test_complete_runs():
    task_tracker = Mock()
    local_storage = Mock()

    usecase = TimeTracking(task_tracker, local_storage)

    task_id = "000000"
    usecase.complete_task(task_id)

    # Fix me! This isn't passing
    assert usecase.task_tracker.complete_task.called_with(task_id)


# Here, we want to set up us tracking a task. If you mark
# a task as complete, we should close out our local tasks
# sync the time, then mark it done in the remote task tracker.
def test_complete_closes_locally_running_task_if_exists():
    task_id = "000000"

    task_tracker = Mock()
    local_storage = get_local_storage()()

    usecase = TimeTracking(task_tracker, local_storage)

    usecase.start_tracking(task_id)

    usecase.complete_task(task_id)

    # check that the task is now actually stopped
    with pytest.raises(TaskDoesNotExist):
        usecase.stop_tracking(task_id)

    assert usecase.task_tracker.sync_time.called_once_with(task_id, 0)

    # Check complete task is called after
    assert usecase.task_tracker.complete_task.called_once_with(task_id)

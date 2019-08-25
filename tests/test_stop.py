import pytest
from unittest.mock import Mock

from repos.local_storage.exceptions import TaskAlreadyExists, TaskDoesNotExist
from repos.factories import get_local_storage
from entities import Task
from serializers import task_serializer
from repos.task_tracker.exceptions import RemoteTaskNotFound
from usecases.TimeTracking import TimeTracking


def test_stop_should_stop_tracking():
    task_id = "1000000"

    # create mocks
    task_tracker = Mock()
    local_storage = get_local_storage()()

    usecase = TimeTracking(task_tracker, local_storage)

    usecase.start_tracking(task_id)
    usecase.stop_tracking(task_id)

    with pytest.raises(TaskDoesNotExist):
        usecase.local_storage.get_task(task_id)


def test_stop_should_sync_tracking_with_remote():
    task_id = "1000000"

    # create mocks
    task_tracker = Mock()
    local_storage = get_local_storage()()

    usecase = TimeTracking(task_tracker, local_storage)

    usecase.start_tracking(task_id)
    usecase.stop_tracking(task_id)

    # check that there's been no errors, and the time
    # sync was called to asana.
    assert usecase.task_tracker.sync_time.called_once()


def test_stop_should_throw_an_error_if_sync_to_remote_fails():
    # TODO: ...
    pass


def test_stop_should_throw_error_for_task_that_no_longer_exist():
    def raise_exc(n, m):
        raise RemoteTaskNotFound

    task_id = "1000000"

    # create mocks
    task_tracker = Mock()
    local_storage = get_local_storage()()

    usecase = TimeTracking(task_tracker, local_storage)

    usecase.start_tracking(task_id)

    # simulate the task no longer existing.
    # this error would be thrown by get_task
    usecase.task_tracker.sync_time.side_effect = raise_exc

    with pytest.raises(RemoteTaskNotFound):
        usecase.stop_tracking(task_id)


def test_stop_should_throw_error_for_task_not_being_tracked():
    task_id = "1000000"

    # create mocks
    task_tracker = Mock()
    local_storage = get_local_storage()()

    usecase = TimeTracking(task_tracker, local_storage)

    with pytest.raises(TaskDoesNotExist):
        usecase.stop_tracking(task_id)

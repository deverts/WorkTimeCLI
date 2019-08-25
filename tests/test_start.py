from datetime import datetime

import pytest
from unittest.mock import Mock

from repos.factories import get_local_storage
from repos.task_tracker.exceptions import RemoteTaskNotFound
from repos.local_storage.exceptions import TaskAlreadyExists
from usecases.TimeTracking import TimeTracking

from entities import Task
from serializers import task_serializer


def test_start_should_start_tracking():
    task_id = "1000000"

    # create mocks
    task_tracker = Mock()
    local_storage = get_local_storage()()

    usecase = TimeTracking(task_tracker, local_storage)

    usecase.start_tracking(task_id)

    # Is Asana checked for validity?
    assert usecase.task_tracker.get_task.called_once()

    # Is the data stored? I.e. was it actually written somewhere
    task = usecase.local_storage.get_task(task_id)

    assert task.id == task_id


def test_start_should_throw_error_for_invalid_remote_task_id():
    def raise_exc(n):
        raise RemoteTaskNotFound

    task_id = "1000000"

    # create mocks
    task_tracker = Mock()
    local_storage = get_local_storage()()

    usecase = TimeTracking(task_tracker, local_storage)

    # set task tracker to respond badly to one of the task IDs
    usecase.task_tracker.get_task.side_effect = raise_exc

    # check that the exception is thrown
    with pytest.raises(RemoteTaskNotFound):
        usecase.start_tracking(task_id)


def test_start_should_throw_error_for_task_we_are_already_tracking():
    task_id = "1000000"

    # create mocks
    task_tracker = Mock()
    local_storage = get_local_storage()()

    usecase = TimeTracking(task_tracker, local_storage)

    task = Task(task_id, datetime.now())

    # This is a testing only method.
    usecase.local_storage.DB.append(task_serializer.task_to_dict(task))

    # check that local storage is checked and causes an error
    with pytest.raises(TaskAlreadyExists):
        usecase.start_tracking(task_id)

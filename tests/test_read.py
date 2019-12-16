import pytest
from unittest.mock import Mock

from usecases.TimeTracking import TimeTracking
from repos.task_tracker.exceptions import RemoteTaskNotFound

# We're just checking that the right underlying
# functions are called and the appropriate exceptions
# are bubbled up.


def test_read_task_with_invalid_task_id():
    def raise_exc(n):
        raise RemoteTaskNotFound

    bad_task_id = "000000"

    task_tracker = Mock()
    local_storage = Mock()

    usecase = TimeTracking(task_tracker, local_storage)

    usecase.task_tracker.get_task.side_effect = raise_exc

    with pytest.raises(RemoteTaskNotFound):
        usecase.read_task(bad_task_id)


def test_read_task():
    def basic_string(n):
        return "Hello world"

    task_id = "00000"

    usecase = TimeTracking(Mock(), Mock())

    usecase.task_tracker.get_task.side_effect = basic_string

    assert usecase.read_task(task_id) == "Hello world"

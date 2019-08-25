import sys
from typing import Type

from .local_storage.interface import LocalStorageInterface
from .local_storage.file import FileLocalStorage
from .local_storage.memory import MemoryLocalStorage


def get_local_storage() -> Type[LocalStorageInterface]:
    if "pytest" in sys.modules:
        return MemoryLocalStorage

    return FileLocalStorage

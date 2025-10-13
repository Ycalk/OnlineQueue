from functools import wraps
from logging import getLogger
from typing import TypeVar

T = TypeVar("T")


def with_logger(cls: type[T]) -> type[T]:
    original_init = cls.__init__

    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        self._logger = getLogger(f"{cls.__module__}.{cls.__name__}")
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls

from abc import ABC, abstractmethod
from datetime import timedelta
from typing import ClassVar

from .use_case import ApplicationUseCase


class Task(ApplicationUseCase, ABC):
    interval: ClassVar[timedelta] = timedelta(minutes=1)

    @abstractmethod
    async def __call__(self): ...

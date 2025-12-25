from abc import ABC, abstractmethod
from datetime import timedelta
from typing import ClassVar


class Task(ABC):
    interval: ClassVar[timedelta] = timedelta(minutes=1)

    @abstractmethod
    async def __call__(self): ...

from abc import abstractmethod
from typing import TypeVar, Protocol

from event_processor.events.base import BaseEvent

TEvent = TypeVar("TEvent", bound=BaseEvent)


class BaseEventHandler(Protocol[TEvent]):
    async def __call__(self, event: TEvent) -> None: ...

    @classmethod
    @abstractmethod
    def event_type(cls) -> type[TEvent]: ...

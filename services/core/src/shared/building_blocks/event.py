from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Protocol, ClassVar, TypeVar
from datetime import datetime


class DomainEvent(ABC, BaseModel):
    name: ClassVar[str]
    occurred_at: datetime = Field(default_factory=datetime.now, init=False)


class IEventPublisher(Protocol):
    async def publish(self, event: DomainEvent) -> None: ...


TEvent = TypeVar("TEvent", bound=DomainEvent)


class IEventHandler(Protocol[TEvent]):
    async def __call__(self, event: TEvent) -> None: ...

    @classmethod
    @abstractmethod
    def event_type(cls) -> type[TEvent]: ...


class IEventProcessor(Protocol):
    async def register_handler(self, handler: type[IEventHandler[TEvent]]) -> None: ...

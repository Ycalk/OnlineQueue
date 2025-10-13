from abc import ABC
from pydantic import BaseModel
from typing import Protocol


class DomainEvent(ABC, BaseModel): ...


class IEventPublisher(Protocol):
    async def publish(self, event: DomainEvent) -> None: ...

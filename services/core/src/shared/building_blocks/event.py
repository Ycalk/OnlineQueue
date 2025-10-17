from abc import ABC
from pydantic import BaseModel, Field
from typing import Protocol
from datetime import datetime


class DomainEvent(ABC, BaseModel):
    occurred_at: datetime = Field(default_factory=datetime.now, init=False)


class IEventPublisher(Protocol):
    async def publish(self, event: DomainEvent) -> None: ...

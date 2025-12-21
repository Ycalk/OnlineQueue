from uuid import UUID
from typing import ClassVar

from .base import BaseEvent


class QueueCreated(BaseEvent):
    name: ClassVar[str] = "queue.created"

    queue_id: UUID
    owner_id: UUID
    queue_name: str

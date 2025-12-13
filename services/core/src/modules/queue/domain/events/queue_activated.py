from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class QueueActivated(DomainEvent):
    name: ClassVar[str] = "queue.activated"

    queue_id: UUID

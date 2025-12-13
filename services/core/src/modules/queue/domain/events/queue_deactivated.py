from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class QueueDeactivated(DomainEvent):
    name: ClassVar[str] = "queue.deactivated"

    queue_id: UUID

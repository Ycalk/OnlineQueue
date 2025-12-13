from uuid import UUID
from datetime import time
from typing import ClassVar

from shared.building_blocks import DomainEvent


class QueueCreated(DomainEvent):
    name: ClassVar[str] = "queue.created"

    queue_id: UUID
    owner_id: UUID
    queue_name: str
    description: str | None
    cleanup_period_days: int

    reception_time_start: time
    reception_time_end: time

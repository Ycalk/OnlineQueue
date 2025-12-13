from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class QueueCleanedUp(DomainEvent):
    name: ClassVar[str] = "queue.cleaned_up"

    queue_id: UUID

from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class DescriptionChanged(DomainEvent):
    name: ClassVar[str] = "queue.description_changed"

    queue_id: UUID
    old_description: str | None
    new_description: str | None

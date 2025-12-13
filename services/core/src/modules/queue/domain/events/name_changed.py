from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class NameChanged(DomainEvent):
    name: ClassVar[str] = "queue.name_changed"

    queue_id: UUID
    old_name: str
    new_name: str

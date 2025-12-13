from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import (
    RequestPriority,
)


class RequestChangedPriority(DomainEvent):
    name: ClassVar[str] = "request.changed_priority"

    request_id: UUID
    new_priority: RequestPriority

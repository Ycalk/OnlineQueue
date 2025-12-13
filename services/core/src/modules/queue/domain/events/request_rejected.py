from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class RequestRejected(DomainEvent):
    name: ClassVar[str] = "queue.request.rejected"

    request_id: UUID

from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class RequestRequeued(DomainEvent):
    name: ClassVar[str] = "queue.request.requeued"

    request_id: UUID

from uuid import UUID
from datetime import datetime
from typing import ClassVar

from shared.building_blocks import DomainEvent


class RequestArchived(DomainEvent):
    name: ClassVar[str] = "queue.request.archived"

    request_id: UUID
    user_id: UUID
    request_created_at: datetime

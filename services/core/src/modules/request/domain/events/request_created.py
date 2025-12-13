from uuid import UUID
from datetime import date, time
from typing import ClassVar

from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import (
    RequestPriority,
    RequestStatus,
)


class RequestCreated(DomainEvent):
    name: ClassVar[str] = "request.created"

    request_id: UUID
    user_id: UUID
    queue_id: UUID
    purpose: str
    priority: RequestPriority
    status: RequestStatus

    preferred_date: date
    preferred_time_start: time
    preferred_time_end: time

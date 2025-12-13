from uuid import UUID
from datetime import date, time
from typing import ClassVar

from shared.building_blocks import DomainEvent


class RequestAccepted(DomainEvent):
    name: ClassVar[str] = "request.accepted"

    request_id: UUID
    confirmed_date: date
    confirmed_time_start: time
    confirmed_time_end: time

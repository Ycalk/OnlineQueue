from uuid import UUID
from datetime import date, time
from typing import ClassVar

from .base import BaseEvent


class RequestAccepted(BaseEvent):
    name: ClassVar[str] = "request.accepted"

    request_id: UUID
    confirmed_date: date
    confirmed_time_start: time
    confirmed_time_end: time

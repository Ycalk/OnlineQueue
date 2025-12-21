from uuid import UUID
from datetime import date, time
from typing import ClassVar

from .base import BaseEvent


class RequestTimeChanged(BaseEvent):
    name: ClassVar[str] = "request.changed_confirmed_datetime"

    request_id: UUID
    new_confirmed_date: date
    new_confirmed_time_start: time
    new_confirmed_time_end: time

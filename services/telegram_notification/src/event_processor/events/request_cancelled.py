from uuid import UUID
from typing import ClassVar

from .base import BaseEvent


class RequestCancelled(BaseEvent):
    name: ClassVar[str] = "request.cancelled"

    request_id: UUID
    user_id: UUID
    queue_id: UUID

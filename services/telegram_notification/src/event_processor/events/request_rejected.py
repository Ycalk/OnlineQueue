from uuid import UUID
from typing import ClassVar

from .base import BaseEvent


class RequestRejected(BaseEvent):
    name: ClassVar[str] = "request_rejected"

    request_id: UUID
    user_id: UUID
    queue_id: UUID
    reason: str | None

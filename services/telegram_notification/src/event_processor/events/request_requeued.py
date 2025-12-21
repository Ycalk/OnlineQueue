from uuid import UUID
from typing import ClassVar

from .base import BaseEvent


class RequestRequeued(BaseEvent):
    name: ClassVar[str] = "request_requeued"

    request_id: UUID
    user_id: UUID
    queue_id: UUID

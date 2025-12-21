from uuid import UUID
from typing import ClassVar

from .base import BaseEvent


class RequestCreated(BaseEvent):
    name: ClassVar[str] = "request.created"

    request_id: UUID
    user_id: UUID
    queue_id: UUID

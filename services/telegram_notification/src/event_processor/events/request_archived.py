from uuid import UUID
from typing import ClassVar

from .base import BaseEvent


class RequestArchived(BaseEvent):
    name: ClassVar[str] = "request.archived"

    request_id: UUID
    user_id: UUID
    queue_id: UUID
    status: str

from uuid import UUID
from typing import ClassVar

from .base import BaseEvent


class RequestRejected(BaseEvent):
    name: ClassVar[str] = "request.rejected"

    request_id: UUID

from uuid import UUID
from typing import ClassVar

from .base import BaseEvent


class UserLogin(BaseEvent):
    name: ClassVar[str] = "user.login"

    user_id: UUID
    ip_address: str | None

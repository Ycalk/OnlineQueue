from uuid import UUID
from typing import ClassVar

from .base import BaseEvent


class UserRegistered(BaseEvent):
    name: ClassVar[str] = "user.registered"

    user_id: UUID
    email: str

    first_name: str
    last_name: str
    patronymic: str | None

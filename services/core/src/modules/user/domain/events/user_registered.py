from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class UserRegistered(DomainEvent):
    name: ClassVar[str] = "user.registered"

    user_id: UUID
    email: str

    first_name: str
    last_name: str
    patronymic: str | None

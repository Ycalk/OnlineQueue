from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class UserLogin(DomainEvent):
    name: ClassVar[str] = "user.login"

    user_id: UUID
    email: str

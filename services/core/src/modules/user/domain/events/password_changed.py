from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class PasswordChanged(DomainEvent):
    name: ClassVar[str] = "user.password_changed"

    user_id: UUID
    email: str

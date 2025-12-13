from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class NameChanged(DomainEvent):
    name: ClassVar[str] = "user.name_changed"

    user_id: UUID
    email: str

    old_first_name: str
    old_last_name: str
    old_patronymic: str | None

    new_first_name: str
    new_last_name: str
    new_patronymic: str | None

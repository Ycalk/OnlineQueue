from uuid import UUID
from typing import ClassVar

from shared.building_blocks import DomainEvent


class EmailChanged(DomainEvent):
    name: ClassVar[str] = "user.email_changed"

    user_id: UUID
    new_email: str
    old_email: str

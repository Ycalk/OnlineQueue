from shared.building_blocks import DomainEvent
from modules.user.domain.value_objects import Email, Name
from modules.user.domain.aggregates import UserId


class NameChanged(DomainEvent):
    user_id: UserId
    email: Email
    old_name: Name
    new_name: Name

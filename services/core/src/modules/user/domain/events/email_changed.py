from shared.building_blocks import DomainEvent
from modules.user.domain.value_objects import Email
from modules.user.domain.aggregates import UserId


class EmailChanged(DomainEvent):
    user_id: UserId
    new_email: Email
    old_email: Email

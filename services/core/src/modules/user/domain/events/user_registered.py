from shared.building_blocks import DomainEvent
from modules.user.domain.value_objects import Email, Name
from modules.user.domain.aggregates import UserId


class UserRegistered(DomainEvent):
    user_id: UserId
    email: Email
    name: Name

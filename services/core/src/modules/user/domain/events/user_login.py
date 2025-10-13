from shared.building_blocks import DomainEvent
from modules.user.domain.value_objects import Email
from modules.user.domain.aggregates import UserId


class UserLogin(DomainEvent):
    user_id: UserId
    email: Email

from dataclasses import dataclass
from .id import UserId
from modules.user.domain.value_objects import Email, Name, HashedPassword, Username
from shared.building_blocks import AggregateRoot


@dataclass
class User(AggregateRoot):
    id: UserId
    email: Email
    name: Name
    username: Username
    hashed_password: HashedPassword

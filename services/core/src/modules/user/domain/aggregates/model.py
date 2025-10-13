from dataclasses import dataclass
from .id import UserId
from modules.user.domain.value_objects import Email, Name, HashedPassword
from shared.building_blocks import AggregateRoot
from modules.user.domain.events import (
    UserRegistered,
    UserLogin,
    PasswordChanged,
    EmailChanged,
    NameChanged,
)
from modules.user.domain.errors import WeakPasswordError, InvalidPasswordError
from typing import Self


@dataclass
class User(AggregateRoot):
    id: UserId
    email: Email
    name: Name
    hashed_password: HashedPassword

    @classmethod
    def register(cls, email: Email, name: Name, plain_password: str) -> Self:
        if len(plain_password) < 8:
            raise WeakPasswordError("Password must be at least 8 characters long")
        user = cls(
            id=UserId(),
            email=email,
            name=name,
            hashed_password=HashedPassword.from_plain_password(plain_password),
        )
        user._add_event(UserRegistered(user_id=user.id, email=email, name=name))
        return user

    def login(self, plain_password: str) -> None:
        if not self.hashed_password.verify(plain_password):
            raise InvalidPasswordError("Invalid password")

        self._add_event(UserLogin(user_id=self.id, email=self.email))

    def change_password(self, old_password: str, new_password: str) -> None:
        if not self.hashed_password.verify(old_password):
            raise InvalidPasswordError("Invalid password")
        if len(new_password) < 8:
            raise WeakPasswordError("Password must be at least 8 characters long")

        self.hashed_password = HashedPassword.from_plain_password(new_password)
        self._add_event(PasswordChanged(user_id=self.id, email=self.email))

    def change_email(self, new_email: Email) -> None:
        event = EmailChanged(user_id=self.id, new_email=new_email, old_email=self.email)
        self.email = new_email
        self._add_event(event)

    def change_name(self, new_name: Name) -> None:
        event = NameChanged(
            user_id=self.id, email=self.email, old_name=self.name, new_name=new_name
        )
        self.name = new_name
        self._add_event(event)

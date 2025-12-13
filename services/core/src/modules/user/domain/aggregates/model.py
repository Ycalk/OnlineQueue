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
from modules.user.domain.errors import (
    InvalidPasswordError,
    SamePasswordError,
    SameEmailError,
)
from typing import Self


@dataclass
class User(AggregateRoot):
    id: UserId
    email: Email
    name: Name
    hashed_password: HashedPassword

    @classmethod
    def register(cls, email: Email, name: Name, plain_password: str) -> Self:
        user = cls(
            id=UserId(),
            email=email,
            name=name,
            hashed_password=HashedPassword.from_plain_password(plain_password),
        )
        user._add_event(
            UserRegistered(
                user_id=user.id.value,
                email=email.value,
                first_name=name.first_name,
                last_name=name.last_name,
                patronymic=name.patronymic,
            )
        )
        return user

    def login(self, plain_password: str) -> None:
        if not self.hashed_password.verify(plain_password):
            raise InvalidPasswordError("Invalid password")

        self._add_event(UserLogin(user_id=self.id.value, email=self.email.value))

    def change_password(self, old_password: str, new_password: str) -> None:
        if not self.hashed_password.verify(old_password):
            raise InvalidPasswordError("Invalid password")

        if old_password == new_password:
            raise SamePasswordError("New password must be different from old password")

        self.hashed_password = HashedPassword.from_plain_password(new_password)
        self._add_event(PasswordChanged(user_id=self.id.value, email=self.email.value))

    def change_email(self, new_email: Email, password: str) -> None:
        if not self.hashed_password.verify(password):
            raise InvalidPasswordError("Invalid password")

        if new_email == self.email:
            raise SameEmailError("New email must be different from old email")

        event = EmailChanged(
            user_id=self.id.value, new_email=new_email.value, old_email=self.email.value
        )
        self.email = new_email
        self._add_event(event)

    def change_name(self, new_name: Name) -> None:
        event = NameChanged(
            user_id=self.id.value,
            email=self.email.value,
            old_first_name=self.name.first_name,
            old_last_name=self.name.last_name,
            old_patronymic=self.name.patronymic,
            new_first_name=new_name.first_name,
            new_last_name=new_name.last_name,
            new_patronymic=new_name.patronymic,
        )
        self.name = new_name
        self._add_event(event)

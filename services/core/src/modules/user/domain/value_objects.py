import bcrypt
from pydantic import BaseModel, ConfigDict
from pydantic.types import StringConstraints
from pydantic import EmailStr
from typing import Annotated, Self, Final
from modules.user.domain.errors import WeakPasswordError


MINIMAL_PASSWORD_LENGTH: Final[int] = 8


class HashedPassword(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: str

    @classmethod
    def from_plain_password(cls, from_plain_password: str) -> Self:
        if len(from_plain_password) < MINIMAL_PASSWORD_LENGTH:
            raise WeakPasswordError(
                f"Password must be at least {MINIMAL_PASSWORD_LENGTH} characters long"
            )
        return cls(
            value=bcrypt.hashpw(
                from_plain_password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
        )

    def verify(self, plain_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), self.value.encode("utf-8")
        )


_NameItem = Annotated[str, StringConstraints(min_length=1, max_length=100)]


class Name(BaseModel):
    model_config = ConfigDict(frozen=True)

    first_name: _NameItem
    last_name: _NameItem
    patronymic: _NameItem | None = None


class Email(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: EmailStr

    def __str__(self) -> str:
        return self.value

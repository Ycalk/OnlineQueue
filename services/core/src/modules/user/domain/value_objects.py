import bcrypt
from pydantic import BaseModel, ConfigDict
from pydantic.types import StringConstraints
from pydantic import EmailStr
from typing import Annotated, Self


class HashedPassword(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: str

    @classmethod
    def from_plain_password(cls, from_plain_password: str) -> Self:
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


class Username(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: Annotated[str, StringConstraints(min_length=3, max_length=32)]

    def __str__(self) -> str:
        return self.value


class Email(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: EmailStr

    def __str__(self) -> str:
        return self.value

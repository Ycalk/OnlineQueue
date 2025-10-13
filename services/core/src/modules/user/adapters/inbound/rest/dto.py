from pydantic import BaseModel, Field
from typing import Literal


class RegisterRequest(BaseModel):
    email: str = Field(description="Электронная почта", examples=["abcdef@example.com"])
    password: str = Field(description="Пароль, который ввел пользователь")
    first_name: str = Field(description="Имя пользователя")
    last_name: str = Field(description="Фамилия пользователя")
    patronymic: str | None = Field(None, description="Отчество пользователя")


class LoginRequest(BaseModel):
    email: str = Field(description="Электронная почта", examples=["abcdef@example.com"])
    password: str = Field(description="Пароль, который ввел пользователь")


class TokenResponse(BaseModel):
    access_token: str = Field(
        description="Токен доступа, который нужен для аутентификации (его нужно передавать в header)"
    )
    token_type: Literal["bearer"] = Field(
        default="bearer",
        description="Тип токена, который нужен для аутентификации. Всегда будет 'bearer'",
    )


class MessageResponse(BaseModel):
    message: str

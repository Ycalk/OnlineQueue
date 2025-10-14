from pydantic import BaseModel, Field
from typing import Literal


class LoginRequest(BaseModel):
    email: str = Field(description="Электронная почта", examples=["abcdef@example.com"])
    password: str = Field(description="Пароль, который ввел пользователь")


class RegisterRequest(LoginRequest):
    first_name: str = Field(description="Имя пользователя")
    last_name: str = Field(description="Фамилия пользователя")
    patronymic: str | None = Field(None, description="Отчество пользователя")


class TokenResponse(BaseModel):
    access_token: str = Field(
        description="Токен доступа, который нужен для аутентификации (его нужно передавать в header)"
    )
    token_type: Literal["bearer"] = Field(
        default="bearer",
        description="Тип токена, который нужен для аутентификации. Всегда будет 'bearer'",
    )


class UpdateEmailRequest(BaseModel):
    new_email: str = Field(description="Новый email", examples=["abcdef@example.com"])
    current_password: str = Field(description="Текущий пароль пользователя")


class UpdateNameRequest(BaseModel):
    first_name: str | None = Field(description="Новое имя пользователя")
    last_name: str | None = Field(description="Новая фамилия пользователя")
    patronymic: str | None = Field(description="Новое отчество пользователя")


class UpdatePasswordRequest(BaseModel):
    old_password: str = Field(description="Текущий пароль пользователя")
    new_password: str = Field(description="Новый пароль пользователя")

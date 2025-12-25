import struct
import time
import base64
from uuid import UUID
from fastapi import APIRouter, Depends, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from cryptography.hazmat.primitives.ciphers.aead import AESSIV

from core.settings import settings
from modules.user.domain.ports.inbound.use_cases import (
    IChangeEmail,
    IChangeName,
    IChangePassword,
)
from modules.user.application.ports.inbound.queries import IGetUser
from modules.user.domain.aggregates import UserId
from modules.user.domain.commands import ChangeEmail, ChangeName, ChangePassword
from modules.user.domain.value_objects import Email
from shared.adapters.rest import get_current_user_id, MessageResponse, ErrorResponse
from .dto import (
    UpdateEmailRequest,
    UpdateNameRequest,
    UpdatePasswordRequest,
    UserNameResponse,
    TelegramLinkResponse,
)
from modules.user.application.dto import User as UserResponse


router = APIRouter(
    prefix="/users",
    tags=["users"],
    route_class=DishkaRoute,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Токен не валиден",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Токен доступа указан неверно",
        },
    },
)


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(
    get_user_query: FromDishka[IGetUser],
    current_user_id: UUID = Depends(get_current_user_id),
) -> UserResponse:
    """
    Получить информацию о текущем пользователе.
    \nВозможные ошибки:
    \n`UserNotFoundError` - пользователь не найден
    """
    return await get_user_query(current_user_id)


@router.patch("/email", status_code=status.HTTP_200_OK)
async def update_email(
    request: UpdateEmailRequest,
    change_email_uc: FromDishka[IChangeEmail],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Изменить email текущего пользователя.
    \nВозможные ошибки:
    \n`UserNotFoundError` - пользователь не найден
    \n`UserAlreadyExistsError` - пользователь с таким email уже зарегистрирован
    \n`InvalidPasswordError` - неверный пароль
    \n`SameEmailError` - новый email совпадает с текущим
    """
    command = ChangeEmail(
        user_id=UserId(value=current_user_id),
        new_email=Email(value=request.new_email),
        password=request.current_password,
    )

    await change_email_uc(command)

    return MessageResponse(message="Email updated successfully")


@router.patch("/name", status_code=status.HTTP_200_OK)
async def update_name(
    request: UpdateNameRequest,
    change_name_uc: FromDishka[IChangeName],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Изменить имя текущего пользователя.
    \nВозможные ошибки:
    \n`UserNotFoundError` - пользователь не найден
    """

    command = ChangeName(
        user_id=UserId(value=current_user_id),
        new_first_name=request.first_name,
        new_last_name=request.last_name,
        new_patronymic=request.patronymic,
    )

    await change_name_uc(command)

    return MessageResponse(message="Name updated successfully")


@router.patch(
    "/password",
    status_code=status.HTTP_200_OK,
)
async def update_password(
    request: UpdatePasswordRequest,
    change_password_uc: FromDishka[IChangePassword],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Изменить пароль текущего пользователя.
    \nВозможные ошибки:
    \n`UserNotFoundError` - пользователь не найден
    \n`InvalidPasswordError` - неверный пароль
    \n`SamePasswordError` - новый пароль совпадает с текущим
    \n`WeakPasswordError` - пароль слишком слабый
    """
    command = ChangePassword(
        user_id=UserId(value=current_user_id),
        old_password=request.old_password,
        new_password=request.new_password,
    )

    await change_password_uc(command)

    return MessageResponse(message="Password updated successfully")


@router.get("/telegram", status_code=status.HTTP_200_OK)
async def get_telegram_link(
    aessiv: FromDishka[AESSIV],
    current_user_id: UUID = Depends(get_current_user_id),
) -> TelegramLinkResponse:
    """
    Сгенерировать ссылку для привязки Telegram-аккаунта.
    """
    timestamp = int(time.time())
    packed_data = struct.pack(">16sI", current_user_id.bytes, timestamp)
    encrypted_bytes = aessiv.encrypt(packed_data, None)
    token = base64.urlsafe_b64encode(encrypted_bytes).decode("utf-8")

    link = f"https://t.me/{settings.notifications_bot_username}?start={token}"

    return TelegramLinkResponse(link=link)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_name(
    user_id: UUID,
    get_user_query: FromDishka[IGetUser],
) -> UserNameResponse:
    """
    Получить информацию о имени пользователя.
    \nВозможные ошибки:
    \n`UserNotFoundError` - пользователь не найден
    """

    user = await get_user_query(user_id)

    return UserNameResponse(
        first_name=user.first_name,
        last_name=user.last_name,
        patronymic=user.patronymic,
    )

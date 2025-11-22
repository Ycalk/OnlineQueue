from uuid import UUID
from fastapi import APIRouter, Depends, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from modules.user.domain.ports.inbound.use_cases import (
    IChangeEmail,
    IChangeName,
    IChangePassword,
)
from modules.user.domain.ports.inbound.queries import IGetUser
from modules.user.domain.aggregates import UserId
from modules.user.domain.commands import ChangeEmail, ChangeName, ChangePassword
from modules.user.domain.value_objects import Email
from shared.adapters import get_current_user_id, MessageResponse, ErrorResponse
from .dto import (
    UpdateEmailRequest,
    UpdateNameRequest,
    UpdatePasswordRequest,
    UserResponse,
    UserNameResponse,
)


router = APIRouter(
    prefix="/users",
    tags=["users"],
    route_class=DishkaRoute,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Пользователь с id из токена не найден",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Токен не валиден",
        },
    },
)


@router.get("/me")
async def get_me(
    get_user_query: FromDishka[IGetUser],
    current_user_id: UUID = Depends(get_current_user_id),
) -> UserResponse:
    """
    Получить информацию о текущем пользователе
    """

    user = await get_user_query(UserId(value=current_user_id))

    return UserResponse(
        email=user.email.value,
        first_name=user.name.first_name,
        last_name=user.name.last_name,
        patronymic=user.name.patronymic,
    )


@router.patch(
    "/email",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Неверный пароль",
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "Пользователь с таким email уже зарегистрирован",
        },
    },
)
async def update_email(
    request: UpdateEmailRequest,
    change_email_uc: FromDishka[IChangeEmail],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Изменить email текущего пользователя
    """
    command = ChangeEmail(
        user_id=UserId(value=current_user_id),
        new_email=Email(value=request.new_email),
        password=request.current_password,
    )

    await change_email_uc(command)

    return MessageResponse(message="Email updated successfully")


@router.patch("/name")
async def update_name(
    request: UpdateNameRequest,
    change_name_uc: FromDishka[IChangeName],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Изменить имя текущего пользователя
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
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "Неверный текущий пароль",
        },
    },
)
async def update_password(
    request: UpdatePasswordRequest,
    change_password_uc: FromDishka[IChangePassword],
    current_user_id: UUID = Depends(get_current_user_id),
) -> MessageResponse:
    """
    Изменить пароль текущего пользователя
    """
    command = ChangePassword(
        user_id=UserId(value=current_user_id),
        old_password=request.old_password,
        new_password=request.new_password,
    )

    await change_password_uc(command)

    return MessageResponse(message="Password updated successfully")


@router.get("/{user_id}")
async def get_user_name(
    user_id: UUID,
    get_user_query: FromDishka[IGetUser],
    _: UUID = Depends(get_current_user_id),
) -> UserNameResponse:
    """
    Получить информацию о текущем пользователе
    """

    user = await get_user_query(UserId(value=user_id))

    return UserNameResponse(
        first_name=user.name.first_name,
        last_name=user.name.last_name,
        patronymic=user.name.patronymic,
    )

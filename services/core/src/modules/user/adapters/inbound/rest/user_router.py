from fastapi import APIRouter, Depends, HTTPException, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from modules.user.domain.ports.inbound.use_cases import (
    IChangeEmail,
    IChangeName,
    IChangePassword,
)
from modules.user.domain.aggregates import UserId
from modules.user.domain.commands import ChangeEmail, ChangeName, ChangePassword
from modules.user.domain.value_objects import Email
from modules.user.domain.errors import (
    InvalidPasswordError,
    WeakPasswordError,
    SamePasswordError,
    SameEmailError,
)
from modules.user.application.errors import UserNotFoundError, UserAlreadyExistsError
from shared.adapters import get_current_user_id, MessageResponse, HTTPError
from .dto import UpdateEmailRequest, UpdateNameRequest, UpdatePasswordRequest


router = APIRouter(
    prefix="/user",
    tags=["users"],
    route_class=DishkaRoute,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTPError,
            "description": "Пользователь с id из токена не найден",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTPError,
            "description": "Токен не валиден",
        },
    },
)


@router.patch(
    "/email",
    response_model=MessageResponse,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": HTTPError,
            "description": "Неверный пароль",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPError,
            "description": "Новый email должен отличаться от старого",
        },
        status.HTTP_409_CONFLICT: {
            "model": HTTPError,
            "description": "Пользователь с таким email уже зарегистрирован",
        },
    },
)
async def update_email(
    request: UpdateEmailRequest,
    change_email_uc: FromDishka[IChangeEmail],
    current_user_id: UserId = Depends(get_current_user_id),
):
    """
    Изменить email текущего пользователя
    """
    try:
        command = ChangeEmail(
            user_id=current_user_id,
            new_email=Email(value=request.new_email),
            password=request.current_password,
        )

        await change_email_uc(command)

        return MessageResponse(message="Email updated successfully")

    except InvalidPasswordError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid password"
        )
    except SameEmailError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New email must be different from old email",
        )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.patch("/name", response_model=MessageResponse)
async def update_name(
    request: UpdateNameRequest,
    change_name_uc: FromDishka[IChangeName],
    current_user_id: UserId = Depends(get_current_user_id),
):
    """
    Изменить имя текущего пользователя
    """
    try:
        command = ChangeName(
            user_id=current_user_id,
            new_first_name=request.first_name,
            new_last_name=request.last_name,
            new_patronymic=request.patronymic,
        )

        await change_name_uc(command)

        return MessageResponse(message="Name updated successfully")

    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.patch(
    "/password",
    response_model=MessageResponse,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "model": HTTPError,
            "description": "Неверный текущий пароль",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPError,
            "description": "Новый пароль должен отличаться от старого",
        },
        status.HTTP_409_CONFLICT: {
            "model": HTTPError,
            "description": "Новый пароль слишком слабый",
        },
    },
)
async def update_password(
    request: UpdatePasswordRequest,
    change_password_uc: FromDishka[IChangePassword],
    current_user_id: UserId = Depends(get_current_user_id),
):
    """
    Изменить пароль текущего пользователя
    """
    try:
        command = ChangePassword(
            user_id=current_user_id,
            old_password=request.old_password,
            new_password=request.new_password,
        )

        await change_password_uc(command)

        return MessageResponse(message="Password updated successfully")

    except InvalidPasswordError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid current password"
        )
    except SamePasswordError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from old password",
        )
    except WeakPasswordError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Password is too weak"
        )

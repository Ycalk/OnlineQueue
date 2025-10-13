from fastapi import APIRouter, Response, Cookie, HTTPException, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from modules.user.domain.ports.inbound.use_cases import ICreateUser, ILogin
from modules.user.domain.commands import CreateUser, Login
from modules.user.domain.value_objects import Email, Name
from modules.user.domain.errors import WeakPasswordError, InvalidPasswordError
from modules.user.application.errors import UserAlreadyExistsError, UserNotFoundError
from shared.adapters import (
    JWTService,
    InvalidTokenError,
    TokenExpiredError,
    TokenType,
    HTTPError,
)
from core.settings import settings
from .dto import RegisterRequest, LoginRequest, TokenResponse, MessageResponse

router = APIRouter(prefix="/auth", tags=["authentication"], route_class=DishkaRoute)


def set_refresh_token_cookie(response: Response, refresh_token: str) -> None:
    response.set_cookie(
        key=settings.refresh_token_cookie_name,
        value=refresh_token,
        max_age=settings.refresh_token_expire_days * 86400,  # в секундах
        httponly=True,
        secure=not settings.debug,  # HTTPS only в production
        samesite="lax",
        path="/auth/token",
    )


def clear_refresh_token_cookie(response: Response) -> None:
    response.delete_cookie(key=settings.refresh_token_cookie_name, path="/auth/token")


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": HTTPError,
            "description": "Пользователь с таким email уже зарегистрирован",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTPError,
            "description": "Слишком слабый пароль",
        },
    },
)
async def register(
    request: RegisterRequest,
    response: Response,
    create_user_uc: FromDishka[ICreateUser],
):
    """
    Регистрация нового пользователя
    """
    try:
        command = CreateUser(
            email=Email(value=request.email),
            name=Name(
                first_name=request.first_name,
                last_name=request.last_name,
                patronymic=request.patronymic,
            ),
            password=request.password,
        )
        user = await create_user_uc(command)

        access_token = JWTService.create_access_token(user.id.value)
        refresh_token = JWTService.create_refresh_token(user.id.value)
        set_refresh_token_cookie(response, refresh_token)

        return TokenResponse(access_token=access_token)

    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except WeakPasswordError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTPError,
            "description": "Неверные email или пароль",
        }
    },
)
async def login(
    request: LoginRequest, response: Response, verify_uc: FromDishka[ILogin]
):
    """
    Аутентификация пользователя
    """
    try:
        command = Login(
            email=Email(value=request.email), plain_password=request.password
        )
        user = await verify_uc(command)

        access_token = JWTService.create_access_token(user.id.value)
        refresh_token = JWTService.create_refresh_token(user.id.value)
        set_refresh_token_cookie(response, refresh_token)

        return TokenResponse(access_token=access_token)

    except (UserNotFoundError, InvalidPasswordError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )


@router.post(
    "/token",
    response_model=TokenResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": HTTPError,
            "description": "Refresh токена нет в куках / невалиден / истек. После этого нужно залогиниться заново",
        }
    },
)
async def refresh_access_token(
    response: Response,
    refresh_token: str | None = Cookie(None, alias=settings.refresh_token_cookie_name),
):
    """
    Обновление токена доступа
    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found"
        )

    try:
        user_id = JWTService.verify_token(refresh_token, token_type=TokenType.REFRESH)

        new_access_token = JWTService.create_access_token(user_id)
        new_refresh_token = JWTService.create_refresh_token(user_id)
        set_refresh_token_cookie(response, new_refresh_token)

        return TokenResponse(access_token=new_access_token)

    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired"
        )

    except InvalidTokenError as e:
        clear_refresh_token_cookie(response)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {str(e)}",
        )


@router.post("/logout", response_model=MessageResponse)
async def logout(response: Response):
    """
    Выход из аккаунта
    """
    clear_refresh_token_cookie(response)
    return MessageResponse(message="Logged out successfully")

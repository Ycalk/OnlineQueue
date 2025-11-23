from uuid import UUID
from fastapi import Depends, status
from shared.building_blocks import CustomHTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_service import JWTService, TokenType, InvalidTokenError, TokenExpiredError


security = HTTPBearer(
    scheme_name="Основная авторизация",
    description=(
        "Для использования API необходимо передать токен в заголовке "
        "Authorization в формате 'Bearer <токен>'."
    ),
)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UUID:
    token = credentials.credentials

    try:
        return JWTService.verify_token(token, TokenType.ACCESS)

    except TokenExpiredError:
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error="TokenExpiredError",
            message="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error="InvalidTokenError",
            message="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

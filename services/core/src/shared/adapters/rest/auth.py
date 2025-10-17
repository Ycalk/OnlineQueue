from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_service import JWTService, TokenType, InvalidTokenError, TokenExpiredError
from modules.user.domain.aggregates import UserId


security = HTTPBearer(
    scheme_name="Основная авторизация",
    description=(
        "Для использования API необходимо передать токен в заголовке "
        "Authorization в формате 'Bearer <токен>'."
    ),
)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserId:
    token = credentials.credentials

    try:
        user_uuid = JWTService.verify_token(token, TokenType.ACCESS)
        return UserId(value=user_uuid)

    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

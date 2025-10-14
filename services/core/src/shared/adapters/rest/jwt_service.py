import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from uuid import UUID
from enum import StrEnum
from core.settings import settings


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPayload(BaseModel):
    sub: UUID
    exp: int
    iat: int
    type: TokenType


class InvalidTokenError(Exception):
    pass


class TokenExpiredError(Exception):
    pass


class JWTService:
    @classmethod
    def create_access_token(cls, user_id: UUID) -> str:
        now = datetime.now()
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)

        payload = TokenPayload(
            sub=user_id,
            exp=int((now + expires_delta).timestamp()),
            iat=int(now.timestamp()),
            type=TokenType.ACCESS,
        )

        return jwt.encode(
            payload.model_dump(mode="json"),
            settings.secret_key,
            algorithm=settings.encoding_algorithm,
        )

    @classmethod
    def create_refresh_token(cls, user_id: UUID) -> str:
        now = datetime.now()
        expires_delta = timedelta(days=settings.refresh_token_expire_days)

        payload = TokenPayload(
            sub=user_id,
            exp=int((now + expires_delta).timestamp()),
            iat=int(now.timestamp()),
            type=TokenType.REFRESH,
        )

        return jwt.encode(
            payload.model_dump(mode="json"),
            settings.secret_key,
            algorithm=settings.encoding_algorithm,
        )

    @classmethod
    def verify_token(cls, token: str, token_type: TokenType) -> UUID:
        try:
            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.encoding_algorithm]
            )

            token_data = TokenPayload(**payload)

            if token_data.type != token_type:
                raise InvalidTokenError(
                    f"Invalid token type: expected {token_type}, got {token_data.type}"
                )

            if token_data.exp < int(datetime.now().timestamp()):
                raise TokenExpiredError("Token expired")

            return token_data.sub

        except jwt.InvalidTokenError as e:
            raise InvalidTokenError(f"Invalid token: {str(e)}") from e

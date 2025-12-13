from core.settings import settings
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from typing import Final

DATABASE_URL: Final[str] = (
    (
        f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    )
    if not settings.debug
    else "sqlite+aiosqlite:///:memory:"
)


class Base(AsyncAttrs, DeclarativeBase):
    pass

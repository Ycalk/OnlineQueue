from typing import AsyncIterable

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from dishka import Provider, Scope, provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from cryptography.hazmat.primitives.ciphers.aead import AESSIV

from .models import Base
from .settings import settings


class BotProvider(Provider):
    @provide(scope=Scope.APP)
    def get_bot(self) -> Bot:
        return Bot(token=settings.bot_token)

    @provide(scope=Scope.APP)
    async def get_redis(self) -> AsyncIterable[Redis]:
        redis = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
        )
        yield redis
        await redis.aclose()

    @provide(scope=Scope.APP)
    def get_dispatcher(self, redis: Redis) -> Dispatcher:
        storage = RedisStorage(redis)
        return Dispatcher(storage=storage)

    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        url = (
            f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
            f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
        )
        engine = create_async_engine(url, echo=False)

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def get_session_factory(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with factory() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_aessiv(self) -> AESSIV:
        return AESSIV(bytes.fromhex(settings.aessiv_hex_key))

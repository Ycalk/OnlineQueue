from typing import AsyncIterable
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from shared.persistence import DATABASE_URL, Base, register_models
from core.settings import settings


class PersistenceProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        if settings.debug:
            engine = create_async_engine(
                DATABASE_URL,
                connect_args={"check_same_thread": False},
                poolclass=None,
            )
            async with engine.begin() as conn:
                await register_models(conn, sqlite_mode=True)
                await conn.run_sync(Base.metadata.create_all)
        else:
            engine = create_async_engine(
                DATABASE_URL,
                echo=False,
                pool_size=settings.pool_size,
                max_overflow=settings.max_overflow,
                pool_pre_ping=True,
            )
        try:
            yield engine
        finally:
            await engine.dispose()

    @provide(scope=Scope.APP)
    def get_session_factory(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

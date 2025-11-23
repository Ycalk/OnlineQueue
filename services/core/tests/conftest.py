import pytest
import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from shared.building_blocks.event import IEventPublisher
from shared.persistence import Base, register_models


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=None,
    )
    async with engine.begin() as conn:
        await register_models(conn, sqlite_mode=True)
        await conn.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    async with session_factory() as session:
        yield session

    await engine.dispose()


class EventPublisherCounter(IEventPublisher):
    def __init__(self):
        self.events = []

    async def publish(self, event):
        self.events.append(event)


@pytest.fixture(scope="function")
def event_publisher() -> EventPublisherCounter:
    return EventPublisherCounter()

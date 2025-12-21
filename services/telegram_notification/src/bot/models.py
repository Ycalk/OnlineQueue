from datetime import datetime, date, time
from uuid import UUID

from sqlalchemy import BigInteger, String, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    user_id: Mapped[UUID] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)

    linked_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Queue(Base):
    __tablename__ = "queues"

    queue_id: Mapped[UUID] = mapped_column(primary_key=True)
    owner_id: Mapped[UUID] = mapped_column(index=True)
    name: Mapped[str] = mapped_column(String(255))


class Request(Base):
    __tablename__ = "requests"

    request_id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(index=True)
    queue_id: Mapped[UUID] = mapped_column(ForeignKey("queues.queue_id"), index=True)
    purpose: Mapped[str] = mapped_column(String(1000))
    preferred_date: Mapped[date] = mapped_column()
    preferred_time_start: Mapped[time] = mapped_column()
    preferred_time_end: Mapped[time] = mapped_column()

    status: Mapped[str] = mapped_column(String(50), default="pending")

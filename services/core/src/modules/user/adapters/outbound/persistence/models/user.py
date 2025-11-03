from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from shared.persistence.utils import Base
from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .telegram_user import TelegramUser


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "user_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    patronymic: Mapped[str | None] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    telegram_account: Mapped[Optional["TelegramUser"]] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __init__(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password_hash: str,
        id: UUID | None = None,
        patronymic: str | None = None,
    ):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
        self.patronymic = patronymic
        if id is not None:
            self.id = id

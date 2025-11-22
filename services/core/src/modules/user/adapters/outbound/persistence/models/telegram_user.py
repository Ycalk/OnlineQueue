from uuid import UUID
from datetime import datetime
from shared.persistence.utils import Base
from sqlalchemy import func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .user import User


class TelegramUser(Base):
    __tablename__ = "telegram_user"
    __table_args__ = {"schema": "user_schema"}

    telegram_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(User.id), index=True)
    username: Mapped[str | None] = mapped_column(String(40))
    added_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="telegram_account")

    def __init__(self, telegram_id: int, user: "User", username: str | None = None):
        self.telegram_id = telegram_id
        self.username = username
        self.user = user

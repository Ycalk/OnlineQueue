from uuid import UUID, uuid4
from datetime import datetime, time
from shared.persistence.utils import Base
from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .request import Request


class Queue(Base):
    __tablename__ = "queue"
    __table_args__ = {"schema": "queue_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    owner_id: Mapped[UUID] = mapped_column(index=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(1000))
    clean_up_period_days: Mapped[int] = mapped_column()
    reception_time_start: Mapped[time] = mapped_column()
    reception_time_end: Mapped[time] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    requests: Mapped[list["Request"]] = relationship(
        back_populates="queue",
        cascade="all, delete-orphan",
        lazy="raise",
    )

    def __init__(
        self,
        owner_id: UUID,
        name: str,
        clean_up_period_days: int,
        reception_time_start: time,
        reception_time_end: time,
        description: str | None = None,
        id: UUID | None = None,
        is_active: bool | None = None,
    ):
        self.owner_id = owner_id
        self.name = name
        self.description = description
        self.clean_up_period_days = clean_up_period_days
        self.reception_time_start = reception_time_start
        self.reception_time_end = reception_time_end
        if id:
            self.id = id
        if is_active is not None:
            self.is_active = is_active

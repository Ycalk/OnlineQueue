from datetime import datetime, time
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.persistence.utils import Base

if TYPE_CHECKING:
    from .request import RequestModel


class Queue(Base):
    __tablename__ = "queue"
    __table_args__ = {"schema": "request_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    owner_id: Mapped[UUID] = mapped_column(index=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    reception_time_start: Mapped[time] = mapped_column()
    reception_time_end: Mapped[time] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    requests: Mapped[list["RequestModel"]] = relationship(
        back_populates="queue",
        cascade="all, delete-orphan",
        lazy="raise",
    )

    def __init__(
        self,
        owner_id: UUID,
        reception_time_start: time,
        reception_time_end: time,
        id: UUID | None = None,
        is_active: bool | None = None,
    ):
        self.owner_id = owner_id
        self.reception_time_start = reception_time_start
        self.reception_time_end = reception_time_end
        if id:
            self.id = id
        if is_active is not None:
            self.is_active = is_active

from uuid import UUID, uuid4
from datetime import datetime, time, date
from shared.adapters.persistence.utils import Base
from sqlalchemy import func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .queue import Queue


class QueueRequest(Base):
    __tablename__ = "request"
    __table_args__ = {"schema": "queue_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(index=True)
    queue_id: Mapped[UUID] = mapped_column(ForeignKey(Queue.id), index=True)

    preferred_date: Mapped[date] = mapped_column()
    preferred_time_start: Mapped[time] = mapped_column()
    preferred_time_end: Mapped[time] = mapped_column()

    confirmed_date: Mapped[date | None] = mapped_column()
    confirmed_time_start: Mapped[time | None] = mapped_column()
    confirmed_time_end: Mapped[time | None] = mapped_column()

    archived: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    status: Mapped[str] = mapped_column(String(50))
    priority: Mapped[str] = mapped_column(String(50))
    queue: Mapped[Queue] = relationship(back_populates="requests")

    def __init__(
        self,
        user_id: UUID,
        queue: Queue,
        preferred_date: date,
        preferred_time_start: time,
        preferred_time_end: time,
        status: str,
        priority: str,
        confirmed_date: date | None = None,
        confirmed_time_start: time | None = None,
        confirmed_time_end: time | None = None,
        id: UUID | None = None,
        archived: bool | None = None,
        created_at: datetime | None = None,
    ):
        self.user_id = user_id
        self.queue = queue
        self.status = status
        self.preferred_date = preferred_date
        self.preferred_time_start = preferred_time_start
        self.preferred_time_end = preferred_time_end
        self.confirmed_date = confirmed_date
        self.confirmed_time_start = confirmed_time_start
        self.confirmed_time_end = confirmed_time_end
        self.priority = priority
        if id:
            self.id = id
        if archived:
            self.archived = archived
        if created_at:
            self.created_at = created_at

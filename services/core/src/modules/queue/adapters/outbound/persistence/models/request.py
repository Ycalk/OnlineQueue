from uuid import UUID, uuid4
from datetime import datetime, time, date
from shared.persistence.utils import Base
from sqlalchemy import func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .queue import Queue


class Request(Base):
    __tablename__ = "request"
    __table_args__ = {"schema": "request_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column()
    queue_id: Mapped[UUID] = mapped_column(ForeignKey(Queue.id))

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

    status_history: Mapped[list["RequestStatusHistoryItem"]] = relationship(
        back_populates="request"
    )
    queue: Mapped[Queue] = relationship(back_populates="requests")

    def __init__(
        self,
        user_id: UUID,
        queue: Queue,
        preferred_date: date,
        preferred_time_start: time,
        preferred_time_end: time,
        confirmed_date: date | None = None,
        confirmed_time_start: time | None = None,
        confirmed_time_end: time | None = None,
        id: UUID | None = None,
        archived: bool | None = None,
        created_at: datetime | None = None,
    ):
        self.user_id = user_id
        self.queue = queue
        self.preferred_date = preferred_date
        self.preferred_time_start = preferred_time_start
        self.preferred_time_end = preferred_time_end
        self.confirmed_date = confirmed_date
        self.confirmed_time_start = confirmed_time_start
        self.confirmed_time_end = confirmed_time_end
        if id:
            self.id = id
        if archived:
            self.archived = archived
        if created_at:
            self.created_at = created_at


class RequestStatusHistoryItem(Base):
    __tablename__ = "request_status_history_item"
    __table_args__ = {"schema": "request_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    request_id: Mapped[UUID] = mapped_column(ForeignKey(Request.id))
    status: Mapped[str] = mapped_column(String(50))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    request: Mapped[Request] = relationship(back_populates="status_history")

    def __init__(
        self,
        request: Request,
        status: str,
        id: UUID | None = None,
    ):
        self.request = request
        self.status = status
        if id:
            self.id = id

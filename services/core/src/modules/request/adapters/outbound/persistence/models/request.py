from datetime import date as DateType, time as TimeType, datetime as DateTimeType
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.persistence.utils import Base
from .queue import Queue


class Request(Base):
    __tablename__ = "request"
    __table_args__ = {"schema": "request_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(index=True)
    queue_id: Mapped[UUID] = mapped_column(ForeignKey(Queue.id), index=True)

    purpose: Mapped[str] = mapped_column(String(1000))

    preferred_date: Mapped[DateType | None] = mapped_column()
    preferred_time_start: Mapped[TimeType | None] = mapped_column()
    preferred_time_end: Mapped[TimeType | None] = mapped_column()

    confirmed_date: Mapped[DateType | None] = mapped_column()
    confirmed_time_start: Mapped[TimeType | None] = mapped_column()
    confirmed_time_end: Mapped[TimeType | None] = mapped_column()

    is_archived: Mapped[bool] = mapped_column(default=False)
    priority: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20))

    created_at: Mapped[DateTimeType] = mapped_column(server_default=func.now())
    updated_at: Mapped[DateTimeType] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    status_history: Mapped[list["RequestStatusHistoryItem"]] = relationship(
        back_populates="request",
        cascade="all, delete-orphan",
        lazy="raise",
    )
    confirmation_history: Mapped[list["RequestConfirmationHistoryItem"]] = relationship(
        back_populates="request",
        cascade="all, delete-orphan",
        lazy="raise",
    )

    queue: Mapped[Queue] = relationship(back_populates="requests")

    def __init__(
        self,
        user_id: UUID,
        queue: Queue,
        purpose: str,
        preferred_date: DateType | None = None,
        preferred_time_start: TimeType | None = None,
        preferred_time_end: TimeType | None = None,
        confirmed_date: DateType | None = None,
        confirmed_time_start: TimeType | None = None,
        confirmed_time_end: TimeType | None = None,
        priority: str = "medium",
        status: str = "pending",
        id: UUID | None = None,
        is_archived: bool | None = None,
        created_at: DateTimeType | None = None,
    ):
        self.user_id = user_id
        self.queue = queue
        self.purpose = purpose

        self.preferred_date = preferred_date
        self.preferred_time_start = preferred_time_start
        self.preferred_time_end = preferred_time_end

        self.confirmed_date = confirmed_date
        self.confirmed_time_start = confirmed_time_start
        self.confirmed_time_end = confirmed_time_end

        self.priority = priority
        self.status = status

        if id:
            self.id = id
        if is_archived is not None:
            self.is_archived = is_archived
        if created_at:
            self.created_at = created_at


class RequestStatusHistoryItem(Base):
    __tablename__ = "request_status_history_item"
    __table_args__ = {"schema": "request_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    request_id: Mapped[UUID] = mapped_column(ForeignKey(Request.id), index=True)
    status: Mapped[str] = mapped_column(String(50))
    updated_at: Mapped[DateTimeType] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
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


class RequestConfirmationHistoryItem(Base):
    __tablename__ = "request_confirmation_history_item"
    __table_args__ = {"schema": "request_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    request_id: Mapped[UUID] = mapped_column(ForeignKey(Request.id), index=True)

    date: Mapped[DateType] = mapped_column()
    time_start: Mapped[TimeType] = mapped_column()
    time_end: Mapped[TimeType] = mapped_column()
    updated_at: Mapped[DateTimeType] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    request: Mapped[Request] = relationship(back_populates="confirmation_history")

    def __init__(
        self,
        request: Request,
        date: DateType,
        time_start: TimeType,
        time_end: TimeType,
        id: UUID | None = None,
    ):
        self.request = request
        self.date = date
        self.time_start = time_start
        self.time_end = time_end
        if id:
            self.id = id

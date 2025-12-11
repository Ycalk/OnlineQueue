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

    preferred_date: Mapped[DateType] = mapped_column()
    preferred_time_start: Mapped[TimeType] = mapped_column()
    preferred_time_end: Mapped[TimeType] = mapped_column()

    archived: Mapped[bool] = mapped_column(default=False)

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
    confirmation_datetime_history: Mapped[
        list["RequestConfirmationDatetimeHistoryItem"]
    ] = relationship(
        back_populates="request",
        cascade="all, delete-orphan",
        lazy="raise",
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="request",
        cascade="all, delete-orphan",
        lazy="raise",
    )
    priority_history: Mapped[list["RequestPriorityHistoryItem"]] = relationship(
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
        preferred_date: DateType,
        preferred_time_start: TimeType,
        preferred_time_end: TimeType,
        id: UUID | None = None,
        archived: bool | None = None,
    ):
        self.user_id = user_id
        self.queue = queue
        self.purpose = purpose

        self.preferred_date = preferred_date
        self.preferred_time_start = preferred_time_start
        self.preferred_time_end = preferred_time_end

        if id:
            self.id = id
        if archived is not None:
            self.archived = archived


class RequestStatusHistoryItem(Base):
    __tablename__ = "request_status_history_item"
    __table_args__ = {"schema": "request_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    request_id: Mapped[UUID] = mapped_column(ForeignKey(Request.id), index=True)
    status: Mapped[str] = mapped_column(String(50))
    occurred_at: Mapped[DateTimeType] = mapped_column(
        server_default=func.now(),
    )

    request: Mapped[Request] = relationship(back_populates="status_history")

    def __init__(
        self,
        request: Request,
        status: str,
        id: UUID | None = None,
        occurred_at: DateTimeType | None = None,
    ):
        self.request = request
        self.status = status
        if id:
            self.id = id
        if occurred_at:
            self.occurred_at = occurred_at


class RequestPriorityHistoryItem(Base):
    __tablename__ = "request_priority_history_item"
    __table_args__ = {"schema": "request_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    request_id: Mapped[UUID] = mapped_column(ForeignKey(Request.id), index=True)

    priority: Mapped[str] = mapped_column(String(50))
    occurred_at: Mapped[DateTimeType] = mapped_column(
        server_default=func.now(),
    )

    request: Mapped[Request] = relationship(back_populates="priority_history")

    def __init__(
        self,
        request: Request,
        priority: str,
        id: UUID | None = None,
        occurred_at: DateTimeType | None = None,
    ):
        self.request = request
        self.priority = priority
        if id:
            self.id = id
        if occurred_at:
            self.occurred_at = occurred_at


class RequestConfirmationDatetimeHistoryItem(Base):
    __tablename__ = "request_confirmation_datetime_history_item"
    __table_args__ = {"schema": "request_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    request_id: Mapped[UUID] = mapped_column(ForeignKey(Request.id), index=True)

    date: Mapped[DateType] = mapped_column()
    time_start: Mapped[TimeType] = mapped_column()
    time_end: Mapped[TimeType] = mapped_column()
    occurred_at: Mapped[DateTimeType] = mapped_column(
        server_default=func.now(),
    )

    request: Mapped[Request] = relationship(
        back_populates="confirmation_datetime_history"
    )

    def __init__(
        self,
        request: Request,
        date: DateType,
        time_start: TimeType,
        time_end: TimeType,
        id: UUID | None = None,
        occurred_at: DateTimeType | None = None,
    ):
        self.request = request
        self.date = date
        self.time_start = time_start
        self.time_end = time_end
        if id:
            self.id = id
        if occurred_at:
            self.occurred_at = occurred_at


class Comment(Base):
    __tablename__ = "request_comment"
    __table_args__ = {"schema": "request_schema"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    request_id: Mapped[UUID] = mapped_column(ForeignKey(Request.id), index=True)

    author: Mapped[str] = mapped_column(String(50))
    text: Mapped[str] = mapped_column(String(1000))

    created_at: Mapped[DateTimeType] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[DateTimeType] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    request: Mapped[Request] = relationship(back_populates="comments")

    def __init__(
        self,
        request: Request,
        author: str,
        text: str,
        id: UUID | None = None,
        created_at: DateTimeType | None = None,
    ):
        self.request = request
        self.author = author
        self.text = text
        if id:
            self.id = id
        if created_at:
            self.created_at = created_at

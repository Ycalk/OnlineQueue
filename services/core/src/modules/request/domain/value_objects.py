from __future__ import annotations

from datetime import date, time, datetime
from enum import StrEnum
from typing import Annotated, Self
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.types import PositiveInt, StringConstraints

from .errors import TimePeriodNotValid


# --- Общие value-объекты (как в queue) ---

class Name(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: Annotated[
        str,
        StringConstraints(min_length=1, max_length=100, strip_whitespace=True),
    ]


class Description(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: Annotated[
        str | None,
        StringConstraints(min_length=1, max_length=1000, strip_whitespace=True),
    ]


class IsActive(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: bool


class CleanupPeriod(BaseModel):
    model_config = ConfigDict(frozen=True)

    value_days: PositiveInt

    @property
    def value_seconds(self) -> int:
        return self.value_days * 86400

    @property
    def value_hours(self) -> float:
        return self.value_days / 24

    @property
    def value_minutes(self) -> float:
        return self.value_hours * 60


class TimePeriod(BaseModel):
    model_config = ConfigDict(frozen=True)

    start_time: time
    end_time: time

    @model_validator(mode="after")
    def check_start_time_before_end_time(self) -> Self:
        if self.start_time > self.end_time:
            raise TimePeriodNotValid("Start time must be before end time")
        return self


class UserId(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: UUID = Field(default_factory=uuid4)

    @classmethod
    def from_uuid(cls, value: UUID) -> Self:
        return cls(value=value)


class RequestId(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: UUID = Field(default_factory=uuid4)

    @classmethod
    def from_uuid(cls, value: UUID) -> Self:
        return cls(value=value)


class QueueId(BaseModel):
    """
    Локальный идентификатор очереди в bounded context `request`.
    Сюда прилетает UUID из ивента QueueCreated из BC queue.
    """

    model_config = ConfigDict(frozen=True)

    value: UUID

    @classmethod
    def from_uuid(cls, value: UUID) -> Self:
        return cls(value=value)


class RequestDateTime(BaseModel):
    """
    Конкретное подтверждённое время записи: дата + интервал.
    """

    model_config = ConfigDict(frozen=True)

    date: date
    time_period: TimePeriod

    @property
    def start_period(self) -> datetime:
        return datetime.combine(self.date, self.time_period.start_time)

    @property
    def end_period(self) -> datetime:
        return datetime.combine(self.date, self.time_period.end_time)


# --- Статус и приоритет заявки ---

class RequestStatus(StrEnum):
    PENDING = "pending"      # в очереди
    ACCEPTED = "accepted"    # принят
    REJECTED = "rejected"    # отклонен


class RequestPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# --- История статусов и подтверждений ---

class RequestStatusHistoryItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: RequestStatus
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class RequestConfirmationHistoryItem(BaseModel):
    """
    Элемент истории подтверждений: когда для заявки назначили
    конкретный интервал времени.
    """

    model_config = ConfigDict(frozen=True)

    date: date
    time_start: time
    time_end: time
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(mode="after")
    def check_time_order(self) -> Self:
        if self.time_start > self.time_end:
            raise TimePeriodNotValid("Start time must be before end time")
        return self

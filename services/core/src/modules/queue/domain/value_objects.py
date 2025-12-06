from pydantic import BaseModel, ConfigDict, model_validator, Field
from uuid import UUID, uuid4
from enum import StrEnum
from datetime import time, date, datetime
from pydantic.types import StringConstraints, PositiveInt
from typing import Annotated, Self
from .errors import TimePeriodNotValid


class Name(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: Annotated[
        str, StringConstraints(min_length=1, max_length=100, strip_whitespace=True)
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


class RequestDateTime(BaseModel):
    model_config = ConfigDict(frozen=True)

    date: date
    time_period: TimePeriod

    @property
    def start_period(self) -> datetime:
        return datetime.combine(self.date, self.time_period.start_time)

    @property
    def end_period(self) -> datetime:
        return datetime.combine(self.date, self.time_period.end_time)


class RequestStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

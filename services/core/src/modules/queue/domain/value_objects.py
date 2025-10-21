from pydantic import BaseModel, ConfigDict
from pydantic.types import StringConstraints, PositiveInt
from typing import Annotated
from modules.user.domain.aggregates import UserId


class OwnerId(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: UserId


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


class Active(BaseModel):
    model_config = ConfigDict(frozen=True)

    value: bool


class SlotDuration(BaseModel):
    model_config = ConfigDict(frozen=True)

    value_minutes: PositiveInt

    @property
    def value_seconds(self) -> int:
        return self.value_minutes * 60

    @property
    def value_hours(self) -> float:
        return self.value_minutes / 60

    @property
    def value_days(self) -> float:
        return self.value_hours / 24


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

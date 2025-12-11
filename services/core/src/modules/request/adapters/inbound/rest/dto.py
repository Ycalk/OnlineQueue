from datetime import date, time, timedelta, datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from modules.request.domain.value_objects import RequestPriority


class CreateRequestRequest(BaseModel):
    queue_id: UUID = Field(description="ID очереди, в которую записываемся")
    purpose: str = Field(min_length=1, max_length=1000, description="Цель визита")

    preferred_date: str = Field(
        description="Предпочтительная дата записи (формат: YYYY-MM-DD)",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        examples=["2025-01-01"],
    )
    preferred_time_start: str = Field(
        description="Предпочтительное время начала (формат: HH:MM)",
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
        examples=["09:00", "18:00"],
    )
    preferred_time_end: str = Field(
        description="Предпочтительное время окончания (формат: HH:MM)",
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
        examples=["09:30", "18:30"],
    )

    @field_validator("preferred_date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format (e.g., 2025-01-01)")

    @field_validator("preferred_time_start", "preferred_time_end")
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        try:
            hour, minute = map(int, v.split(":"))
            time(hour=hour, minute=minute)
            return v
        except (ValueError, AttributeError):
            raise ValueError("Time must be in HH:MM format (e.g., 09:00, 18:30)")

    def get_preferred_date(self) -> date:
        return date.fromisoformat(self.preferred_date)

    def get_preferred_time_start(self) -> time:
        hour, minute = map(int, self.preferred_time_start.split(":"))
        return time(hour=hour, minute=minute)

    def get_preferred_time_end(self) -> time:
        hour, minute = map(int, self.preferred_time_end.split(":"))
        return time(hour=hour, minute=minute)


class UpdateRequestConfirmationDatetime(BaseModel):
    date: str = Field(
        description="Дата записи (формат: YYYY-MM-DD)",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        examples=["2025-01-01"],
    )
    time_start: str = Field(
        description="Время начала (формат: HH:MM)",
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
        examples=["18:00"],
    )
    duration_minutes: int = Field(gt=0, description="Длительность визита в минутах")

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format (e.g., 2025-01-01)")

    @field_validator("time_start")
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        try:
            hour, minute = map(int, v.split(":"))
            time(hour=hour, minute=minute)
            return v
        except (ValueError, AttributeError):
            raise ValueError("Time must be in HH:MM format (e.g., 18:00)")

    def get_date(self):
        return date.fromisoformat(self.date)

    def get_time_start(self) -> time:
        hour, minute = map(int, self.time_start.split(":"))
        return time(hour=hour, minute=minute)

    def get_time_end(self) -> time:
        start_datetime = datetime.combine(self.get_date(), self.get_time_start())
        return (start_datetime + timedelta(minutes=self.duration_minutes)).time()


class UpdateRequestPriorityRequest(BaseModel):
    new_priority: RequestPriority = Field(
        description="Новый приоритет (low / medium / high)"
    )


class RequestCreatedResponse(BaseModel):
    id: UUID = Field(description="Идентификатор созданной записи")

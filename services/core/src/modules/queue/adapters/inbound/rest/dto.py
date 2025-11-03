from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import time


class CreateQueueRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Название очереди")
    description: str | None = Field(
        None, max_length=1000, description="Описание очереди"
    )
    cleanup_period_days: int = Field(
        gt=0, description="Период очистки архивных заявок в днях"
    )
    reception_time_start: str = Field(
        description="Время начала приема (формат: HH:MM)",
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
        examples=["09:00", "14:30", "18:45"],
    )
    reception_time_end: str = Field(
        description="Время окончания приема (формат: HH:MM)",
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
        examples=["17:00", "20:00", "23:59"],
    )

    @field_validator("reception_time_start", "reception_time_end")
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        try:
            hour, minute = map(int, v.split(":"))
            time(hour=hour, minute=minute)
            return v
        except (ValueError, AttributeError):
            raise ValueError("Time must be in HH:MM format (e.g., 09:00, 14:30)")

    def get_reception_time_start(self) -> time:
        hour, minute = map(int, self.reception_time_start.split(":"))
        return time(hour=hour, minute=minute)

    def get_reception_time_end(self) -> time:
        hour, minute = map(int, self.reception_time_end.split(":"))
        return time(hour=hour, minute=minute)


class UpdateQueueNameRequest(BaseModel):
    new_name: str = Field(min_length=1, max_length=100, description="Новое название")


class UpdateQueueDescriptionRequest(BaseModel):
    new_description: str = Field(max_length=1000, description="Новое описание")


class UpdateCleanupPeriodRequest(BaseModel):
    new_cleanup_period_days: int = Field(
        gt=0, description="Новый период очистки в днях"
    )


class QueueCreatedResponse(BaseModel):
    id: UUID = Field(description="Идентификатор очереди")

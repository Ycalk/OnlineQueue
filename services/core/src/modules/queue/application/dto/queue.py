from uuid import UUID
from pydantic import BaseModel, Field

from modules.queue.domain.value_objects import RequestStatus, RequestPriority


class Queue(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    description: str | None
    cleanup_period_days: int
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
    requests_avg_duration_seconds: int | None
    is_active: bool


class TimePeriod(BaseModel):
    start: int
    end: int


class Request(BaseModel):
    id: UUID
    user_id: UUID
    preferred_time: TimePeriod
    confirmed_time: TimePeriod | None
    archived: bool
    created_at: int
    status: RequestStatus
    priority: RequestPriority


class QueueWithRequests(Queue):
    requests: list[Request]

from uuid import UUID

from pydantic import BaseModel, Field

from modules.request.domain.value_objects import (
    RequestStatus,
    RequestPriority,
    Comment,
    RequestStatusHistoryItem,
    RequestPriorityHistoryItem,
)


class RequestDatetime(BaseModel):
    """
    start_unix и end_unix эквивалентны date, time_start и time_end
    только в unix timestamp формате, также они имеют одинаковую дату
    """

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
    time_end: str = Field(
        description="Время окончания (формат: HH:MM)",
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
        examples=["18:30"],
    )

    start_unix: int = Field(description="Unix timestamp времени начала")
    end_unix: int = Field(description="Unix timestamp времени окончания")


class ConfirmationDatetimeHistoryItem(RequestDatetime):
    occurred_at: int


class Request(BaseModel):
    id: UUID
    purpose: str

    user_id: UUID
    queue_id: UUID

    preferred_datetime: RequestDatetime
    confirmed_datetime: RequestDatetime | None

    confirmation_datetime_history: list[ConfirmationDatetimeHistoryItem]
    status_history: list[RequestStatusHistoryItem]
    priority_history: list[RequestPriorityHistoryItem]
    comments: list[Comment]

    is_archived: bool
    priority: RequestPriority
    status: RequestStatus

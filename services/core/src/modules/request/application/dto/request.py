from uuid import UUID

from pydantic import BaseModel, Field

from modules.request.domain.value_objects import RequestStatus, RequestPriority


class StatusHistoryItem(BaseModel):
    status: RequestStatus
    updated_at: int  # UNIX timestamp


class ConfirmationHistoryItem(BaseModel):
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
    updated_at: int  # UNIX timestamp, когда была зафиксирована эта запись истории


class Request(BaseModel):
    id: UUID
    purpose: str

    user_id: UUID
    queue_id: UUID

    # Предпочтительное время (из create-команды)
    preferred_date: str | None = Field(
        default=None,
        description="Предпочтительная дата (YYYY-MM-DD)",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
    )
    preferred_time_start: str | None = Field(
        default=None,
        description="Предпочтительное время начала (HH:MM)",
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
    )
    preferred_time_end: str | None = Field(
        default=None,
        description="Предпочтительное время окончания (HH:MM)",
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
    )

    # Текущее подтверждённое время (удобно для UI),
    # вычисляется как последнее из confirmation_history
    confirmed_date: str | None = Field(
        default=None,
        description="Подтверждённая дата (YYYY-MM-DD)",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
    )
    confirmed_time_start: str | None = Field(
        default=None,
        description="Подтверждённое время начала (HH:MM)",
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
    )
    confirmed_time_end: str | None = Field(
        default=None,
        description="Подтверждённое время окончания (HH:MM)",
        pattern=r"^([01]\d|2[0-3]):([0-5]\d)$",
    )

    confirmation_history: list[ConfirmationHistoryItem]
    status_history: list[StatusHistoryItem]

    is_archived: bool
    priority: RequestPriority
    status: RequestStatus

    created_at: int          # UNIX timestamp
    updated_at: int | None   # UNIX timestamp или None

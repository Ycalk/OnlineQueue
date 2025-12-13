from pydantic import BaseModel, model_validator, Field
from datetime import datetime
from typing import Self

from modules.queue.domain.value_objects import (
    RequestDateTime,
    RequestStatus,
    UserId,
    RequestId,
    RequestPriority,
)
from modules.queue.domain.errors import NotConsistentFields


# Значения статусов в связке с флагом archived
# PENDING archived - заявка попала под авто очистку
# PENDING not archived - ожидает подтверждения владельцем очереди и назначения времени
# ACCEPTED archived - заявка успешно обработана
# ACCEPTED not archived - время назначено и пользователь ожидает визит
# REJECTED archived - заявка отклонена владельцем очереди
# REJECTED not archived - невозможная связка значений
class Request(BaseModel):
    id: RequestId
    user_id: UserId
    preferred_time: RequestDateTime
    confirmed_time: RequestDateTime | None = None
    status: RequestStatus
    priority: RequestPriority
    archived: bool
    created_at: datetime = Field(default_factory=datetime.now)

    def archive(self) -> None:
        self.archived = True

    def reject(self) -> None:
        self.status = RequestStatus.REJECTED
        self.archived = True

    def calculate_duration_seconds(self) -> int | None:
        if self.confirmed_time is None:
            return None
        return int(
            self.confirmed_time.end_period.timestamp()
            - self.confirmed_time.start_period.timestamp()
        )

    @model_validator(mode="after")
    def check_confirmed_time(self) -> Self:
        if self.status == RequestStatus.ACCEPTED and self.confirmed_time is None:
            raise NotConsistentFields(
                "Confirmed time is required when request is accepted"
            )
        elif self.status == RequestStatus.PENDING and self.confirmed_time is not None:
            raise NotConsistentFields(
                "Confirmed time must not be set when request is pending"
            )
        elif self.status == RequestStatus.REJECTED and not self.archived:
            raise NotConsistentFields("Request must be archived when rejected")
        return self

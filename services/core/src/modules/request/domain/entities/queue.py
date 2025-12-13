from pydantic import BaseModel

from modules.request.domain.value_objects import (
    QueueId,
    UserId,
    IsActive,
    TimePeriod,
)
from modules.request.domain.errors import QueueAlreadyActivated, QueueAlreadyDeactivated


class Queue(BaseModel):
    id: QueueId
    owner_id: UserId
    is_active: IsActive
    reception_time: TimePeriod

    @classmethod
    def create(
        cls,
        id: QueueId,
        owner_id: UserId,
        is_active: IsActive,
        reception_time: TimePeriod,
    ):
        return cls(
            id=id,
            owner_id=owner_id,
            is_active=is_active,
            reception_time=reception_time,
        )

    def activate(self):
        if self.is_active.value:
            raise QueueAlreadyActivated(
                f"Queue with id {self.id.value} is already active"
            )
        self.is_active = IsActive(value=True)

    def deactivate(self):
        if not self.is_active.value:
            raise QueueAlreadyDeactivated(
                f"Queue with id {self.id.value} is already inactive"
            )
        self.is_active = IsActive(value=False)

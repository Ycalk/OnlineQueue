from pydantic import BaseModel

from modules.request.domain.value_objects import (
    QueueId,
    UserId,
    IsActive,
    TimePeriod,
)


class Queue(BaseModel):
    id: QueueId
    owner_id: UserId
    is_active: IsActive
    reception_time: TimePeriod

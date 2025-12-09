from datetime import datetime
from uuid import UUID


from shared.building_blocks import DomainEvent
from modules.request.domain.value_objects import (
    RequestId,
    UserId,
    QueueId,
    RequestDateTime,
)


class RequestAccepted(DomainEvent):
    request_id: UUID
    user_id: UUID
    queue_id: UUID
    accepted_at: datetime
    # Может быть принята без точного слота, либо с ним
    confirmed_datetime: RequestDateTime | None = None
